#!/usr/bin/env python3
"""
Script to create issue files in a GitHub repository using GitPython.
This utilizes SSH authentication via your existing SSH keys.
"""

import os
import sys
import time
from pathlib import Path
import git  # Requires GitPython library

# GitHub repository information
REPO_OWNER = "tetra-aero"
REPO_NAME = "GachaconSensorDispaly"
REPO_URL = f"git@github.com:{REPO_OWNER}/{REPO_NAME}.git"

def read_issue_file(filepath):
    """Read an issue markdown file and extract title and body."""
    with open(filepath, 'r') as file:
        content = file.read()
    
    lines = content.split('\n')
    title = lines[0].replace('# ', '')
    body = '\n'.join(lines[1:])
    
    return title, body

def check_gitpython_installed():
    """Check if GitPython is installed."""
    try:
        import git
        return True
    except ImportError:
        return False

def main():
    """Main function to process all issue files and create a branch with issue files."""
    # Check if GitPython is installed
    if not check_gitpython_installed():
        print("Error: GitPython is not installed. Please install it first:")
        print("  pip install GitPython")
        sys.exit(1)
    
    # Check if we're in a git repository
    try:
        repo = git.Repo(os.getcwd(), search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError:
        print("Error: Not in a git repository. Please run this from within the git repository.")
        sys.exit(1)
    
    # Find all issue markdown files
    issue_files = sorted(Path('.').glob('issue_*.md'))
    
    if not issue_files:
        print("No issue files found. Please make sure files named issue_*.md exist.")
        sys.exit(1)
    
    print(f"Found {len(issue_files)} issue files.")
    
    # Create a timestamp for the branch name
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    branch_name = f"issues-{timestamp}"
    
    # Create a new branch for the issues
    current_branch = repo.active_branch.name
    print(f"Current branch: {current_branch}")
    print(f"Creating new branch: {branch_name}")
    
    try:
        # Create and check out new branch
        new_branch = repo.create_head(branch_name)
        new_branch.checkout()
        
        # Create a directory for the issues
        issues_dir = Path(".github/issues")
        issues_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all issue files to the .github/issues directory
        for issue_file in issue_files:
            target_file = issues_dir / issue_file.name
            with open(issue_file, 'r') as src_file:
                content = src_file.read()
            
            with open(target_file, 'w') as dest_file:
                dest_file.write(content)
            
            print(f"Copied {issue_file} to {target_file}")
        
        # Create a README file explaining what these files are for
        readme_content = """# GitHub Issues

This directory contains Markdown files for issues that should be created in the GitHub repository.
Each file represents a separate issue.

These files were added automatically by a script.
"""
        with open(issues_dir / "README.md", 'w') as readme_file:
            readme_file.write(readme_content)
        
        # Add the files to git
        repo.git.add(str(issues_dir))
        
        # Commit the changes
        repo.git.commit("-m", "Add issue files for gachacon_driver.py improvements")
        
        print(f"\nIssue files have been committed to the branch: {branch_name}")
        print("To push these issues to GitHub, run:")
        print(f"  git push origin {branch_name}")
        print("")
        print("After pushing, you can create a Pull Request at:")
        print(f"  https://github.com/{REPO_OWNER}/{REPO_NAME}/pull/new/{branch_name}")
        print("")
        print("You can then create issues on GitHub by following these steps:")
        print("1. Go to your repository on GitHub")
        print("2. Click on the 'Issues' tab")
        print("3. Click 'New issue'")
        print("4. Copy and paste the content from each of the issue files")
        
        # Ask if we should push the branch now
        push_now = input("Do you want to push the branch to GitHub now? (y/n) ")
        if push_now.lower() == 'y':
            print(f"Pushing branch {branch_name} to origin...")
            repo.git.push("origin", branch_name)
            
            print(f"\nYou can now create a Pull Request at:")
            print(f"  https://github.com/{REPO_OWNER}/{REPO_NAME}/pull/new/{branch_name}")
        
    except Exception as e:
        print(f"Error: {e}")
        # Switch back to the original branch if something went wrong
        repo.git.checkout(current_branch)
        sys.exit(1)

if __name__ == "__main__":
    main()
