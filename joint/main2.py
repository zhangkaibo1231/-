import subprocess  #顺序执行程序文件
import sys

def print_hi(name):
    print(f'Hi, {name}')

def run_script(script_path):
    print(f'正在运行: {script_path}')  # 添加这行来打印当前正在运行的脚本名称
    subprocess.check_call([sys.executable, script_path])

if __name__ == '__main__':
    print_hi('QUSTer')

    # 这些脚本将按顺序运行，一个完成后才开始下一个、、
    run_script('../txt2csv/1txt2csv.py')
    run_script('2makepose.py')
    run_script('3vector.py')
    run_script('4_2simple_rdp.py')
    run_script('5_2simple2space.py')
    run_script('6if.py')
    print("是否开始打印? y/n")
    choice = input().lower()
    if choice == 'y':
        run_script('gojoint.py')
    else:
        print("已取消打印")


