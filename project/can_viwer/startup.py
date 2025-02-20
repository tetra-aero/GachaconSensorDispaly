import subprocess
import os


def run_command(command):
    try:
        # コマンドを実行
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"{command[1]} Success! : {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"{command[1]} Error:{command[1]}  {e.stderr}")

def run_pycommand(command):
    for script in command:
        log_file = f"{script}.log"
        print(f"Starting: {script}, logging to {log_file}")
        with open(log_file, 'w') as log:
            subprocess.Popen(['sudo', 'python3', script], stdout=log, stderr=log)

# CANインターフェースを設定
commands = [
    ['sudo', 'mkdir', '-p', '/mnt/ramdisk'],
    ['sudo', 'mount', '-t', 'tmpfs', '-o', 'size=128m', 'tmpfs', '/mnt/ramdisk']
]
for command in commands:
    run_command(command)


# 現在のディレクトリを取得
mydir = os.getcwd()

pycommand = [
    ['server.py'],
    ['gachacon_driver.py'],
]


for command in pycommand:
    run_pycommand(command)
