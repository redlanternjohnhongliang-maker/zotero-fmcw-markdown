# Gao 77GHz Raw ADC 数据下载与可用性检查报告

生成时间：2026-06-26 13:10  
当前数据根目录：`G:\mineru_output\gao_77ghz_raw_adc`

## 1. 本次执行范围

本次只执行数据下载前检查、官方入口可访问性检查和下载尝试。未启动 D1-D14，未训练模型，未做 synthetic interference injection，未做 CFAR，未做 fixed-PFA threshold calibration。

## 2. 本地目录

已创建当前工作区内的数据目录：

- `G:\mineru_output\gao_77ghz_raw_adc\downloads`
- `G:\mineru_output\gao_77ghz_raw_adc\raw`
- `G:\mineru_output\gao_77ghz_raw_adc\subset`
- `G:\mineru_output\gao_77ghz_raw_adc\reports`
- `G:\mineru_output\gao_77ghz_raw_adc\reports\figures`

## 3. 下载前检查

| 项目 | 结果 |
|---|---|
| G 盘剩余空间 | 约 658 GB |
| GitHub repo 是否可访问 | 是 |
| 官方 README 是否可读取 | 是 |
| Google Drive 入口是否在 README 中 | 是 |
| IEEE DataPort 入口是否在 README 中 | 是 |
| git | 已安装：`G:\Git\cmd\git.exe` |
| Python 环境 | `G:\Anaconda\envs\cnn_learn\python.exe` |
| gdown | 已安装到 `cnn_learn` 环境，版本 5.2.2 |

官方 GitHub 仓库：

`https://github.com/Xiangyu-Gao/Raw_ADC_radar_dataset_for_automotive_object_detection`

官方 README 已保存到：

`G:\mineru_output\gao_77ghz_raw_adc\downloads\README_github.md`

## 4. 下载尝试结果

### 4.1 Google Drive

来源：

`https://drive.google.com/file/d/1OfqXXgoFg6xRYZkRqPJye4cQ29Fomh3l/view?usp=sharing`

结果：失败。

具体原因：

- 使用 `gdown` 访问官方 Google Drive 链接时，无法取得公开下载 URL。
- `gdown` 返回提示：可能需要将文件权限改为 anyone with the link，或访问次数过多。
- 对同一文件 ID 做直接 HTTP 探测时，只返回 2.4 KB HTML 页面，不是数据压缩包。

日志：

- `G:\mineru_output\gao_77ghz_raw_adc\downloads\google_drive_download.log`
- `G:\mineru_output\gao_77ghz_raw_adc\downloads\google_drive_headers.txt`
- `G:\mineru_output\gao_77ghz_raw_adc\downloads\google_drive_probe.bin`

### 4.2 IEEE DataPort

来源：

`https://ieee-dataport.org/documents/raw-adc-data-77ghz-mmwave-radar-automotive-object-detection`

结果：无法直接下载。

具体原因：

- IEEE DataPort 页面可以访问。
- 页面显示数据文件为 `Automotive.zip`，大小 `14.71 GB`。
- 页面同时显示需要登录并具有 IEEE DataPort Subscription 才能访问数据文件。
- 当前未登录状态下没有可直接下载的数据文件链接。

页面快照：

`G:\mineru_output\gao_77ghz_raw_adc\downloads\ieee_dataport_page.html`

## 5. 原始文件与解压状态

| 项目 | 结果 |
|---|---|
| 是否成功下载 | 否 |
| 下载来源 | Google Drive 尝试失败；IEEE DataPort 需要登录/订阅 |
| 原始文件大小 | 未获得；DataPort 页面标称 `Automotive.zip` 为 14.71 GB |
| 解压后大小 | 未解压 |
| 解压目录 | `G:\mineru_output\gao_77ghz_raw_adc\raw`，当前为空 |
| 子集路径 | `G:\mineru_output\gao_77ghz_raw_adc\subset`，当前为空 |
| 子集帧数 | 0 |

## 6. 数据完整性检查状态

因为没有成功下载原始数据，以下检查无法执行：

| 检查项 | 状态 |
|---|---|
| sequence 名称 | 未获得 |
| radar_raw_frame 文件数量 | 未获得 |
| text_labels 文件数量 | 未获得 |
| `.mat` 与 `.csv` 是否按文件名对齐 | 未检查 |
| 随机读取 5 个 `.mat` | 未执行 |
| `.mat` 变量名 | 未获得 |
| raw ADC tensor shape | 未获得 |
| shape 是否接近 128 samples / 255 chirps / 4 receivers / 2 transmitters | 未验证 |
| 随机读取 5 个 `.csv` | 未执行 |
| 标签列是否为 uid, class, px, py, wid, len | 未验证 |
| 小子集目标类别统计 | 未获得 |
| px, py 合理性 | 未检查 |
| wid, len 是否为正数 | 未检查 |
| 空标签帧 | 未检查 |
| radar 有但 label 缺失 | 未检查 |
| label 有但 radar 缺失 | 未检查 |

## 7. 最小 radar processing smoke test 状态

因为没有 `.mat` raw ADC 文件，以下 smoke test 未执行：

| 检查项 | 状态 |
|---|---|
| 读取 raw ADC | 未执行 |
| TDM 虚拟阵列形成 | 未执行 |
| range FFT | 未执行 |
| Doppler FFT | 未执行 |
| range profile shape | 未获得 |
| RD map shape | 未获得 |
| range profile 可视化 | 未生成 |
| RD map 可视化 | 未生成 |
| 标签投影图 | 未生成 |

可视化目录已创建但当前为空：

`G:\mineru_output\gao_77ghz_raw_adc\reports\figures`

## 8. 是否足够进入 D1

当前不建议进入 D1。

阻塞点：

1. 没有成功下载官方数据压缩包；
2. 没有 `.mat` raw ADC 文件；
3. 没有 `.csv` 标签文件；
4. 无法验证 raw ADC shape；
5. 无法验证标签格式与 frame 对齐；
6. 无法生成 range profile / RD map。

## 9. 下一步建议

建议先手动解决官方数据访问问题，再继续：

1. 用浏览器登录 Google / IEEE DataPort，确认官方 Google Drive 文件是否能手动下载；
2. 如果 Google Drive 页面可以下载，把 `Automotive.zip` 保存到：  
   `G:\mineru_output\gao_77ghz_raw_adc\downloads`
3. 如果只能通过 IEEE DataPort 下载，需要登录有订阅权限的账号后下载官方 `Automotive.zip`；
4. 下载完成后，再继续执行解压、抽取一个 sequence 的前 500-1000 帧、数据完整性检查和最小 radar processing smoke test；
5. 只有当 `.mat` raw ADC 和 `.csv` 标签都可读取，并且能生成基础 range/RD 表示后，才进入 D1。

## 10. 简短结论

- Gao 77GHz 数据：未成功下载。
- 小子集：未生成。
- 本地机器：环境和空间足够，但目前没有数据可读。
- raw ADC shape：未验证。
- label：未验证。
- 是否建议进入 D1：否，先拿到官方数据包。
