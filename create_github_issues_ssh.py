#!/usr/bin/env python3
"""
Script to create GitHub issues from markdown files using GitHub CLI (gh),
which supports SSH key authentication.
"""

import os
import sys
import subprocess
from pathlib import Path

# GitHub repository information
REPO_OWNER = "tetra-aero"
REPO_NAME = "GachaconSensorDispaly"
REPO = f"{REPO_OWNER}/{REPO_NAME}"

def read_issue_file(filepath):
    """Read an issue markdown file and extract title and body."""
    with open(filepath, 'r') as file:
        content = file.read()
    
    lines = content.split('\n')
    title = lines[0].replace('# ', '')
    body = '\n'.join(lines[1:])
    
    return title, body

def create_github_issue_with_gh(title, body):
    """Create a GitHub issue using the GitHub CLI (gh)."""
    # Create a temporary file for the issue body
    temp_body_file = f"/tmp/issue_body_{os.getpid()}.md"
    with open(temp_body_file, 'w') as f:
        f.write(body)
    
    try:
        # Run gh issue create command
        cmd = [
            "gh", "issue", "create",
            "--repo", REPO,
            "--title", title,
            "--body-file", temp_body_file
        ]
        
        result = subprocess.run(
            cmd, 
            text=True, 
            capture_output=True,
            check=True
        )
        
        # Output will contain the URL of the created issue
        issue_url = result.stdout.strip()
        print(f"Successfully created issue: {title}")
        return issue_url
    except subprocess.CalledProcessError as e:
        print(f"Failed to create issue. Error: {e}")
        print(f"stderr: {e.stderr}")
        return None
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_body_file):
            os.remove(temp_body_file)

def check_gh_installed():
    """Check if GitHub CLI (gh) is installed."""
    try:
        subprocess.run(["gh", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def check_gh_auth():
    """Check if GitHub CLI (gh) is authenticated."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"], 
            capture_output=True, 
            text=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def main():
    """Main function to process all issue files and create GitHub issues."""
    # Check if gh is installed
    if not check_gh_installed():
        print("Error: GitHub CLI (gh) is not installed. Please install it first:")
        print("  https://cli.github.com/manual/installation")
        sys.exit(1)
    
    # Check if gh is authenticated
    if not check_gh_auth():
        print("Error: GitHub CLI (gh) is not authenticated. Please run:")
        print("  gh auth login")
        print("And follow the instructions to authenticate with SSH.")
        sys.exit(1)
    
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
        
        issue_url = create_github_issue_with_gh(title, body)
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
