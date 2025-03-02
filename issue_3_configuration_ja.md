# gachacon_driver.pyに設定管理機能を追加する

## 課題の説明
gachacon_driver.pyスクリプトは現在、柔軟な設定メカニズムがなくハードコードされた設定を使用しているため、異なる環境へのデプロイが困難です。

## 特定された問題点
- コメントアウトされた実際のCANインターフェース用の行: `#can_bus = can.interface.Bus(channel="can0", interface='socketcan')`
- 現在は仮想CANを使用: `can_bus = can.interface.Bus(channel="vcan0", interface='socketcan')`
- 本番環境と開発環境の間で簡単に切り替えるための設定メカニズムがない
- JSONアウトプット用のファイルパスのハードコード (`/mnt/ramdisk/outputv1.json`, `/mnt/ramdisk/output.json`)
- リレー操作のタイミング値がハードコードされている

## 提案される改善点
- 以下を制御するための設定ファイルまたはコマンドライン引数パーシングを作成する:
  - CANインターフェースの選択（仮想か実物か）
  - 出力ファイルパス
  - ロギングの詳細レベル
  - リレー操作のタイミングパラメータ
- 異なるデプロイメント環境に適応できる設定ローダーを実装する
- 環境固有のデフォルト設定（開発、テスト、本番）を追加する

## 技術的詳細
簡単な実装では、コマンドライン設定用のPythonのargparseモジュールと、より複雑な設定用のYAMLまたはJSON設定ファイルを使用できます:

```python
import argparse
import yaml

def parse_args():
    parser = argparse.ArgumentParser(description='Gachacon CANドライバー')
    parser.add_argument('--config', type=str, default='config.yaml', 
                      help='設定ファイルのパス')
    parser.add_argument('--can-interface', type=str, 
                      help='使用するCANインターフェース（設定ファイルより優先）')
    return parser.parse_args()

def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

# 使用例
args = parse_args()
config = load_config(args.config)
can_interface = args.can_interface or config.get('can_interface', 'vcan0')
```

## 優先度
中

## 影響
適切な設定管理を追加することで、以下のことが可能になります:
- 異なる環境間でのデプロイメントの簡易化
- 環境を変更する際のコード修正の必要性の低減
- 異なるハードウェアセットアップに対するシステムの柔軟性の向上
- 全体的な保守性の向上
