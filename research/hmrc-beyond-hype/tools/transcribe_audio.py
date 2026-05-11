#!/usr/bin/env python3
"""Transcribe HMRC talk-prep audio with local whisper.cpp tooling."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path


PACK_DIR = Path(__file__).resolve().parents[1]
IMPORT_DIR = PACK_DIR / "import"
TRANSCRIPTS_DIR = PACK_DIR / "transcripts"
WAV_DIR = TRANSCRIPTS_DIR / "_wav"

AUDIO_FILES = (
    "Governing_agentic_AI_in_software_engineering.m4a",
    "Engineering_Accountability_in_Public_Sector_AI.m4a",
)


@dataclass(frozen=True)
class TranscriptRun:
    slug: str
    source_file: str
    duration_seconds: float
    transcript_path: str
    srt_path: str
    transcript_chars: int
    tool: str
    model: str
    execution: str
    threads: int
    elapsed_seconds_this_run: float


def slugify(value: str) -> str:
    value = Path(value).stem.replace("_", "-")
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def run_command(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, check=True, text=True, capture_output=True)


def duration_seconds(path: Path) -> float:
    result = run_command(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(path),
        ]
    )
    return float(result.stdout.strip())


def ensure_wav(source: Path, wav_path: Path) -> None:
    if wav_path.exists() and wav_path.stat().st_size > 0:
        return
    wav_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            str(source),
            "-ac",
            "1",
            "-ar",
            "16000",
            "-sample_fmt",
            "s16",
            str(wav_path),
        ],
        check=True,
    )


def write_readme(runs: list[TranscriptRun]) -> None:
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
    for run in runs:
        speaker_md = f"{run.slug}.speakers.md"
        lines.append(
            f"| `{Path(run.source_file).name}` | {run.duration_seconds / 60:.1f} min | "
            f"[{Path(run.transcript_path).name}]({Path(run.transcript_path).name}) | "
            f"[{Path(run.srt_path).name}]({Path(run.srt_path).name}) | "
            f"[{speaker_md}]({speaker_md}) | {run.transcript_chars} |"
        )
    lines.extend(
        [
            "",
            "## Review Notes",
            "",
            "- Whisper provides the base text and subtitle timings.",
            "- Speaker-attributed transcripts use pyannote diarization and `Trace` / "
            "`Query` voice names; they are review drafts, not verified human transcripts.",
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        required=True,
        help="Path to a whisper.cpp model file.",
    )
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        raise SystemExit("ffmpeg is required")
    if shutil.which("ffprobe") is None:
        raise SystemExit("ffprobe is required")
    if shutil.which("whisper-cli") is None:
        raise SystemExit("whisper-cli is required")
    model_path = Path(args.model)
    if not model_path.exists():
        raise SystemExit(f"Whisper model not found: {model_path}")

    TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)
    runs: list[TranscriptRun] = []
    started_at = datetime.now(UTC).isoformat()

    for file_name in AUDIO_FILES:
        source = IMPORT_DIR / file_name
        if not source.exists():
            raise SystemExit(f"Source audio not found: {source}")
        slug = slugify(file_name)
        wav_path = WAV_DIR / f"{slug}.wav"
        transcript_path = TRANSCRIPTS_DIR / f"{slug}.txt"
        srt_path = TRANSCRIPTS_DIR / f"{slug}.srt"

        print(f"Converting {file_name} to WAV...")
        ensure_wav(source, wav_path)

        started = time.perf_counter()
        print(f"Transcribing {file_name} with whisper-cli CPU/no-flash...")
        subprocess.run(
            [
                "whisper-cli",
                "-m",
                str(model_path),
                "-f",
                str(wav_path),
                "-l",
                "en",
                "-t",
                str(args.threads),
                "-otxt",
                "-osrt",
                "-of",
                str(TRANSCRIPTS_DIR / slug),
                "-np",
                "-ng",
                "-nfa",
            ],
            check=True,
        )
        elapsed = time.perf_counter() - started
        runs.append(
            TranscriptRun(
                slug=slug,
                source_file=str(source.relative_to(Path.cwd())),
                duration_seconds=round(duration_seconds(source), 3),
                transcript_path=str(transcript_path.relative_to(Path.cwd())),
                srt_path=str(srt_path.relative_to(Path.cwd())),
                transcript_chars=len(transcript_path.read_text(encoding="utf-8")),
                tool="whisper-cli",
                model=model_path.name,
                execution="CPU with no flash attention (-ng -nfa)",
                threads=args.threads,
                elapsed_seconds_this_run=round(elapsed, 3),
            )
        )

    manifest = {
        "created_at": started_at,
        "generated_by": "research/hmrc-beyond-hype/tools/transcribe_audio.py",
        "runs": [asdict(run) for run in runs],
    }
    (TRANSCRIPTS_DIR / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n",
        encoding="utf-8",
    )
    write_readme(runs)
    print(json.dumps(manifest["runs"], indent=2))


if __name__ == "__main__":
    main()
