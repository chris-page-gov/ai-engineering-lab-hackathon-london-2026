# HMRC Beyond the Hype Audio Transcripts

Generated locally from the two M4A files in `research/hmrc-beyond-hype/import/` using `ffmpeg`, `whisper-cli`, and pyannote diarization.

These transcripts are machine-generated and should be reviewed before quoting in slides or speaker notes.

| Source audio | Duration | Transcript | Subtitles | Speaker transcript | Characters |
|---|---:|---|---|---|---:|
| `Governing_agentic_AI_in_software_engineering.m4a` | 20.2 min | [governing-agentic-ai-in-software-engineering.txt](governing-agentic-ai-in-software-engineering.txt) | [governing-agentic-ai-in-software-engineering.srt](governing-agentic-ai-in-software-engineering.srt) | [governing-agentic-ai-in-software-engineering.speakers.md](governing-agentic-ai-in-software-engineering.speakers.md) | 21785 |
| `Engineering_Accountability_in_Public_Sector_AI.m4a` | 19.8 min | [engineering-accountability-in-public-sector-ai.txt](engineering-accountability-in-public-sector-ai.txt) | [engineering-accountability-in-public-sector-ai.srt](engineering-accountability-in-public-sector-ai.srt) | [engineering-accountability-in-public-sector-ai.speakers.md](engineering-accountability-in-public-sector-ai.speakers.md) | 21204 |

## Review Notes

- Whisper provides the base text and subtitle timings.
- Speaker-attributed transcripts use pyannote diarization and `Trace` / `Query` voice names; they are review drafts, not verified human transcripts.
- Voice names are aligned across the two audio files when pyannote embeddings are available, so a file does not necessarily start with `Trace`.
- Treat important quotes as provisional until checked against the audio.
- The raw M4A files are local import resources and are not committed by default.

## Reproduction

```bash
python3 research/hmrc-beyond-hype/tools/transcribe_audio.py --model /path/to/ggml-base.en.bin
uv run --with pyannote.audio --with torch python research/hmrc-beyond-hype/tools/diarize_audio_transcripts.py
```
