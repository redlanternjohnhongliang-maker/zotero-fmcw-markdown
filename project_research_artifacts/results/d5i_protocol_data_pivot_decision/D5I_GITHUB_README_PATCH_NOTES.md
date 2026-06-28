# D5I GitHub README Patch Notes

**目标仓库**: `redlanternjohnhongliang-maker/zotero-fmcw-markdown`  
**当前提交**: `ac44e62`  
**用途**: 给 GitHub README 和 `project_research_artifacts/README.md` 补充 D5I 后的路线说明。

## 1. 建议补到根 README 的内容

```markdown
## D5I Protocol/Data Pivot Decision

After the D5H-Exec no-training representation audit, no representation is eligible for training escalation. The project should not continue weak weighting, should not enter D6, and should not modify the detector or fixed-PFA evaluation protocol.

Current route ranking:

1. External labeled dataset feasibility: RADIal, RADDet, and CARRADA are candidates, but no dataset download or training is allowed yet.
2. Controlled synthetic RAD protocol sanity: next smallest executable action after the feasibility table, protocol unit test only.
3. Negative-result / limitation consolidation: useful report direction after adding dataset feasibility, classical baseline review, and a protocol diagram.
4. Gao77 RA calibration RCA: diagnostic appendix only; not a main result route.

The next recommended executable project step is D5J: validate the fixed-PFA weak-target metric chain in a controlled synthetic RAD unit test with known range, Doppler, azimuth, target strength, overlap, SIR, clean/interfered pairing, and false-alarm budget. This synthetic test is not a real-world performance claim.
```

## 2. 建议补到 project_research_artifacts/README.md 的内容

```markdown
## D5I Pivot Decision

`results/d5i_protocol_data_pivot_decision/` records the protocol/data pivot decision after D5H-Exec no-pass.

Main decision:

- No model training.
- No D6.
- No weak weighting continuation.
- No false alarm penalty.
- No detector or fixed-PFA protocol modification.
- Gao77 remains diagnostic evidence only.
- External datasets remain feasibility candidates only until label/engineering checks are complete.
- Controlled synthetic RAD protocol is allowed as a protocol unit test after the minimal feasibility table.

Read in this order:

1. `D5I_NEXT_STEP_DECISION.md`
2. `D5I_ROUTE_COMPARISON.md`
3. `D5I_DATASET_FEASIBILITY_TABLE.csv`
4. `D5I_RESULT_TO_CLAIM.md`
5. `D5I_KILL_ARGUMENT.md`
```

## 3. 建议 GitHub 目录变更

建议把本地目录：

```text
G:\mineru_output\results\d5i_protocol_data_pivot_decision
```

同步到 GitHub 归档仓库：

```text
G:\mineru_output\05_github_upload\zotero-fmcw-markdown\project_research_artifacts\results\d5i_protocol_data_pivot_decision
```

## 4. 不建议补的内容

- 不上传 raw `.mat`、原始 ADC、PDF、Zotero 数据库、模型权重或完整训练产物。
- 不把 D5I 写成 positive performance result。
- 不把 synthetic protocol 写成 real-world mitigation result。
- 不把 Gao77 RA diagnostic 写成 confirmed RA performance。
