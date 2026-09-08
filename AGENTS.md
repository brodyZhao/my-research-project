# AGENTS.md

## Project Overview

当前仓库用于维护项目代码及 Codex、GitHub、ChatGPT Web 之间的协作状态。
当前目录尚未包含业务源码；后续加入源码后，应在本节补充项目目标和运行方式。

## Repository Structure

- `AGENTS.md`：Codex 长期需要遵守的项目规则。
- `HANDOFF.md`：Codex 与 ChatGPT Web 之间的任务交接和当前状态。
- `outputs/`：项目外部需要交付给用户的生成物，不作为临时工作区使用。
- `work/`：本地临时文件、分析脚本和中间产物，不提交到仓库。

## Development Rules

- 不直接在 `main` 或 `master` 上开发。
- 每个相对完整的任务使用 `codex/<task-name>` 分支。
- 修改前先阅读相关代码、`README.md`、`AGENTS.md` 和 `HANDOFF.md`。
- 尽量保持原项目代码风格。
- 不无理由进行大规模重构。
- 不随意删除原有功能。
- 不修改无关文件。
- 对关键修改添加必要注释。
- 不把密钥、令牌、数据集或本地环境配置提交到 Git。
- 不未经用户允许自动 merge 到 `main` 或 `master`。

## Testing

每次修改后，尽可能运行与修改相关的测试。

如果项目没有自动测试，则至少：

- 检查代码是否可以 import。
- 检查语法，优先运行 `python -m compileall .`。
- 对模型或数据流程检查关键 tensor shape、dtype、batch 和 device。
- 尽可能进行最小运行测试或 smoke test。
- 如果无法完成完整测试，需要在 `HANDOFF.md` 明确说明原因。

## Git Workflow

开始任务时：

1. 执行 `git status`、`git branch --show-current` 和 `git remote -v`。
2. 确认工作区没有误覆盖用户未提交的修改。
3. 新任务从 `main` 或 `master` 创建 `codex/<task-name>` 分支；已有任务继续使用对应分支。

完成相对完整的工作阶段时：

1. 检查 `git diff`，确认没有无关文件。
2. 执行 `git add` 和 `git commit`。
3. 如果已配置并确认是目标 GitHub 仓库，push 当前分支。
4. 更新 `HANDOFF.md`。
5. 再次提交并 push `HANDOFF.md`。

没有明确的 GitHub 地址时，不擅自添加 remote；没有 push 权限时，在 `HANDOFF.md` 记录阻塞原因。

## Handoff Rule

每次任务结束时必须更新 `HANDOFF.md`，并在交接中说明：

- 仓库名称；
- 当前分支；
- 最新 commit hash；
- 主要修改文件；
- 测试命令和测试结果；
- 遗留问题；
- 建议 ChatGPT Web 下一步检查的内容。
