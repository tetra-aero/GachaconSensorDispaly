import paramiko
import logging
import time

# ログの設定
logging.basicConfig()
logging.getLogger("paramiko").setLevel(logging.INFO)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

hostname = "192.168.0.101"  # Data Logging PC, enp2s0
#hostname = "192.168.0.100"  # Data Logging PC, enp1s0
username = "tetra"
password = "tetra"

try:
    client.connect(hostname=hostname, username=username, password=password)
    print(f"{hostname}に接続しました。")
except paramiko.AuthenticationException:
    print("認証に失敗しました。ユーザー名とパスワードを確認してください。")
except paramiko.SSHException as ssh_exception:
    print(f"SSH接続エラー: {ssh_exception}")

try:
    # cansend can2 0000600F#00, change standby
    # cansend can2 0000600F#01, change supplying, prechage->intermediate->supplying
    # cansend can2 0000600F#04, change flying, prechage->intermediate->flying
    stdin, stdout, stderr = client.exec_command("cansend can2 0000600F#00")
    print("コマンド出力:")
    for line in stdout:
        print(line.strip())

    print("エラー出力:")
    for line in stderr:
        print(line.strip())
    
finally:
    stdout.close()
    stderr.close()
    stdin.close()
    client.close()  # 明示的にクローズする

# End of file
