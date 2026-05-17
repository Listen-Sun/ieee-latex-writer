# IEEE LaTeX Writer Open

面向 Codex 的 IEEE LaTeX 论文写作技能，适用于 IEEEtran 期刊、会议、Letters、Magazine 以及常见 IEEE 风格投稿流程。

它不只是格式模板助手，也覆盖研究叙事、贡献凝练、双盲匿名检查、实验严谨性、BibTeX 清理、审稿回复和投稿前静态审查。机器人、强化学习、控制和智能系统是增强模块，但不是唯一适用范围。

English version: [READMEEN.md](READMEEN.md)

## 功能

- IEEEtran 论文起草、修订、重构和投稿前检查
- 面向 IEEE 多学科论文的研究叙事、贡献框架、实验逻辑和审稿人视角写作
- 机器人/RL/控制、计算机与智能系统、通信与信号处理、电力与能源系统等领域模块
- 适配 IEEE Transactions、Letters、Conference、RA-L、T-RO、T-AC、ICRA、IROS、RSS、CoRL 等场景
- 双盲匿名检查：作者、机构、基金、ORCID、自引和实验室识别信息
- Response Letter 工作流：逐条映射审稿意见、回复和稿件修改位置
- BibTeX 清理：大小写保护、冗余字段移除、IEEE 期刊会议名缩写
- IEEE LaTeX 静态审查脚本

## 安装

推荐把可编辑源码放在一个固定位置，然后把技能副本同步到当前工作区：

```text
<workspace>/.agents/skills/ieee-latex-writer
```

也可以直接克隆到 Codex skills 目录：

```bash
git clone https://github.com/Listen-Sun/ieee-latex-writer.git ~/.codex/skills/ieee-latex-writer
```

## 更新 Skill

如果你采用当前这种“桌面源码 + 工作区安装副本”的方式，在 PowerShell 中运行：

```powershell
cd C:\Users\sun\Desktop
git -C ieee-latex-writer pull
if (Test-Path .agents\skills\ieee-latex-writer) { Remove-Item -LiteralPath .agents\skills\ieee-latex-writer -Recurse -Force }
Copy-Item -LiteralPath ieee-latex-writer -Destination .agents\skills\ieee-latex-writer -Recurse -Force
```

如果你直接安装在 Codex skills 目录中，运行：

```bash
git -C ~/.codex/skills/ieee-latex-writer pull
```

如果你通过 Agent Skills CLI 安装，可以重新执行安装命令来刷新：

```bash
npx skills add https://github.com/Listen-Sun/ieee-latex-writer --agent codex --yes
```

## 使用

```text
Use $ieee-latex-writer to improve the research narrative, LaTeX structure, and submission readiness of my IEEE paper.
```

```text
Use $ieee-latex-writer to audit my IEEE paper for double-blind review.
```

```text
Use $ieee-latex-writer to clean my BibTeX file and check IEEE formatting risks.
```

## 目录

- `SKILL.md`: 技能核心说明和触发描述
- `agents/openai.yaml`: Codex/OpenAI 侧 UI 元数据
- `references/`: IEEE 写作、LaTeX 工作流和审稿回复参考
- `assets/ieee-official-templates/`: 官方 IEEEtran 模板和说明文件
- `scripts/audit_ieee_latex.py`: IEEE LaTeX 项目静态审查脚本
- `.codex-plugin/plugin.json`: 可选的插件式分发元数据

## 静态审查

```bash
python scripts/audit_ieee_latex.py path/to/main.tex
```

该脚本检查 IEEEtran 类、风险包、未解析引用、缺失图片、caption/label 顺序、双盲泄露、中文或全角标点、百分号和单位格式、数学环境中的 prose、BibTeX 脏字段等常见问题。

它不能替代官方 IEEE Template Selector、IEEE LaTeX Analyzer、Reference Preparation Assistant、PDF Checker 或目标 venue 的投稿说明。

## License

This project is licensed under the [MIT License](LICENSE).
