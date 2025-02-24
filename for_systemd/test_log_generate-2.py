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

# 対象となるコード群
search_codes = ["000020", "000013", "000022"]

def expand_to_little_endian(match):
    """マッチした16進数データを8桁にゼロ埋め後、2桁ずつ逆順にしてリトルエンディアン表現にする"""
    hex_data = match.group(1)
    # 4桁の場合は8桁にゼロ埋め（8桁の場合はそのまま）
    hex_data = hex_data.zfill(8)
    # 2桁ずつに分割
    byte_list = [hex_data[i:i+2] for i in range(0, 8, 2)]
    # バイト順を逆に（リトルエンディアン）
    little_endian = ''.join(reversed(byte_list))
    return "#" + little_endian

# 各行を処理
for line in response.text.splitlines():
    # 指定の文字列が含まれる行のみ対象とする
    if any(code in line for code in search_codes):
        # 000020を含む行の場合、"#"以降の16進数データを変換
        if "000020" in line:
            # 正規表現： "#" の直後に 4桁または8桁の16進数（4桁の場合はゼロ埋めして8桁にする）
            line = re.sub(r"#([0-9A-Fa-f]{4}(?:[0-9A-Fa-f]{4})?)", expand_to_little_endian, line)
        print(line)
    

