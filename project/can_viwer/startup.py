import subprocess
import os
import datetime
import time
import threading


def run_command(command):
    try:
        # コマンドを実行
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"{command[1]} Success! : {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"{command[1]} Error:{command[1]}  {e.stderr}")

def run_pycommand(command):
    for script in command:
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{script}.log"
        print(f"Starting: {script}, logging to {log_file}")
        
        # Start process and capture its PID
        process = subprocess.Popen(['sudo', 'python3', script], 
                                  stdout=open(log_file, 'w'), 
                                  stderr=subprocess.STDOUT)
        
        # Start a monitoring thread for this log file
        monitor_thread = threading.Thread(
            target=monitor_log_size, 
            args=(log_file, process, script),
            daemon=True
        )
        monitor_thread.start()


def monitor_log_size(log_file, process, script_name):
    """Monitor log file size and rotate when it exceeds 100MB"""
    MAX_SIZE = 100 * 1024 * 1024  # 100MB in bytes
    
    while process.poll() is None:  # While process is still running
        try:
            # Check file size
            if os.path.exists(log_file) and os.path.getsize(log_file) > MAX_SIZE:
                # Create new log file with timestamp
                current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                new_log_file = f"{script_name}_{current_time}.log"
                
                # Close current log and open new one
                print(f"Log file {log_file} exceeded 100MB. Rotating to {new_log_file}")
                
                # Redirect process output to new log file
                new_log = open(new_log_file, 'w')
                
                # The tricky part: We can't easily redirect the output of a running process
                # Instead, we'll stop the current process and start a new one
                process.terminate()
                process.wait(timeout=5)
                
                # Start a new process with the same command but new log file
                new_process = subprocess.Popen(['sudo', 'python3', script_name],
                                              stdout=new_log,
                                              stderr=subprocess.STDOUT)
                
                # Update variables to monitor the new process and log file
                process = new_process
                log_file = new_log_file
                
            # Sleep for a while before checking again
            time.sleep(5)
        except Exception as e:
            print(f"Error monitoring log file {log_file}: {e}")
            time.sleep(30)  # Longer sleep if there was an error

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
