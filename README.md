# Duolingo French Cards Skill

把 Duolingo 法语 `Words` 页面截图整理成系统化背单词卡片的 Codex Skill。

这个 skill 适合把零散的 Duolingo 截图变成三份可复用学习资料：

- `duolingo-words.csv`：从截图中提取的法语单词和 Duolingo 英文释义
- `ipa-examples.csv`：补充法语 IPA 音标、例句、词性/用法、英文翻译、中文翻译
- `study-cards.txt`：可直接导入或复制使用的背单词卡片文本

## 适合哪些人

适合：

- 正在用 Duolingo 学法语的人
- 想把 Duolingo 里的法语单词系统整理出来的人
- 想按截图顺序生成可背诵、可复习的法语单词卡片的人
- 想同时获得法语音标、自然例句、中文解释和词性用法的人
- 想把碎片化学习记录变成长期可复习资料的人

不太适合：

- 学习的不是法语
- 只想做通用词典查询，而不是基于 Duolingo 截图整理
- 需要 100% 自动 OCR、完全不人工确认截图内容的场景

## 安装

### 方法一：克隆到 Codex skills 目录

在 PowerShell 中运行：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills"
cd "$env:USERPROFILE\.codex\skills"
git clone https://github.com/Yuting02/duolingo-french-cards-skill.git
```

安装后，新开一个 Codex 对话或重启 Codex，让 skill 被重新发现。

### 方法二：下载 ZIP

1. 打开仓库：<https://github.com/Yuting02/duolingo-french-cards-skill>
2. 点击 `Code` -> `Download ZIP`
3. 解压后，把文件夹命名为 `duolingo-french-cards-skill`
4. 放到：

```text
C:\Users\你的用户名\.codex\skills\duolingo-french-cards-skill
```

macOS / Linux 对应路径通常是：

```text
~/.codex/skills/duolingo-french-cards-skill
```

## 如何使用

### 1. 准备截图

建议建立一个工作目录，例如：

```text
Duolingo-momo-word/
  screenshot/
    001.jpg
    002.jpg
  outputs/
```

把 Duolingo 法语 `Words` 页面截图放进 `screenshot/` 文件夹。

截图建议：

- 尽量截完整的单词卡片
- 保留法语单词和下面的英文释义
- 多张截图之间可以有少量重叠，skill 会按规则去重
- 如果文件名是随机 hash，Codex 会优先参考创建时间和截图滚动顺序

### 2. 在 Codex 中调用 skill

可以直接说：

```text
用 $duolingo-french-cards-skill 根据 screenshot 生成背单词卡片
```

或者更具体一点：

```text
用 $duolingo-french-cards-skill 处理这个目录里的 Duolingo 法语截图：
C:\Users\你的用户名\Desktop\Duolingo-momo-word
请生成 duolingo-words.csv、ipa-examples.csv 和 study-cards.txt
```

### 3. 输出文件

skill 会生成：

```text
outputs/duolingo-words.csv
outputs/ipa-examples.csv
outputs/study-cards.txt
```

最终卡片格式类似：

```text
[P#H1#courriel]
---
courriel

[ku.ʁjɛl]

✅J'envoie un courriel au professeur.
-- I send an email to the teacher.
⭐名词 阳性 un courriel
-- email; 电子邮件
*****
```

## 输出流程

### 第一步：截图提取

从 Duolingo 截图中提取：

```csv
法语单词,英文翻译
```

规则：

- 黑色粗体文字作为法语单词
- 灰色文字作为英文翻译
- 保留截图中的原始顺序
- 重复单词只保留第一次出现
- 被遮挡或看不清的内容不会强行猜测

### 第二步：补充学习信息

生成：

```csv
法语单词,法语英标,例句,词性/用法,英文翻译,中文翻译
```

补充内容包括：

- 法语 IPA 音标
- 自然、简短、适合初学者的法语例句
- 英文例句翻译
- 中文词性/用法说明
- 简短英文释义
- 中文翻译

### 第三步：生成背单词卡片

根据 `ipa-examples.csv` 生成 `study-cards.txt`。

仓库内置脚本可以稳定渲染卡片：

```powershell
python scripts/render_cards.py --input outputs/ipa-examples.csv --output outputs/study-cards.txt
```

也可以校验输出：

```powershell
python scripts/validate_outputs.py --root .
```

## 更新 skill

如果你是通过 git clone 安装的，可以这样更新：

```powershell
cd "$env:USERPROFILE\.codex\skills\duolingo-french-cards-skill"
git pull
```

## 注意事项

- 这个 skill 主要面向 Duolingo 法语单词截图。
- 它会尽量保留 Duolingo 截图中的原始单词顺序。
- 如果截图底部被导航栏遮挡，只有在能从上下文或已有示例确认时才会补齐。
- 法语重音符号、音标和中文内容需要使用 UTF-8 保存。
- Windows PowerShell 如果显示乱码，不一定是文件坏了，通常是控制台编码问题。

## 仓库结构

```text
SKILL.md
agents/openai.yaml
references/workflow.md
references/enrichment-guidelines.md
references/card-format.md
scripts/render_cards.py
scripts/validate_outputs.py
```