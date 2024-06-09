import csv
import glob
import sys
import os

# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取parament.py所在的目录
parent_dir = os.path.dirname(current_dir)
# 将parament.py所在的目录添加到sys.path
sys.path.append(parent_dir)
# 导入parament.py
from parament import Para_Mana

pm=Para_Mana()#参数


def process_file(input_txt, csv_writer, offsets):
    #去除以PAINT/COLOR开头的行的前后n行中以GOTO/开头的行
    with open(input_txt, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
        for i in range(len(lines)):
            lines[i] = lines[i].strip()  # 去除首尾空白
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith('PAINT/COLOR'):
                # 检查前后n行，如果以GOTO/开头就删除
                n=6
                for j in range(1, n + 1):
                    if i - j >= 0 and lines[i - j].startswith('GOTO/'):
                        lines.pop(i - j)
                        i -= 1
                    if i + j < len(lines) and lines[i + j].startswith('GOTO/'):
                        lines.pop(i + j)
            i += 1
        #如果当前行以'GOTO/'开头且前一行不以'RAPID'开头
        prev_line = ''
        for line in lines:
            if line.startswith('GOTO/') and not prev_line.startswith('RAPID'):
                data = line.split('/')[1]
                columns = data.split(',')
                if len(columns) == 6:
                    # 将前三列的坐标加上对应的偏移量
                    for i in range(3):
                        columns[i] = str(float(columns[i]) + offsets[i])
                    csv_writer.writerow(columns)
            prev_line = line

# 定义坐标偏移量(mm)
offsets = [pm.get_param('offset_x'), pm.get_param('offset_y'), pm.get_param('offset_z')]


with open('output.csv', 'w', newline='', encoding='utf-8') as outfile:
    csv_writer = csv.writer(outfile)

    # 获取当前目录下所有.txt文件
    files = glob.glob('*.txt')

    # 根据文件名ASCII码排序
    files.sort()

    # 依次处理每个文件
    for file in files:
        process_file(file, csv_writer, offsets)
        print(f"Processed file: {file}")


'''
def remove_last_lines(filename, num_lines):
    with open(filename, 'r', newline='', encoding='utf-8') as infile:
        lines = infile.readlines()
    # 删除最后 num_lines 行
    del lines[-num_lines:]
    with open(filename, 'w', newline='', encoding='utf-8') as outfile:
        outfile.writelines(lines)

# 删除输出的csv文件的后m行
m=20
remove_last_lines('output.csv', m)  #
'''

