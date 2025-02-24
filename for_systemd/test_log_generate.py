# Ref, https://chatgpt.com/share/67bc6743-5270-800c-8fbc-e208aee203e3
import requests

# ログファイルのURL
url = "https://raw.githubusercontent.com/tetra-aero/GachaconSensorDispaly/refs/heads/main/GACHACON_log/candump-2022-02-22_161128_test03-04-1.log"

# URLからログファイルを取得
response = requests.get(url)
if response.status_code != 200:
    print("ログファイルの取得に失敗しました。")
    exit()

# 各行をチェックして、指定の文字列が含まれる行を出力
search_codes = ["000020", "000013", "000022"]
for line in response.text.splitlines():
    if any(code in line for code in search_codes):
        print(line)
    

