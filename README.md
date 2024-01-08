Code and datasets of our paper "A Question-aware Few-shot Text-to-SQL Neural Model for Industrial Databases"

Our code is based on PyTorch(1.8.1) and Transformers(4.21.0), and is identical with https://github.com/alibaba/AliceMind/tree/main/SDCUP in requirements.

## Data
The few-shot ESQL dataset are located in the "data/esql" directory.
Since the SMI-SQL dataset contains information about a large number of bridges in China, it is temporarily unable to open source the data. However, we can provide original case analyses below.  

## Model
#### Downloading Pretrained Model SDCUP
Please download pretrained model SDCUP first in http://alice-open.oss-cn-zhangjiakou.aliyuncs.com/SDCUP/sdcup_large_model.bin-60000.

#### Finetune
```
python -u train.py --seed 1 --bS 2 --tepoch 20 --lr 0.001 --lr_bert 0.00001 --table_bert_dir sdcup_large_model.bin-60000  --config_path ./models/bert_large_config.json --vocab_path ./models/google_zh_vocab.txt --data_dir ./data/esql
```

#### Case Analyses

The results of case analysis on the ESQL and SMI-SQL datasets

|Datasets | Models | Output SQL Statement |
|:--------------------:|:-------:|:-------:|
|ESQL |Golden Ans. |SELECT `分部` FROM table_1 WHERE `地区`!= “西部” AND `销售率`>“87.27%” |
|ESQL |SDCUP |SELECT `分部` FROM table_1 WHERE `地区`= “西部” AND `销售率`>“87.27%” |
|ESQL |Vicuna-13B |SELECT AVG(`销售率`) from table_1 where `分部` != “西部” AND `销售率` > “87.27” |
|ESQL |QAF-SQL |SELECT `分部` FROM table_1 WHERE `地区`!= “西部” AND `销售率`>“87.27%” |
|SMI-SQL |Golden Ans. |SELECT COUNT(`桥梁名称`) FROM cbms_bridge_all WHERE `桥梁位置`= “西夏区” |
|SMI-SQL |SDCUP |SELECT COUNT(`桥梁名称`) FROM cbms_bridge_all WHERE `桥梁位置`= “西夏区” AND `桥梁规模`= “西夏区” |
|SMI-SQL |Vicuna-13B |SELECT COUNT(*) FROM cbms_bridge_all WHERE 1=1 |
|SMI-SQL |QAF-SQL |SELECT COUNT(`桥梁名称`) FROM cbms_bridge_all WHERE `桥梁位置`= “西夏区” |

The results of error analysis on the ESQL and SMI-SQL datasets

| Datasets |   Models    |                     Output SQL Statement                     |
| :------: | :---------: | :----------------------------------------------------------: |
|   ESQL   | Golden Ans. | SELECT `工程规模` FROM table_2 WHERE `机构`= “东利金融” AND `净利润`> “636.2” |
|   ESQL   |   QAF-SQL   | SELECT COUNT(`工程规模`) FROM table_2 WHERE `机构`= “东利金融” AND `净利润`> “636.2” |
| SMI-SQL  | Golden Ans. | SELECT COUNT(`隧道名称`) FROM tunnel_basic WHERE `隧道长度`> “1000” AND `隧道长度`< “3000” |
| SMI-SQL  |   QAF-SQL   | SELECT COUNT(`隧道名称`) FROM tunnel_basic WHERE `隧道长度`= “1000到3000之间” |

