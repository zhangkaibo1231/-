import csv

with open('euler.csv', 'r') as inp, open('simple_euler.csv', 'w', newline='') as out:
    writer = csv.writer(out)
    for i, row in enumerate(csv.reader(inp)):
        if i % 5 == 0:  # 如果你想隔两行保留一行，可以将这里改为 if i % 3 == 0
            writer.writerow(row)