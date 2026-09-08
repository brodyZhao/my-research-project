# Project Handoff

## Repository

未配置 GitHub remote（仓库 owner/name 待提供）。

## Current Branch

`codex/setup-github-workflow`

## Latest Commit

`2253478` (`chore: add GitHub collaboration workflow`)

## Current Goal

在当前项目建立 Codex、GitHub 与 ChatGPT Web 之间的稳定协作流程。

## Background

当前目录是空项目目录，没有现有业务源码、Git 仓库或 GitHub remote。本次先建立长期协作规则和交接模板，后续任务可直接在独立的 `codex/<task-name>` 分支上继续。

## Completed

- 创建 Codex 长期规则文件 `AGENTS.md`。
- 创建 Codex 与 ChatGPT Web 共用的任务交接文件 `HANDOFF.md`。
- 约定任务分支命名格式为 `codex/<task-name>`。
- 约定每次任务结束前更新交接信息、提交 commit，并在 remote 可用时 push。

## Files Changed

- `AGENTS.md`
- `HANDOFF.md`
- `.gitignore`

## Key Implementation Details

- `AGENTS.md` 覆盖项目规则、测试要求、分支策略、提交/push 流程和交接要求。
- `HANDOFF.md` 记录仓库、分支、commit、目标、修改文件、测试、遗留问题和下一步建议。
- 当前没有业务代码，因此没有算法、网络结构、接口或 tensor shape 变化。

## Tests Performed

已执行：

```bash
git status
git branch --show-current
git remote -v
```

结果：当前目录起初不是 Git 仓库；未配置 GitHub remote；没有业务源码可运行测试。

## Known Issues

- 尚未提供 GitHub 仓库地址，因此无法配置 remote 或 push。
- 当前 Codex 沙箱拒绝在项目根目录创建 `.git`，标准 Git 仓库初始化因此受阻；需要在后续环境允许创建 `.git` 后重新执行 `git init`。
- 当前目录没有业务源码和自动化测试。

## Decisions Made

- 使用 `codex/setup-github-workflow` 作为本次协作流程初始化任务分支。
- 不猜测或绑定未知 GitHub 仓库。
- `work/` 和 `outputs/` 作为本地工作目录，不纳入项目代码提交。

## Questions for ChatGPT

1. 请提供目标 GitHub 仓库的完整地址，以便配置 remote。
2. 请确认后续业务源码应放入当前目录，还是应切换到另一个已有项目目录。
3. 建立标准 `.git` 目录后，是否需要补充 CI、PR 模板或分支保护规则？

## Recommended Next Step

在允许根目录创建 `.git` 后，重新初始化仓库并配置明确的 GitHub remote；随后将本分支 push 到 GitHub，再由 ChatGPT Web 读取 `AGENTS.md` 和 `HANDOFF.md` 进行后续规划或代码审查。
