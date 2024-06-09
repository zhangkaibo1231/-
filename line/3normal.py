import pandas as pd



# 读取CSV文件，告诉pandas没有标题
output = pd.read_csv('outputmore.csv', header=None)

# 修改前三列数据，将数据除以1000，即由毫米改为米
output[[0, 1, 2]] = output[[0, 1, 2]] / 1000

# 对所有数据进行四舍五入，保留4位小数
output = output.round(4)

# 使用前一行的数据填充NaN值
output.ffill(inplace=True)

# 保存到新的CSV文件
output.to_csv('output_rounded.csv', index=False, header=False)