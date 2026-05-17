# IEEE LaTeX Writer Open

面向 IEEE 多数学科论文写作的 Codex Skill，适用于 IEEEtran 期刊、会议、Letters、Magazine 以及常见 IEEE 风格投稿场景。

它不仅处理 LaTeX 格式，还帮助完善研究叙事、贡献逻辑、双盲匿名、实验严谨性、BibTeX 清洗、审稿回复和投稿前静态审计。机器人、强化学习、控制与智能系统是其中的增强模块，而不是唯一适用范围。

English version: [READMEEN.md](READMEEN.md)

## 功能

- IEEEtran 论文写作、润色、重构与投稿前检查
- 面向 IEEE 多领域的研究叙事、贡献组织、实验逻辑和 reviewer-aware 写作
- 领域模块：机器人/强化学习/控制、计算机与智能系统、通信与信号处理、电力与能源系统等
- Venue-aware 写作适配，包括 IEEE Transactions、Letters、Conference、RA-L/T-RO/T-AC/ICRA/IROS/RSS/CoRL 等
- 双盲评审匿名化检查，包括作者、机构、资助号、自引和实验室特征泄露
- Response Letter 工作流，支持审稿意见逐条映射到修改稿
- BibTeX 文献库清洗，包括专有名词大小写保护、冗余字段清理和 IEEE 期刊缩写
- 静态审计脚本，用于检查常见 LaTeX、引用、图片、编码、单位和格式风险

## 安装

将仓库克隆到 Codex skills 目录：

```bash
git clone https://github.com/Listen-Sun/ieee-latex-writer.git ~/.codex/skills/ieee-latex-writer
```

或使用支持 Agent Skills 的 CLI 安装：

```bash
npx skills add https://github.com/Listen-Sun/ieee-latex-writer --agent codex --yes
```

## 使用

示例提示：

```text
Use $ieee-latex-writer to improve the research narrative, LaTeX structure, and submission readiness of my IEEE paper.
```

也可以用于：

```text
Use $ieee-latex-writer to audit my IEEE paper for double-blind review.
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

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Listen-Sun/ieee-latex-writer&type=Date)](https://www.star-history.com/#Listen-Sun/ieee-latex-writer&Date)

## License

本项目采用 [MIT License](LICENSE)。
