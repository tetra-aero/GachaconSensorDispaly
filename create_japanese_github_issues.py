#!/usr/bin/env python3
"""
日本語のマークダウンファイルからGitHubイシューを作成するスクリプト。
"""

import os
import sys
import json
import requests
from pathlib import Path

# GitHubリポジトリ情報
REPO_OWNER = "tetra-aero"
REPO_NAME = "GachaconSensorDispaly"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

def read_issue_file(filepath):
    """イシューマークダウンファイルを読み込み、タイトルと本文を抽出します。"""
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    
    lines = content.split('\n')
    title = lines[0].replace('# ', '')
    body = '\n'.join(lines[1:])
    
    return title, body

def create_github_issue(title, body, token):
    """GitHub APIを使用してGitHubイシューを作成します。"""
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "title": title,
        "body": body
    }
    
    response = requests.post(GITHUB_API_URL, headers=headers, json=data)
    
    if response.status_code == 201:
        issue = response.json()
        print(f"イシューを正常に作成しました #{issue['number']}: {title}")
        return issue['html_url']
    else:
        print(f"イシュー作成に失敗しました。ステータスコード: {response.status_code}")
        print(f"レスポンス: {response.text}")
        return None

def main():
    """すべてのイシューファイルを処理してGitHubイシューを作成するメイン関数。"""
    if len(sys.argv) < 2:
        print("使用法: python create_japanese_github_issues.py <github_token>")
        sys.exit(1)
    
    token = sys.argv[1]
    
    # すべての日本語イシューマークダウンファイルを検索
    issue_files = sorted(Path('.').glob('issue_*_ja.md'))
    
    if not issue_files:
        print("イシューファイルが見つかりません。issue_*_ja.mdという名前のファイルが存在することを確認してください。")
        sys.exit(1)
    
    print(f"{len(issue_files)}個のイシューファイルが見つかりました。")
    
    created_issues = []
    
    for issue_file in issue_files:
        print(f"{issue_file}を処理中...")
        title, body = read_issue_file(issue_file)
        
        issue_url = create_github_issue(title, body, token)
        if issue_url:
            created_issues.append((title, issue_url))
    
    if created_issues:
        print("\n作成されたイシューの概要:")
        for title, url in created_issues:
            print(f"- {title}: {url}")
    else:
        print("\n正常に作成されたイシューはありません。")

if __name__ == "__main__":
    main()
