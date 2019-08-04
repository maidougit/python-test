import json

person = [
    {"name": "张三",
     "age": 12,
     "weight": 123
     },
    {
        "name": "李四",
        "age": 12,
        "weight": 123
    }
]

# 列表转换成json字符串
json_str = json.dumps(person)
print(type(json_str))
print(json_str)

# 写入json文件
with open(r'F:\python-test\file\json\json-test.json', 'w', encoding='utf-8') as fp:
    # fp.write(json_str)
    # 写文件
    json.dump(person, fp, ensure_ascii=False)

# 文件读取
json_str = '[{"name": "张三", "age": 12,"weight": 123 },{  "name": "李四",  "age": 12,   "weight": 123}]';
persons = json.loads(json_str);
print(type(persons))
print(persons)


with open(r'F:\python-test\file\json\json-test.json', 'r', encoding='utf-8') as fp:
    # fp.write(json_str)
    # 写文件
    list = json.load(fp)
    print(list)
