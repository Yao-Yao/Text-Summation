# Text-Summation (文本摘要提取)

本项目实现了一个基于 TF-IDF 评分和长度缩放（Scaling）的文本摘要提取系统。它可以处理文档集，生成词汇表，并对文章中的句子进行排序以提取摘要。

## 环境要求

- **Python 2.x**: 本项目使用了 Python 2 特有的语法和库（如 `basestring`, `unicode`, `reload(sys)` 等）。

## 项目结构

- `article/`: 存放待处理的原始文档集（.txt 格式）。
- `article_rankscale/`: 存放处理后按重要性排序的句子。
- `basicmethods.py`: 基础方法库，包含文件遍历、编码转换（utf-8）等工具。
- `langmodel.py`: 语言模型，支持一元（Unigram）或二元（Bigram）模型分词。
- `buildvocab.py`: 生成词汇表，计算词频（TF）和文档频率（DF），并序列化为 Pickle 文件。
- `rankscale.py`: 对句子进行 TF-IDF 评分并进行长度缩放，最后输出排序后的摘要。
- `getsummary.py`: 提供给 Web 应用调用的接口。

## 使用方法

### 1. 准备数据
在 `article/` 目录下放置你的文档集。

### 2. 构建词汇表
运行 `buildvocab.py` 生成词汇表和频率统计：
```bash
python buildvocab.py
```
执行后会生成：
- `vocabulary.pickle` / `vocab_df.pickle`: 序列化的数据文件。
- `vocabulary.txt` / `vocab_df.txt`: 排序后的可读文本文件。

### 3. 生成摘要排序
运行 `rankscale.py` 对句子进行排序：
```bash
python rankscale.py
```
执行后，排序后的结果将保存在 `article_rankscale/` 目录下。

## API 调用

如果你想在 Web 应用或其他程序中调用摘要功能，可以使用 `getsummary.py` 中的接口：

```python
from getsummary import get_summary

# u_title: 文章标题
# u_content: 文章内容
summary = get_summary(u_title, u_content)
```

## 核心算法说明

1. **TF-IDF 评分**: 基于构建好的语料库计算每个词的权重。
2. **长度缩放 (Scale)**: 为了平衡长短句的权重，系统会对分值进行缩放处理。
3. **排序**: 根据最终得分对文章句子进行降序排列，得分越高越适合作为摘要。
