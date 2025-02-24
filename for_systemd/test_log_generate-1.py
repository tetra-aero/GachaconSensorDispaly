# Ref, https://chatgpt.com/share/67bc6743-5270-800c-8fbc-e208aee203e3
import requests
import re

# ログファイルのURL
url = "https://raw.githubusercontent.com/tetra-aero/GachaconSensorDispaly/refs/heads/main/GACHACON_log/candump-2022-02-22_161128_test03-04-1.log"

# URLからログファイルを取得
response = requests.get(url)
if response.status_code != 200:
    print("ログファイルの取得に失敗しました。")
    exit()

# 対象となる文字列
search_codes = ["000020", "000013", "000022"]

# 4桁のデータを8桁に拡張する関数
def expand_data(match):
    data_4 = match.group(1)
    # ゼロ埋めして8桁にする
    return "#" + data_4.zfill(8)

# ログファイル内の各行を処理
for line in response.text.splitlines():
    # 対象の文字列が含まれる行のみ処理
    if any(code in line for code in search_codes):
        # 「000020」を含む行の場合、"#"以降の4桁のデータを8桁に拡張
        if "000020" in line:
            line = re.sub(r"#([0-9A-Fa-f]{4})", expand_data, line)
        print(line)
    


