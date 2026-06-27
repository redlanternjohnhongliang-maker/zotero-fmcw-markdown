# D1A Gao77 标签策略

生成时间：2026-06-26

## 适用范围

该文件用于 D1A Gao 77GHz Raw ADC fixed-PFA sanity。它只规定标签解释和统计口径，不启动 D1、不训练模型、不做 synthetic interference、不做 CFAR、不做 fixed-PFA threshold calibration。

当前 D1A 子集：

`G:\mineru_output\gao_77ghz_raw_adc\subset_d1a_v1`

引用核查文件：

`G:\mineru_output\refine-logs\D0B_CLASS1_SEMANTICS_CHECK.md`

## 标签映射

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

GAO77_CLASS_GROUP = {
    0: "pedestrian_like",
    1: "cyclist_like",
    2: "vehicle_like",
    3: "motorbike_like",
    5: "vehicle_like",
    7: "vehicle_like",
    80: "cyclist_like",
}
```

Objectness target classes：

```python
[0, 1, 2, 3, 5, 7, 80]
```

## `class=1` 处理

`class=1` 不是官方 README 明确定义的类别。D1A 暂按 `cyclist_alias_or_bicycle` 处理，并与 `class=80` 在类别统计中合并为 `cyclist_like`。

依据：

1. 本地数据审计；
2. 官方仓库 README 历史检查；
3. 抽样相机图检查；
4. `class=1` 的尺寸与 cyclist/bicycle-like 目标一致。

D1A 报告必须写明：

`class=1 is treated as cyclist-like for D1A sanity based on data audit and image inspection, not because it is explicitly defined in the official README.`

## 对 D1A 的影响

D1A 主任务不依赖细分类，target/background mask sanity 使用 objectness。也就是说，target mask 只关心合法目标区域，不做类别分类，所以把 `class=1` 合并为 cyclist-like 不会影响 objectness mask sanity。

如果 D1A 输出 per-class projection hit rate，必须同时输出：

- 原始 class id 统计；
- 合并后的 class group 统计。

原始 label 文件不得被改写。
