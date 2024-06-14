from parament import Para_Mana
pm=Para_Mana()#参数


def datamake(offsets, files):
    def process_file(input_txt, offsets):
        result = []
        with open(input_txt, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
            for i in range(len(lines)):
                lines[i] = lines[i].strip()  # 去除首尾空白
            i = 0
            while i < len(lines):
                line = lines[i]
                if line.startswith('PAINT/COLOR'):
                    # 检查前后n行，如果以GOTO/开头就删除
                    n = pm.get_param('m')
                    for j in range(1, n + 1):
                        if i - j >= 0 and lines[i - j].startswith('GOTO/'):
                            lines.pop(i - j)
                            i -= 1
                        if i + j < len(lines) and lines[i + j].startswith('GOTO/'):
                            lines.pop(i + j)
                i += 1
            prev_line = ''
            for line in lines:
                if line.startswith('GOTO/') and not prev_line.startswith('RAPID'):
                    data = line.split('/')[1]
                    columns = data.split(',')
                    if len(columns) == 6:
                        for i in range(3):
                            columns[i] = str(float(columns[i]) + offsets[i])
                        result.append(columns)
                prev_line = line
        return result

    files.sort()
    data = []
    for file in files:
        data.extend(process_file(file, offsets))
    return data









