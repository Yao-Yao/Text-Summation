1 使用方法：

在article目录下准备好文档集

运行build_vocab.py生成vocabulary，tf和df的，序列化成pickle文件
排序后输出的txt文件：vocabulary.txt和vocab_df.txt。

建立article_rankscale目录

运行rank_scale.py生成rank后的句子。
rank的过程：tfidf评分并scale，最后排序。

——————————————
2 python模块

basicmethods.py
列举指定目录下的所有文件路径list
将字符串转换成unicode编码（utf-8）

langmodel.py
语言模型，一元或二元模型

build_vocab.py
生成vocabulary，tf和df的

rank_scale.py
生成rank后的句子