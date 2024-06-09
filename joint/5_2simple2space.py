import csv

# 打开csv文件并读取数据
with open('simple_vector.csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = [row for row in reader]

# 创建一个新的空数据列表
new_data = [[''] * len(data[0]) for _ in range(len(data))]

# 遍历数据，每隔5行保留一行，其余为为空白行
for i, row in enumerate(data):
    if i % 5 == 0:
        new_data[i] = row

# 输出新数据到CSV文件
with open('space_point.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(new_data)