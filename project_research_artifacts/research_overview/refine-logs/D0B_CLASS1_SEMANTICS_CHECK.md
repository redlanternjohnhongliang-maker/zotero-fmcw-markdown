# D0B `class=1` 语义核查

生成时间：2026-06-26 15:55

## 结论

`class=1` 建议在 D1A sanity 中按 `cyclist / bicycle-like` 处理，并与官方 README 中的 `class=80: cyclist` 合并为同一类目标。

这是高置信推断，但不是官方 README 明文定义。后续写报告时应表述为：`class=1` appears to be a cyclist/bicycle annotation alias, likely due to labeling inconsistency。

## 依据

1. 官方 GitHub README 的 label map 只写了：
   - `0: person`
   - `2: car`
   - `3: motorbike`
   - `5: bus`
   - `7: truck`
   - `80: cyclist`
2. README 历史版本也没有找到 `class=1` 的明确定义。
3. 全量标签扫描显示：
   - `class=1` 全量只有 106 个；
   - 只出现在 `2019_05_09_mlms003` 和 `2019_05_09_bm1s007`；
   - 尺寸恒为 `wid=0.6, len=1.7`；
   - 该尺寸与 `class=80` cyclist/bicycle-like 目标一致。
4. 抽样相机图显示相关帧中确实存在自行车/骑行者目标。

## 对 D1A 的处理建议

1. 做 target/background mask sanity 时，先不依赖细分类，按 objectness 处理所有合法目标。
2. 如果需要类别统计，把 `class=1` 映射为 `cyclist_alias` 或直接并入 `cyclist`。
3. 保留原始 class id，不要改写原始 label 文件。
4. 在 manifest 或 loader 的 label map 中显式写：

```python
GAO77_LABEL_MAP = {
    0: "person",
    1: "cyclist_alias_or_bicycle",
    2: "car",
    3: "motorbike",
    5: "bus",
    7: "truck",
    80: "cyclist",
}
```

## 风险

官方 README 未明示 `class=1`，所以它只能作为数据审计推断。D1A 阶段可以这么处理；正式论文或公开数据说明里不能直接声称官方定义为 cyclist。
