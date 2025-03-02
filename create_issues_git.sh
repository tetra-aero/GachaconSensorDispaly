#!/bin/bash
# Script to prepare issue files for GitHub via git push with SSH

set -e

REPO_OWNER="tetra-aero"
REPO_NAME="GachaconSensorDispaly"
REPO_URL="git@github.com:${REPO_OWNER}/${REPO_NAME}.git"
BRANCH_NAME="issues-$(date +%Y%m%d-%H%M%S)"

# Check if we're already in a git repo
if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    echo "Error: Not in a git repository. Please run this script from within a git repository."
    exit 1
fi

echo "Preparing to create issues using Git..."

# Create a directory for the issues
ISSUES_DIR=".github/issues"
mkdir -p "$ISSUES_DIR"

# Copy all issue files to the .github/issues directory
for file in issue_*.md; do
    if [ -f "$file" ]; then
        cp "$file" "$ISSUES_DIR/"
        echo "Copied $file to $ISSUES_DIR/"
    fi
done

# Create a README file explaining what these files are for
cat > "$ISSUES_DIR/README.md" << EOF
# GitHub Issues

This directory contains Markdown files for issues that should be created in the GitHub repository.
Each file represents a separate issue.

These files were added automatically by a script.
EOF

# Create a new branch for the issues
git checkout -b "$BRANCH_NAME"

# Add the files
git add "$ISSUES_DIR"

# Commit the changes
git commit -m "Add issue files for gachacon_driver.py improvements"

echo -e "\nIssue files have been committed to the branch: $BRANCH_NAME"
echo "To push these issues to GitHub, run:"
echo "  git push origin $BRANCH_NAME"
echo ""
echo "After pushing, you can create a Pull Request at:"
echo "  https://github.com/$REPO_OWNER/$REPO_NAME/pull/new/$BRANCH_NAME"
echo ""
echo "You can then create issues on GitHub by following these steps:"
echo "1. Go to your repository on GitHub"
echo "2. Click on the 'Issues' tab"
echo "3. Click 'New issue'"
echo "4. Copy and paste the content from each of the issue files"

# Offer to push the branch now
read -p "Do you want to push the branch to GitHub now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Pushing branch $BRANCH_NAME to origin..."
    git push origin "$BRANCH_NAME"
    
    echo -e "\nYou can now create a Pull Request at:"
    echo "  https://github.com/$REPO_OWNER/$REPO_NAME/pull/new/$BRANCH_NAME"
fi
