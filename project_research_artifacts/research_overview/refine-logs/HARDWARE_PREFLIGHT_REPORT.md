# HARDWARE_PREFLIGHT_REPORT

**Python**：`G:\Anaconda\envs\cnn_learn\python.exe`
**Python version**：3.9.24
**注意**：默认 `G:\Anaconda\python.exe` 未安装 PyTorch；本次 D1 使用 `cnn_learn` 环境。
**PyTorch available**：True
**PyTorch version**：1.12.0+cu113
**CUDA available in PyTorch**：True
**PyTorch CUDA version**：11.3
**nvidia-smi**：`NVIDIA GeForce GTX 1650, 4096 MiB, 1044 MiB, 581.80`
**NVIDIA driver / CUDA runtime**：Driver 581.80，nvidia-smi 显示 CUDA Version 13.0
**CPU**：Intel(R) Core(TM) i5-9300H CPU @ 2.40GHz
**RAM**：总内存约 31.92 GB，检查时空闲约 11.10 GB

## 数据发现

- 本地数值雷达数据文件采样数量：0
- 结论：未在 `G:/mineru_output` 下发现 `.npy/.npz/.mat/.h5/.pt` 等雷达 tensor 数据；`C:/Users/26978/Desktop/脚本文件` 主要是脚本和金融数据，也未发现雷达 tensor 数据。D1 使用合成 toy RD 数据验证指标链路。

## 样本规模估算

- RD tensor shape：`(1, 64, 128)`
- dtype：`float32`
- 单条 RD tensor 输入占用：0.0312 MiB
- dry-run batch=2 输入占用：0.0625 MiB，仅为输入张量，不含中间激活。

## Dry-Run

- conservative batch size：2
- num_workers：0
- mixed precision：False
- dry-run status：ok
- dry-run detail：`{"status": "ok", "device": "cuda", "input_shape": [2, 1, 64, 128], "output_shape": [2, 1, 64, 128], "loss": 0.033248480409383774, "grad_finite": true, "cuda_memory_allocated_mib": 0.18798828125, "cuda_memory_reserved_mib": 2.0}`

## 预判

- D1：本地机器足够完成。
- D2：simple FCN/AENN 小 batch overfit 可以本地先跑；建议 batch size 从 1 或 2 开始。
- 瓶颈预判：D1 不是瓶颈；D2 小 batch 的主要风险是 4GB 显存和数据 IO；真实数据一旦较大，CPU/RAM 数据加载也可能成为瓶颈。
- 后续 3 seeds、大 batch、长时间训练：GTX 1650 4GB 会非常吃紧，建议届时再租云 GPU。
