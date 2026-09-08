# Project Handoff

## Repository

`brodyZhao/my-research-project`

Remote：`https://github.com/brodyZhao/my-research-project.git`

## Current Branch

`codex/setup-github-workflow`

## Latest Commit

`2253478` (`chore: add GitHub collaboration workflow`; 后续交接文档更新提交为 `ce08d1c`)

## Current Goal

在当前项目建立 Codex、GitHub 与 ChatGPT Web 之间的稳定协作流程。

## Background

当前目录是空项目目录，没有现有业务源码。本次建立长期协作规则和交接模板，并将 `origin` 配置为用户提供的 GitHub 仓库，后续任务可直接在独立的 `codex/<task-name>` 分支上继续。

## Completed

- 创建 Codex 长期规则文件 `AGENTS.md`。
- 创建 Codex 与 ChatGPT Web 共用的任务交接文件 `HANDOFF.md`。
- 约定任务分支命名格式为 `codex/<task-name>`。
- 约定每次任务结束前更新交接信息、提交 commit，并在 remote 可用时 push。
- 已配置 `origin` 指向 `brodyZhao/my-research-project`。
- 已验证 push 请求可以到达 GitHub，但当前环境尚未完成 GitHub CLI/SSH 认证。

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
git --git-dir=work/git-metadata --work-tree=. diff --check
python3 -m compileall -q .
git --git-dir=work/git-metadata --work-tree=. remote -v
git --git-dir=work/git-metadata --work-tree=. push -u origin codex/setup-github-workflow
```

结果：Git 文档校验 PASS；`python3 -m compileall -q .` PASS；`origin` 已正确显示 fetch/push 地址；push 已连到 GitHub，但因缺少 Username/凭据失败；没有业务源码或自动化测试可运行。环境没有 `python` 命令，只有 `python3`。

## Known Issues

- 尚未验证 GitHub 凭据和目标仓库的 push 权限。
- Codex 运行环境没有 `gh`，也没有默认 SSH 公钥；网页版 ChatGPT 的 GitHub 授权不会自动提供本地 Git 凭据。
- 当前 Codex 沙箱拒绝在项目根目录创建 `.git`，标准 Git 仓库初始化因此受阻；需要在后续环境允许创建 `.git` 后重新执行 `git init`。
- 当前目录没有业务源码和自动化测试。

## Decisions Made

- 使用 `codex/setup-github-workflow` 作为本次协作流程初始化任务分支。
- 不猜测或绑定未知 GitHub 仓库。
- `work/` 和 `outputs/` 作为本地工作目录，不纳入项目代码提交。

## Questions for ChatGPT

1. 请确认当前 GitHub 账号对目标仓库具有 push 权限。
2. 请确认后续业务源码应放入当前目录，还是应切换到另一个已有项目目录。
3. 建立标准 `.git` 目录后，是否需要补充 CI、PR 模板或分支保护规则？

## Recommended Next Step

先在 Codex 运行环境完成 GitHub HTTPS/PAT 或 SSH 认证，再将当前分支 push 到 `origin`；随后由 ChatGPT Web 读取 `AGENTS.md` 和 `HANDOFF.md` 进行后续规划或代码审查。
