# Pyannote Diarization Report

## HMRC Talk Navigation

- [Narrative entry point](../narrative/index.md)
- [Navigation and scope](../narrative/notes/navigation-and-scope.md)
- [Transcript runbook](README.md)

- Run ID: `pyannote_community1_mps_20260511T111450Z`
- Model: `pyannote-community/speaker-diarization-community-1`
- Device: `mps`
- Torch: `2.11.0`
- Audio files: 2
- Total audio: 40.0 minutes
- Wall-clock processing: 83.8 seconds

## Speaker Clusters

### governing-agentic-ai-in-software-engineering
- SPEAKER_00: Trace; 664.6s total speech; first seen at 00:00:00.
- SPEAKER_01: Query; 520.3s total speech; first seen at 00:00:10.

### engineering-accountability-in-public-sector-ai
- SPEAKER_00: Trace; 595.0s total speech; first seen at 00:00:06.
- SPEAKER_01: Query; 568.3s total speech; first seen at 00:00:00.

## Caveats

- This is diarization, not named-speaker identification.
- `Trace` and `Query` are machine-assigned voice names. They are aligned across the two files using pyannote speaker embeddings when available.
- Text is assigned to the dominant diarized speaker for each Whisper SRT cue; a cue that contains both voices can still have mixed text under one voice name.
- Verify any important quotation against the source audio before public use.
