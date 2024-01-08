import json

agg_ops = ["", "AVG", "MAX", "MIN", "COUNT", "SUM"]
cond_ops = {0:'>', 1:'<', 2:'=', 3:'!='}
cond_conn_op = ['', 'and', 'or']

data = []
 
with open(r'data/esql/esql_test.txt', 'r', encoding='utf-8') as f:  
    for line in f:
        temp = json.loads(line)
        data.append(temp)

# 指定JSON文件路径
json_file_path = "data/esql/esql_table.json"

header_dict={}
# 读取JSON文件内容为字典
with open(json_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        json_obj = json.loads(line)
        tablename = json_obj["tablename"]
        header = json_obj["header"]
        header_dict[tablename] = header

final_data = []
for item in data:
    json_data = dict()
    sql = 'select '
    json_data['question'] = item['question']
    json_data['sql_id'] = item['sql_id']
    tablename = item["table_id"]
    headers = header_dict.get(tablename)
    if item['sql']['agg'][0] != 0:
        sql += agg_ops[item['sql']['agg'][0]] + '(' + headers[item['sql']['sel'][0]] + ')'
    else:
        sql += headers[item['sql']['sel'][0]]
    sql += ' from ' + item['table_id'] + ' where '
    for i in range(len(item['sql']['conds'])-1):
        condition = item['sql']['conds'][i]
        sql += headers[condition[0]] + cond_ops[condition[1]] + '\'' + condition[2] + '\''  + ' and '
    condition = item['sql']['conds'][-1]
    sql += headers[condition[0]] + cond_ops[condition[1]] + '\'' + condition[2] + '\''
    json_data['sql'] = sql
    json_data['headers'] = headers
    json_data['tablename'] = item['table_id']
    json_data['agg'] = agg_ops[item['sql']['agg'][0]]
    json_data['sel'] = headers[item['sql']['sel'][0]]
    condition = item['sql']['conds']
    wc,wo,wv = [],[],[]
    for i in condition:
        wc.append(headers[i[0]])
        wo.append(cond_ops.get(i[1]))
        wv.append(i[2])
    json_data['wc'] = wc
    json_data['wo'] = wo
    json_data['wv'] = wv
    json_data['wn'] = len(condition)
    print(sql)
    final_data.append(json_data)

out_file = open(r'data/esql/22.txt', 'w', encoding='utf-8') 
for line in final_data:
    json_str = json.dumps(line)
    out_file.write(json_str + '\n')
out_file.close()   