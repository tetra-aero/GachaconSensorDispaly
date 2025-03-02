# gachacon_driver.pyからハードコードされた値を削除する

## 課題の説明
gachacon_driver.pyスクリプトには、コードの柔軟性を低下させ保守を困難にする多くのハードコード値が含まれています。

## 特定された問題点
- JSONアウトプット用のハードコードされたファイルパス (`/mnt/ramdisk/outputv1.json`, `/mnt/ramdisk/output.json`)
- 最小限の説明しかないハードコードされたCAN ID
- ハードコードされたリレータイミング値 (`Wait_seconds_Supply_Relay_Precharge = 7`)
- ハードコードされたデバイス数 (`number_of_devices = 0x23`)
- 最小限の説明しかないハードコードされたCANメッセージデータ値

## 提案される改善点
- すべてのハードコード値をファイルの先頭に定数として移動する
- デプロイメント間で変更される可能性のある値のための設定システムを作成する
- 各値が表す内容に関する明確なドキュメントを追加する
- 関連する定数をグループ化する
- 特定の意味を持つ値に対しては列挙型（enum）の作成を検討する

## 技術的詳細
実装例：

```python
# CANインターフェース設定
CAN_INTERFACE = "vcan0"  # 本番環境では "can0" を使用

# デバイス設定
NUMBER_OF_DEVICES = 0x23  # 35台のデバイス
NUMBER_OF_ELEMENTS = NUMBER_OF_DEVICES * 4

# ファイルパス
OUTPUT_JSON_PATH = "/mnt/ramdisk/output.json"
OUTPUT_V1_JSON_PATH = "/mnt/ramdisk/outputv1.json"

# タイミングパラメータ
SUPPLY_RELAY_PRECHARGE_WAIT_SECONDS = 7
MOTOR_RELAY_PRECHARGE_WAIT_SECONDS = 7

# CANメッセージデータ値
CAN_VALUE_OFF = 0x00
CAN_VALUE_PRECHARGE = 0x80
CAN_VALUE_INTERMEDIATE = 0xC0
CAN_VALUE_MAIN_RELAY = 0x40

# CAN メッセージID（ドキュメント付き）
CAN_ID_MOTOR_BASE = 0x00001201  # モーター制御メッセージのベースID
CAN_ID_RELAY_1 = 0x00001221     # 500Aリレー1
CAN_ID_RELAY_2 = 0x00001222     # 500Aリレー2
CAN_ID_PATROL_LIGHT = 0x0000120F  # パトロールライト制御
```

## 優先度
中

## 影響
ハードコード値の削除により：
- コードがより保守しやすくなる
- 値を変更する際のエラーリスクを低減できる
- コードの可読性が向上する
- コードを詳細に調べることなく設定変更がより簡単に行える
- ドキュメント作成と知識移転の支援となる
