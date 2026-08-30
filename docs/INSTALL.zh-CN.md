# 安装并验证 CNS Skills

CNS Skills 是纯 Skills 插件，不需要 API Key 或额外账号。只有运行可选的
本地审计器时才需要 Python 3.9 及以上版本。

## ChatGPT 桌面端 / Codex

1. 添加仓库 marketplace：

   ```bash
   codex plugin marketplace add niuyupeng/CNS-Skills
   ```

2. 重启 ChatGPT 桌面端。
3. 打开 **Plugins Directory**，选择 **CNS Skills** 来源并安装
   **CNS Skills**。
4. 新建任务并测试：

   ```text
   使用 $cns-skills，根据给定证据审计这句合成文本。
   证据：一次体外实验。句子：“该平台能够推动临床转化。”
   ```

预期行为：Skill 应把句子收窄到已经观察到的体外结果，并明确体内表现和
临床效用尚未验证。

确认 marketplace 已加入：

```bash
codex plugin marketplace list
```

新版本发布后刷新 marketplace：

```bash
codex plugin marketplace upgrade cns-skills
```

随后重启桌面端，在插件详情页更新或重新安装。移除来源前，先在应用中卸载
或停用 CNS Skills，再运行：

```bash
codex plugin marketplace remove cns-skills
```

上述方式属于仓库直接分发；进入 universal Plugins Directory 仍需平台另行
审核。

## Claude Code

```bash
claude plugin marketplace add niuyupeng/CNS-Skills
claude plugin install cns-skills@cns-skills
```

重新加载并显式调用：

```text
/reload-plugins
/cns-skills:cns-skills
```

更新或卸载：

```bash
claude plugin marketplace update cns-skills
claude plugin uninstall cns-skills@cns-skills
claude plugin marketplace remove cns-skills
```

## 独立 Agent Skill

```bash
# ChatGPT 桌面端 / Codex
git clone https://github.com/niuyupeng/CNS-Skills.git ~/.agents/skills/cns-skills

# Claude Code
git clone https://github.com/niuyupeng/CNS-Skills.git ~/.claude/skills/cns-skills
```

通过 Git 克隆安装时，在仓库目录中运行 `git pull --ff-only` 即可更新。

## 验证可选本地审计器

在仓库根目录运行：

```bash
python scripts/cns_audit.py --version
python scripts/review_citation_audit.py --version
python scripts/review_search_audit.py --version
python scripts/title_audit.py --version
python scripts/check_invariants.py --version
python scripts/check_crossrefs.py --version
```

只能处理你有权处理的文件。JSON 报告需要对外分享时，应使用
`--shareable`；否则报告可能保留本地路径或稿件片段。

## 常见问题

- **已添加 marketplace 但看不到插件：**重启桌面端，打开 Plugins
  Directory，并切换到 CNS Skills 来源。
- **Claude 提示找不到插件：**运行
  `claude plugin marketplace update cns-skills` 后重新安装。
- **没有自动触发：**在 ChatGPT/Codex 中显式写 `$cns-skills`，或在
  Claude Code 中运行 `/cns-skills:cns-skills`。
- **审计器拒绝文件：**先取消 strict 参数查看诊断。诊断用于分诊，不是
  科学正确性的证明。

可复现的安装问题请提交到
[Bug Report](https://github.com/niuyupeng/CNS-Skills/issues/new?template=bug_report.yml)。
