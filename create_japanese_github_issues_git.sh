#!/bin/bash
# 日本語のイシューファイルをGitHubにアップロードするためのスクリプト

set -e

REPO_OWNER="tetra-aero"
REPO_NAME="GachaconSensorDispaly"
BRANCH_NAME="japanese-issues-$(date +%Y%m%d-%H%M%S)"

# Gitリポジトリ内にいるか確認
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    echo "エラー: Gitリポジトリ内ではありません。Gitリポジトリ内でこのスクリプトを実行してください。"
    exit 1
fi

echo "Gitを使用して日本語のイシューを作成する準備をしています..."

# イシュー用のディレクトリを作成
ISSUES_DIR=".github/japanese-issues"
mkdir -p "$ISSUES_DIR"

# すべての日本語イシューファイルを.github/japanese-issuesディレクトリにコピー
for file in issue_*_ja.md; do
    if [ -f "$file" ]; then
        cp "$file" "$ISSUES_DIR/"
        echo "$fileを$ISSUES_DIR/にコピーしました"
    fi
done

# これらのファイルが何のためのものかを説明するREADMEファイルを作成
cat > "$ISSUES_DIR/README.md" << EOF
# GitHub イシュー（日本語）

このディレクトリには、GitHubリポジトリに作成されるべきイシューのための日本語マークダウンファイルが含まれています。
各ファイルは別々のイシューを表しています。

これらのファイルはスクリプトによって自動的に追加されました。

イシューを作成するには：
1. GitHubのリポジトリページに移動
2. 「Issues」タブをクリック
3. 「New issue」をクリック
4. 各イシューファイルの内容をコピー＆ペースト
EOF

# イシュー用の新しいブランチを作成
git checkout -b "$BRANCH_NAME"

# ファイルを追加
git add "$ISSUES_DIR"

# 変更をコミット
git commit -m "gachacon_driver.py改善のための日本語イシューファイルを追加"

echo -e "\nイシューファイルがブランチにコミットされました: $BRANCH_NAME"
echo "これらのイシューをGitHubにプッシュするには、次のコマンドを実行してください:"
echo "  git push origin $BRANCH_NAME"
echo ""
echo "プッシュ後、以下のURLでプルリクエストを作成できます:"
echo "  https://github.com/$REPO_OWNER/$REPO_NAME/pull/new/$BRANCH_NAME"
echo ""
echo "その後、以下の手順でGitHub上でイシューを作成できます:"
echo "1. GitHubのリポジトリページに移動"
echo "2. 「Issues」タブをクリック"
echo "3. 「New issue」をクリック"
echo "4. 各イシューファイルの内容をコピー＆ペースト"

# 今すぐブランチをプッシュするか確認
read -p "今すぐブランチをGitHubにプッシュしますか？ (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "ブランチ $BRANCH_NAME を origin にプッシュしています..."
    git push origin "$BRANCH_NAME"
    
    echo -e "\n以下のURLでプルリクエストを作成できます:"
    echo "  https://github.com/$REPO_OWNER/$REPO_NAME/pull/new/$BRANCH_NAME"
fi
