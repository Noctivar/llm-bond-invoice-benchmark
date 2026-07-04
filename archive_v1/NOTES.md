# archive_v1 — Notes

This folder preserves material that is intentionally **excluded from the main
case-study narrative** but kept for transparency. Nothing here has been deleted.

## `baseline_05_unexpected_pass/`

Contents:

* `solution.py` — moved from `attempts/baseline_05_unexpected_pass/solution.py`
* `baseline_05_unexpected_pass_eval.txt` — moved from
  `results/baseline_05_unexpected_pass_eval.txt`

### Why it is archived

* **Orphan run.** This run is **not included** in the main `README.md` results
  table, is **not recorded** in `metadata/runs.csv`, and is **not summarized** in
  `results/baseline_results.md`. It has no ledger entry tying it to a specific
  prompt or run number, so it cannot be cited as a canonical benchmark result.
* **Mislabeled / stale eval header.** The evaluation file's header reads
  `Evaluating: attempts/baseline_05/solution.py` yet reports a score of
  **16/16**. The canonical `baseline_05` run scores **0/16** (a degenerate
  `float(quote)` parse failure). The header therefore appears to have been
  copied from the `baseline_05` run and not updated, so the file's provenance is
  ambiguous.
* **Interesting but undocumented.** The archived solution is a full Treasury
  quote parser that passes all 16 cases — i.e., a case where a vague/baseline
  prompt appears to have produced correct code. This is a genuinely interesting
  data point, but because its prompt and provenance were never recorded, it is
  preserved here for transparency and **excluded from the main case-study
  narrative** rather than presented as a result.

If this run is ever promoted into the benchmark, it needs a reconciled prompt
record, a corrected eval header, and a proper `metadata/runs.csv` entry first.
