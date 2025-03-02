#!/usr/bin/env python3
"""
Script to create GitHub issues from markdown files.
"""

import os
import sys
import json
import requests
from pathlib import Path

# GitHub repository information
REPO_OWNER = "tetra-aero"
REPO_NAME = "GachaconSensorDispaly"
GITHUB_API_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"

def read_issue_file(filepath):
    """Read an issue markdown file and extract title and body."""
    with open(filepath, 'r') as file:
        content = file.read()
    
    lines = content.split('\n')
    title = lines[0].replace('# ', '')
    body = '\n'.join(lines[1:])
    
    return title, body

def create_github_issue(title, body, token):
    """Create a GitHub issue using the GitHub API."""
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
        print(f"Successfully created issue #{issue['number']}: {title}")
        return issue['html_url']
    else:
        print(f"Failed to create issue. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def main():
    """Main function to process all issue files and create GitHub issues."""
    if len(sys.argv) < 2:
        print("Usage: python create_github_issues.py <github_token>")
        sys.exit(1)
    
    token = sys.argv[1]
    
    # Find all issue markdown files
    issue_files = sorted(Path('.').glob('issue_*.md'))
    
    if not issue_files:
        print("No issue files found. Please make sure files named issue_*.md exist.")
        sys.exit(1)
    
    print(f"Found {len(issue_files)} issue files.")
    
    created_issues = []
    
    for issue_file in issue_files:
        print(f"Processing {issue_file}...")
        title, body = read_issue_file(issue_file)
        
        issue_url = create_github_issue(title, body, token)
        if issue_url:
            created_issues.append((title, issue_url))
    
    if created_issues:
        print("\nSummary of created issues:")
        for title, url in created_issues:
            print(f"- {title}: {url}")
    else:
        print("\nNo issues were created successfully.")

if __name__ == "__main__":
    main()
