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
