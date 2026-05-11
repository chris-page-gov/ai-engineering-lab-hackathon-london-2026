#!/usr/bin/env python3
"""Add speaker-attributed transcripts using local pyannote diarization."""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from itertools import permutations
from pathlib import Path
from typing import Any

os.environ.setdefault("PYTORCH_ENABLE_MPS_FALLBACK", "1")

import numpy as np
import torch
from pyannote.audio import Pipeline


PACK_DIR = Path(__file__).resolve().parents[1]
IMPORT_DIR = PACK_DIR / "import"
TRANSCRIPTS_DIR = PACK_DIR / "transcripts"
WAV_DIR = TRANSCRIPTS_DIR / "_wav"
RUNS_CSV = TRANSCRIPTS_DIR / "pyannote_diarization_runs.csv"
SEGMENTS_CSV = TRANSCRIPTS_DIR / "pyannote_diarization_segments.csv"
REPORT_MD = TRANSCRIPTS_DIR / "pyannote_diarization_report.md"
MANIFEST_JSON = TRANSCRIPTS_DIR / "manifest.json"
DEFAULT_MODEL = "pyannote-community/speaker-diarization-community-1"

AUDIO_FILES = (
    "Governing_agentic_AI_in_software_engineering.m4a",
    "Engineering_Accountability_in_Public_Sector_AI.m4a",
)


@dataclass(frozen=True)
class AudioItem:
    slug: str
    source: Path
    transcript: Path
    srt: Path
    speaker_md: Path
    speaker_txt: Path
    wav: Path


@dataclass(frozen=True)
class SrtCue:
    index: int
    start_seconds: float
    end_seconds: float
    text: str


def slugify(value: str) -> str:
    value = Path(value).stem.replace("_", "-")
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def format_seconds(seconds: float) -> str:
    total = max(0, int(seconds))
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def parse_srt_timestamp(value: str) -> float:
    hours, minutes, seconds = value.replace(",", ".").split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def parse_srt(path: Path) -> list[SrtCue]:
    blocks = re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip())
    cues: list[SrtCue] = []
    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if len(lines) < 3 or "-->" not in lines[1]:
            continue
        start_text, end_text = [part.strip() for part in lines[1].split("-->", 1)]
        cues.append(
            SrtCue(
                index=int(lines[0]) if lines[0].isdigit() else len(cues) + 1,
                start_seconds=parse_srt_timestamp(start_text),
                end_seconds=parse_srt_timestamp(end_text),
                text=" ".join(lines[2:]),
            )
        )
    return cues


def overlap_seconds(start_a: float, end_a: float, start_b: float, end_b: float) -> float:
    return max(0.0, min(end_a, end_b) - max(start_a, start_b))


def normalized(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(normalized(a), normalized(b)))


def choose_device(requested: str) -> str:
    if requested != "auto":
        return requested
    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def duration_seconds(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    return float(result.stdout.strip())


def ensure_wav(item: AudioItem) -> None:
    if item.wav.exists() and item.wav.stat().st_size > 0:
        return
    item.wav.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(item.source),
            "-ac",
            "1",
            "-ar",
            "16000",
            "-sample_fmt",
            "s16",
            str(item.wav),
        ],
        check=True,
    )


def audio_items() -> list[AudioItem]:
    items: list[AudioItem] = []
    for file_name in AUDIO_FILES:
        slug = slugify(file_name)
        items.append(
            AudioItem(
                slug=slug,
                source=IMPORT_DIR / file_name,
                transcript=TRANSCRIPTS_DIR / f"{slug}.txt",
                srt=TRANSCRIPTS_DIR / f"{slug}.srt",
                speaker_md=TRANSCRIPTS_DIR / f"{slug}.speakers.md",
                speaker_txt=TRANSCRIPTS_DIR / f"{slug}.speakers.txt",
                wav=WAV_DIR / f"{slug}.wav",
            )
        )
    return items


def dominant_label(
    rows: list[dict[str, Any]], start_seconds: float, end_seconds: float
) -> tuple[str, float]:
    totals: dict[str, float] = {}
    for row in rows:
        overlap = overlap_seconds(
            start_seconds,
            end_seconds,
            float(row["start_seconds"]),
            float(row["end_seconds"]),
        )
        if overlap > 0:
            label = str(row["local_speaker_label"])
            totals[label] = totals.get(label, 0.0) + overlap
    if not totals:
        return "UNKNOWN", 0.0
    return max(totals.items(), key=lambda item: item[1])


def diarize(
    items: list[AudioItem], model_id: str, device_name: str
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    pipeline = Pipeline.from_pretrained(model_id)
    pipeline.to(torch.device(device_name))

    segment_rows: list[dict[str, Any]] = []
    item_results: dict[str, dict[str, Any]] = {}

    for item in items:
        ensure_wav(item)
        started = time.perf_counter()
        output = pipeline(str(item.wav), min_speakers=2, max_speakers=2)
        elapsed_seconds = time.perf_counter() - started

        annotation = getattr(output, "speaker_diarization", output)
        labels = list(annotation.labels())
        embeddings = np.asarray(getattr(output, "speaker_embeddings", []))
        label_embeddings = {
            label: embeddings[index].astype(float)
            for index, label in enumerate(labels)
            if index < len(embeddings)
        }

        local_segments: list[dict[str, Any]] = []
        for segment_index, (turn, _track, label) in enumerate(
            annotation.itertracks(yield_label=True), start=1
        ):
            row = {
                "slug": item.slug,
                "source_file": str(item.source.relative_to(Path.cwd())),
                "wav_path": str(item.wav.relative_to(Path.cwd())),
                "srt_path": str(item.srt.relative_to(Path.cwd())),
                "segment_index": segment_index,
                "start_seconds": round(float(turn.start), 3),
                "end_seconds": round(float(turn.end), 3),
                "duration_seconds": round(float(turn.end - turn.start), 3),
                "local_speaker_label": label,
            }
            local_segments.append(row)
            segment_rows.append(row)

        first_start_by_label: dict[str, float] = {}
        total_by_label: dict[str, float] = {}
        for row in local_segments:
            label = str(row["local_speaker_label"])
            first_start_by_label[label] = min(
                first_start_by_label.get(label, float("inf")), float(row["start_seconds"])
            )
            total_by_label[label] = total_by_label.get(label, 0.0) + float(
                row["duration_seconds"]
            )

        item_results[item.slug] = {
            "item": item,
            "elapsed_seconds": elapsed_seconds,
            "labels": labels,
            "label_embeddings": label_embeddings,
            "segments": local_segments,
            "first_start_by_label": first_start_by_label,
            "total_by_label": total_by_label,
        }
        print(
            f"{item.slug}: {len(labels)} speakers, {len(local_segments)} segments, "
            f"{elapsed_seconds:.1f}s"
        )

    return segment_rows, item_results


def build_global_speaker_map(item_results: dict[str, dict[str, Any]]) -> dict[tuple[str, str], str]:
    slugs = list(item_results.keys())
    first = item_results[slugs[0]]
    first_labels = sorted(
        first["labels"],
        key=lambda label: first["first_start_by_label"].get(label, float("inf")),
    )
    reference: dict[str, np.ndarray] = {}
    speaker_map: dict[tuple[str, str], str] = {}
    for index, label in enumerate(first_labels[:2], start=1):
        speaker_name = f"Speaker {index}"
        speaker_map[(slugs[0], label)] = speaker_name
        embedding = first["label_embeddings"].get(label)
        if embedding is not None:
            reference[speaker_name] = normalized(embedding)

    for slug in slugs[1:]:
        result = item_results[slug]
        labels = list(result["labels"])
        if len(labels) == 2 and len(reference) == 2:
            speaker_names = list(reference.keys())
            best_perm: tuple[str, str] | None = None
            best_score = float("-inf")
            for perm in permutations(speaker_names):
                score = 0.0
                for label, speaker_name in zip(labels, perm, strict=True):
                    embedding = result["label_embeddings"].get(label)
                    score += cosine(embedding, reference[speaker_name]) if embedding is not None else -1.0
                if score > best_score:
                    best_score = score
                    best_perm = perm
            if best_perm is not None:
                for label, speaker_name in zip(labels, best_perm, strict=True):
                    speaker_map[(slug, label)] = speaker_name
                continue

        sorted_labels = sorted(
            labels,
            key=lambda label: result["first_start_by_label"].get(label, float("inf")),
        )
        for index, label in enumerate(sorted_labels[:2], start=1):
            speaker_map[(slug, label)] = f"Speaker {index}"

    return speaker_map


def speaker_for_cue(
    slug: str,
    cue: SrtCue,
    segments: list[dict[str, Any]],
    speaker_map: dict[tuple[str, str], str],
) -> tuple[str, float, str]:
    label, overlap = dominant_label(segments, cue.start_seconds, cue.end_seconds)
    return speaker_map.get((slug, label), "Unknown"), overlap, label


def write_speaker_transcripts(
    item_results: dict[str, dict[str, Any]],
    speaker_map: dict[tuple[str, str], str],
    run_row: dict[str, Any],
) -> None:
    for result in item_results.values():
        item: AudioItem = result["item"]
        cues = parse_srt(item.srt)
        segments = result["segments"]
        turns: list[dict[str, Any]] = []

        for cue in cues:
            speaker, overlap, local_label = speaker_for_cue(
                item.slug, cue, segments, speaker_map
            )
            if turns and turns[-1]["speaker"] == speaker:
                turns[-1]["end_seconds"] = cue.end_seconds
                turns[-1]["text"].append(cue.text)
                turns[-1]["cue_count"] += 1
            else:
                turns.append(
                    {
                        "speaker": speaker,
                        "local_label": local_label,
                        "start_seconds": cue.start_seconds,
                        "end_seconds": cue.end_seconds,
                        "text": [cue.text],
                        "cue_count": 1,
                        "dominant_overlap_seconds": round(overlap, 3),
                    }
                )

        header = [
            f"# {item.slug.replace('-', ' ').title()}",
            "",
            f"- Source audio: `{item.source.relative_to(Path.cwd())}`",
            f"- Base transcript: `{item.transcript.relative_to(Path.cwd())}`",
            f"- Subtitle timing: `{item.srt.relative_to(Path.cwd())}`",
            f"- Diarization model: `{run_row['model_id']}`",
            f"- Device: `{run_row['device']}`",
            "- Speaker labels: `Speaker 1` / `Speaker 2` from pyannote diarization",
            "",
            "Machine-generated transcript and diarization. Verify important quotes against "
            "the audio before using them in slides, speaker notes, or published material.",
            "",
            "## Speaker-Attributed Transcript",
            "",
        ]
        body = []
        plain = []
        for turn in turns:
            span = f"{format_seconds(turn['start_seconds'])}-{format_seconds(turn['end_seconds'])}"
            text = " ".join(turn["text"]).strip()
            body.append(f"**{turn['speaker']} [{span}]**: {text}")
            body.append("")
            plain.append(f"{turn['speaker']} [{span}]: {text}")
            plain.append("")

        item.speaker_md.write_text("\n".join(header + body), encoding="utf-8")
        item.speaker_txt.write_text("\n".join(plain), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def update_manifest(run_row: dict[str, Any], items: list[AudioItem]) -> None:
    manifest = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
    records = manifest.get("runs") or manifest.get("items") or []
    by_slug = {run["slug"]: run for run in records}
    for item in items:
        run = by_slug.get(item.slug)
        if not run:
            continue
        run["speaker_transcript_path"] = str(item.speaker_md.relative_to(Path.cwd()))
        run["speaker_transcript_text_path"] = str(item.speaker_txt.relative_to(Path.cwd()))
        run["diarization"] = {
            "model": run_row["model_id"],
            "device": run_row["device"],
            "run_id": run_row["run_id"],
            "speaker_labels": ["Speaker 1", "Speaker 2"],
        }
    manifest["diarization_run"] = run_row
    manifest["updated_at"] = datetime.now(UTC).isoformat()
    MANIFEST_JSON.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def write_readme(items: list[AudioItem]) -> None:
    manifest = json.loads(MANIFEST_JSON.read_text(encoding="utf-8"))
    records = manifest.get("runs") or manifest.get("items") or []
    by_slug = {run["slug"]: run for run in records}

    lines = [
        "# HMRC Beyond the Hype Audio Transcripts",
        "",
        "Generated locally from the two M4A files in `research/hmrc-beyond-hype/import/` "
        "using `ffmpeg`, `whisper-cli`, and pyannote diarization.",
        "",
        "These transcripts are machine-generated and should be reviewed before quoting in "
        "slides or speaker notes.",
        "",
        "| Source audio | Duration | Transcript | Subtitles | Speaker transcript | Characters |",
        "|---|---:|---|---|---|---:|",
    ]
    for item in items:
        run = by_slug[item.slug]
        lines.append(
            f"| `{item.source.name}` | {float(run['duration_seconds']) / 60:.1f} min | "
            f"[{item.transcript.name}]({item.transcript.name}) | "
            f"[{item.srt.name}]({item.srt.name}) | "
            f"[{item.speaker_md.name}]({item.speaker_md.name}) | "
            f"{run['transcript_chars']} |"
        )
    lines.extend(
        [
            "",
            "## Review Notes",
            "",
            "- Whisper provides the base text and subtitle timings.",
            "- Speaker-attributed transcripts use pyannote diarization and `Speaker 1` / "
            "`Speaker 2` labels; they are review drafts, not verified human transcripts.",
            "- Speaker labels are aligned across the two audio files when pyannote embeddings "
            "are available, so a file does not necessarily start with `Speaker 1`.",
            "- Treat important quotes as provisional until checked against the audio.",
            "- The raw M4A files are local import resources and are not committed by default.",
            "",
            "## Reproduction",
            "",
            "```bash",
            "python3 research/hmrc-beyond-hype/tools/transcribe_audio.py "
            "--model /path/to/ggml-base.en.bin",
            "uv run --with pyannote.audio --with torch "
            "python research/hmrc-beyond-hype/tools/diarize_audio_transcripts.py",
            "```",
            "",
        ]
    )
    (TRANSCRIPTS_DIR / "README.md").write_text("\n".join(lines), encoding="utf-8")


def write_report(
    run_row: dict[str, Any],
    item_results: dict[str, dict[str, Any]],
    speaker_map: dict[tuple[str, str], str],
) -> None:
    lines = [
        "# Pyannote Diarization Report",
        "",
        f"- Run ID: `{run_row['run_id']}`",
        f"- Model: `{run_row['model_id']}`",
        f"- Device: `{run_row['device']}`",
        f"- Torch: `{run_row['torch_version']}`",
        f"- Audio files: {run_row['audio_file_count']}",
        f"- Total audio: {run_row['total_audio_seconds'] / 60:.1f} minutes",
        f"- Wall-clock processing: {run_row['wall_clock_seconds']:.1f} seconds",
        "",
        "## Speaker Clusters",
        "",
    ]
    for slug, result in item_results.items():
        lines.append(f"### {slug}")
        for label in sorted(result["labels"]):
            speaker = speaker_map.get((slug, label), "Unknown")
            total = result["total_by_label"].get(label, 0.0)
            first_start = result["first_start_by_label"].get(label, 0.0)
            lines.append(
                f"- {label}: {speaker}; {total:.1f}s total speech; first seen at "
                f"{format_seconds(first_start)}."
            )
        lines.append("")

    lines.extend(
        [
            "## Caveats",
            "",
            "- This is diarization, not named-speaker identification.",
            "- `Speaker 1` and `Speaker 2` are machine-assigned labels. They are aligned across "
            "the two files using pyannote speaker embeddings when available.",
            "- Text is assigned to the dominant diarized speaker for each Whisper SRT cue; a cue "
            "that contains both voices can still have mixed text under one speaker label.",
            "- Verify any important quotation against the source audio before public use.",
            "",
        ]
    )
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--device", default="auto", choices=["auto", "cpu", "mps", "cuda"])
    args = parser.parse_args()

    items = audio_items()
    for item in items:
        for path in (item.source, item.transcript, item.srt):
            if not path.exists():
                raise SystemExit(f"Required file not found: {path}")

    device_name = choose_device(args.device)
    run_id = f"pyannote_community1_{device_name}_{datetime.now(UTC):%Y%m%dT%H%M%SZ}"
    started = time.perf_counter()
    segment_rows, item_results = diarize(items, args.model, device_name)
    speaker_map = build_global_speaker_map(item_results)

    enriched_segments: list[dict[str, Any]] = []
    for row in segment_rows:
        enriched_segments.append(
            {
                **row,
                "speaker_label": speaker_map.get(
                    (str(row["slug"]), str(row["local_speaker_label"])), "Unknown"
                ),
                "run_id": run_id,
                "model_id": args.model,
                "device": device_name,
            }
        )

    run_row = {
        "run_id": run_id,
        "model_id": args.model,
        "device": device_name,
        "torch_version": torch.__version__,
        "mps_available": bool(torch.backends.mps.is_available()),
        "audio_file_count": len(items),
        "total_audio_seconds": round(sum(duration_seconds(item.source) for item in items), 3),
        "wall_clock_seconds": round(time.perf_counter() - started, 3),
        "created_at": datetime.now(UTC).isoformat(),
        "params_json": json.dumps({"min_speakers": 2, "max_speakers": 2}),
    }

    write_csv(RUNS_CSV, [run_row])
    write_csv(SEGMENTS_CSV, enriched_segments)
    write_speaker_transcripts(item_results, speaker_map, run_row)
    write_report(run_row, item_results, speaker_map)
    update_manifest(run_row, items)
    write_readme(items)
    print(f"Wrote {RUNS_CSV}")
    print(f"Wrote {SEGMENTS_CSV}")
    print(f"Wrote {REPORT_MD}")


if __name__ == "__main__":
    main()
