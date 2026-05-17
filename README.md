# IEEE LaTeX Writer Open

面向 IEEE、RA-L、T-RO、T-AC、ICRA、IROS、RSS、CoRL 等机器人、强化学习、控制与智能系统论文的 Codex Skill。

它不仅处理 IEEE LaTeX 格式，还帮助完善研究叙事、贡献逻辑、双盲匿名、实验严谨性、BibTeX 清洗、审稿回复和投稿前静态审计。

英文版见 [READMEEN.md](READMEEN.md)。

## 功能

- IEEEtran 论文写作、润色、重构与投稿前检查
- 机器人、强化学习、控制、智能系统等领域的论文策略与符号规范
- RA-L/T-RO/T-AC/ICRA/IROS/RSS/CoRL 等 venue-aware 写作适配
- 双盲评审匿名化检查，包括作者、机构、资助号、自引和实验室特征泄露
- Response Letter 工作流，支持审稿意见逐条映射到修改稿
- BibTeX 文献库清洗，包括专有名词大小写保护、冗余字段清理和 IEEE 期刊缩写
- 静态审计脚本，用于检查常见 LaTeX、引用、图片、编码、单位和格式风险

## 安装

将仓库克隆到 Codex skills 目录：

```bash
git clone https://github.com/YOUR-USER/ieee-latex-writer.git ~/.codex/skills/ieee-latex-writer
```

或使用支持 Agent Skills 的 CLI 安装：

```bash
npx skills add https://github.com/YOUR-USER/ieee-latex-writer --agent codex --yes
```

将 `YOUR-USER` 替换为实际 GitHub 用户名或组织名。

## 使用

示例提示：

```text
Use $ieee-latex-writer to strengthen the research narrative, experiments, and LaTeX of my IEEE robotics paper.
```

也可以用于：

```text
Use $ieee-latex-writer to audit my RA-L paper for double-blind review.
```

```text
Use $ieee-latex-writer to clean my BibTeX file and check IEEE formatting risks.
```

## 仓库内容

- `SKILL.md`：核心 Skill 指令与触发描述
- `agents/openai.yaml`：Skill UI 元数据
- `references/`：IEEE 写作、LaTeX 工作流与审稿回复参考
- `assets/minimal-ieee-paper.tex`：轻量 IEEEtran 起始模板
- `scripts/audit_ieee_latex.py`：IEEE LaTeX 静态审计脚本

## 静态审计

运行：

```bash
python scripts/audit_ieee_latex.py path/to/main.tex
```

审计脚本会检查常见风险，例如 IEEEtran 类使用、危险宏包、未解析引用、缺失图片、caption/label 顺序、双盲身份泄露、中文/全角标点、百分号与单位格式、公式环境中的叙述性文本，以及脏 BibTeX 字段。

该脚本不能替代官方 IEEE Template Selector、IEEE LaTeX Analyzer、Reference Preparation Assistant、PDF Checker 或目标 venue 的投稿说明。

## 许可

MIT
