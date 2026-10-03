# AutoFluent Skill for Codex

通过 Codex 操作 **Fluent 2023 R1**，同时打开可手动操作的 Fluent 原生窗口。

本仓库是 Codex skill，配合 [AutoFluent MCP](https://github.com/YangC1222/AutoFluent-) 使用。MCP 执行算例读写、参数修改、迭代和数据导出；skill 管理可见窗口启动、连接、状态检查和协作流程。Fluent 窗口独立于 Codex，不是嵌入聊天区域的视频界面。

## 安装

先配置 AutoFluent MCP 和本机 Fluent 2023 R1。使用已有 AutoFluent Python 环境，保持 `ansys-fluent-core==0.37.0`。

```powershell
git clone https://github.com/YangC1222/AutoFluent-skill.git
$skillDestination = Join-Path $env:USERPROFILE '.codex\skills\autofluent-gui'
if (Test-Path -LiteralPath $skillDestination) { throw '已有同名 skill，请先检查后再更新。' }
New-Item -ItemType Directory -Path $skillDestination | Out-Null
Copy-Item -Path '.\AutoFluent-skill\SKILL.md', '.\AutoFluent-skill\agents', '.\AutoFluent-skill\scripts', '.\AutoFluent-skill\references' -Destination $skillDestination -Recurse
```

自定义 `CODEX_HOME` 时使用该目录下的 `skills/autofluent-gui`。安装后新建 Codex 对话或重新加载技能。

## 使用

> 使用 $autofluent-gui 打开 Fluent 2023 R1 可见窗口，连接 AutoFluent，读取我指定的 case/data 并显示当前工况。

> 使用 $autofluent-gui 将入口速度设为 11 m/s，计算到稳态并检查质量、能量守恒，保存为新文件。

用户可在原生窗口查看网格、云图和残差，并在自动任务空闲时手动操作。请避免 GUI 与 Codex 同时修改参数。API 修改不会保证自动切换每个 GUI 面板。

## 文件与生命周期

- `SKILL.md`：Codex 工作流程。
- `scripts/launch_gui.py`：固定版本、可见 GUI 启动与连接文件生成。
- `references/setup.md`：依赖、手动连接与故障恢复。
- 启动结果只返回连接文件路径，不返回密码。运行文件保存在 MCP workspace 的 `.autofluent-gui/`。
- GUI 在启动脚本结束后继续运行。MCP 对这个会话的关闭操作仅断开连接；保存结果后可从 Fluent 窗口正常退出。

脚本支持 `--check`，仅检查环境，不占许可证。详细使用方式见 [setup](references/setup.md)。

## 新增四项能力

需要 AutoFluent MCP 0.2.0（28 个工具）：原生云图控制、可恢复批量管流工况、联合收敛检查、九列 Excel 与理论比较图。参数和限制见 [工作流指南](references/workflows.md)。

## 八个独立工程 skills（MCP 0.3.0）

| Skill | 功能 |
| --- | --- |
| [autofluent-preflight](skills/autofluent-preflight) | 网格、单位、材料、边界和模型预检查 |
| [autofluent-axial-heat](skills/autofluent-axial-heat) | 自动截面/壁面分段，局部 Tw/Tb/h/Nu 曲线 |
| [autofluent-pressure](skills/autofluent-pressure) | 静压差、总压损失、摩擦因子、泵功和可选 PEC |
| [autofluent-grid-study](skills/autofluent-grid-study) | 三套已有网格的求解编排、对比和适用条件内 GCI |
| [autofluent-correlations](skills/autofluent-correlations) | Dittus–Boelter、Gnielinski、层流、Hausen 及适用性 |
| [autofluent-monitor](skills/autofluent-monitor) | 本机监控页面、趋势、日志、取消及下载 |
| [autofluent-sweep](skills/autofluent-sweep) | 边界/恒物性参数的笛卡尔组合扫描和恢复 |
| [autofluent-report](skills/autofluent-report) | 有来源记录的 Word/PDF 与完整证据附件 |

保持根目录 autofluent-gui 的原安装方式不变。安装新增八项：

```powershell
python scripts/install_skills.py
```

默认安装至 `$CODEX_HOME/skills` 或 `~/.codex/skills`；已有目录会拒绝覆盖，检查后用 `--replace` 更新。每项可独立安装，其 SKILL.md 和 references/example.json 包含实际 MCP 参数。全部依赖 AutoFluent MCP 0.3.0；图表及报告需其 `[reports]` 可选依赖。

示例：`使用 $autofluent-axial-heat 对已收敛 pipe 算例输出五个轴向位置的局部换热曲线。`

限制：GCI 需真实三套可比网格，不会凭空生成；多参数求解当前针对恒物性稳态加热管流，几何扫描需要分别重划网格。监控页面是独立本机网页，不是 Fluent GUI 视频。更多验证见 MCP 仓库 docs/engineering.md。
