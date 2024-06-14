import subprocess  #顺序执行程序文件
import sys


def run_script(script_path):
    print(f'正在运行: {script_path}')  # 添加这行来打印当前正在运行的脚本名称
    subprocess.check_call([sys.executable, script_path])

if __name__ == '__main__':
    result = run_script('../txt2csv/if_model_inspace.py')
    if result == "No":
        print("模型不完全在灵活工作空间，是否继续打印? y/n")
        choice = input().lower()
        if choice != 'y':
            print("已取消打印")
            sys.exit()
    run_script('2makepose.py')
    run_script('3vector.py')
    run_script('4simple_rdp.py')
    run_script('5simple2space.py')
    run_script('6if.py')
    run_script('angleshow.py')
    print("是否开始打印? y/n")
    choice = input().lower()
    if choice == 'y':
        run_script('gojoint.py')
    else:
        print("已取消打印")

