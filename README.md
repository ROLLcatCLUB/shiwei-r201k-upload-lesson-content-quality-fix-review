# 1013R_R201K_UPLOAD_LESSON_CONTENT_QUALITY_FIX_LOOP

R201J-P1 created teacher-readable snapshots but the content quality failed as usable lesson drafts. R201K is a bounded content-quality fix loop for uploaded lesson preview candidates.

## Decision

```text
PASS_AS_CONTENT_QUALITY_FIX_CANDIDATE_SNAPSHOTS_NOT_ROUTE_BOUND
```

This is still not a route switch, not R97B rendering, and not formal apply. It only creates repaired candidate teacher snapshots for review.

## What Changed

- Filled one teacher-readable key talk candidate for every episode.
- Repaired front matter from process episodes and evidence:
  - objectives
  - key and difficult points
  - preparation
- Replaced generic episode projection sentences with sample-specific student learning change, teacher organization, student action, and observable evidence.
- Repaired old-shoes objectives back to old-shoe redesign, material choice, design intent, 5-sentence story, and release preparation.
- Compressed teacher confirmation items into:
  - must confirm
  - suggested confirm
  - folded diagnostic
- Rewrote table evidence in the umbrella sample into natural teacher language.

## Boundary

- No R201I schema structure change.
- No R220E rendering.
- No R97B shell change.
- No formal apply.
- No database / Feishu / memory write.
- No R95.
- No provider or model call.

## Main Files

- `r201k_content_quality_fix_report.md`
- `r201k_before_after_teacher_snapshot_comparison.md`
- `r201k_front_matter_derivation_policy.md`
- `r201k_episode_projection_repair_report.md`
- `r201k_key_teacher_talk_candidate_policy.md`
- `r201k_confirmation_item_grouping_policy.md`
- `r201k_table_evidence_sanitizer_report.md`
- `sample_snapshots_after_fix/*/teacher_readable_lesson_snapshot.md`
- `validate_1013R_R201K_upload_lesson_content_quality_fix_loop_result.json`

## Validation

All required checks passed:

- `missing_key_teacher_talk_count_zero = true`
- `generic_episode_projection_count_zero = true`
- `old_shoes_objective_misalignment_zero = true`
- `table_evidence_raw_field_dump_count_zero = true`
- `teacher_confirm_item_count_per_sample_lte_8 = true`
- `front_matter_thin_blocking_count_zero = true`
- `engineering_term_in_teacher_main_zero = true`
- `source_gap_as_teacher_content_zero = true`
- `teacher_main_forbidden_sources_zero = true`
