# Metadata

## Claude Code Runs

| Run | Model | Tool Version | Prompt Timestamp UTC | Final Response Timestamp UTC | Score | Raw Transcript |
| --- | --- | --- | --- | --- | ---: | --- |
| baseline_01 | claude-opus-4-8 | 2.1.196 | 2026-06-30T11:57:58.171Z | 2026-06-30T11:58:38.511Z | 11/16 | `metadata/baseline_01_raw.jsonl` |
| baseline_02 | claude-opus-4-8 | 2.1.196 | 2026-06-30T12:01:05.439Z | 2026-06-30T12:01:36.769Z | 11/16 | `metadata/baseline_02_raw.jsonl` |
| baseline_03 | claude-opus-4-8 | 2.1.196 | 2026-06-30T12:02:26.628Z | 2026-06-30T12:03:10.619Z | 11/16 | `metadata/baseline_03_raw.jsonl` |
| baseline_04 | claude-opus-4-8 | 2.1.196 | 2026-06-30T12:04:02.078Z | 2026-06-30T12:04:53.101Z | 11/16 | `metadata/baseline_04_raw.jsonl` |
| baseline_05 | claude-opus-4-8 | 2.1.196 | 2026-06-30T12:14:36.155Z | 2026-06-30T12:15:11.128Z | 0/16 | `metadata/baseline_05_raw.jsonl` |
| improved_01 | claude-opus-4-8 | 2.1.196 | 2026-06-30T12:17:20.882Z | 2026-06-30T12:17:55.803Z | 16/16 | `metadata/improved_01_raw.jsonl` |
| improved_02 | claude-opus-4-8 | 2.1.196 | 2026-06-30T12:19:21.335Z | 2026-06-30T12:19:41.235Z | 16/16 | `metadata/improved_02_raw.jsonl` |
| improved_03 | claude-opus-4-8 | 2.1.196 | 2026-06-30T12:20:01.223Z | 2026-06-30T12:20:46.708Z | 16/16 | `metadata/improved_03_raw.jsonl` |
| improved_04 | claude-opus-4-8 | 2.1.196 | 2026-06-30T12:21:11.277Z | 2026-06-30T12:21:30.567Z | 16/16 | `metadata/improved_04_raw.jsonl` |
| improved_05 | claude-opus-4-8 | 2.1.196 | 2026-06-30T12:21:46.438Z | 2026-06-30T12:22:03.080Z | 16/16 | `metadata/improved_05_raw.jsonl` |

All runs were executed through Claude Code using the Anthropic model `claude-opus-4-8` and Claude Code version `2.1.196`.

The complete session IDs, prompt UUIDs, final response UUIDs, request IDs, response IDs, request-response pairs, evaluation scores, and transcript paths are recorded in `metadata/runs.csv`.

## Captured Evidence

* Generated code for every run in `attempts/`.
* Raw Claude Code JSONL transcripts for all five baseline and five improved runs in `metadata/`.
* Request IDs and response IDs for every model round trip in `metadata/runs.csv`.
* Evaluation cases in `cases.json`.
* Evaluator in `evaluate_attempt.py`.
* Oracle implementation in `oracle.py`.
* Per-run evaluation outputs in `results/`.
* Baseline scores of 11/16, 11/16, 11/16, 11/16, and 0/16.
* Improved scores of 16/16 for all five runs.
* Audit test result: 29 tests passed.

## Remaining Uncaptured Settings

Temperature, top-p, and other server-side generation settings are not present in the recovered Claude Code transcripts. All identifiers and timestamps available in the local JSONL records are now preserved.

## Prompt Records

The submitted baseline prompts are recorded in `results/baseline_results.md`, with abbreviated prompt records retained in `prompts/baseline_prompts.md`. Generated artifacts are stored under `attempts/[run]/solution.py`.
