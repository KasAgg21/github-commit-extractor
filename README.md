# GitHub Commit Exporter

This Python script exports all commits from all repositories and their respective branches for an authenticated GitHub user into a text file.

It uses GitHub's REST API v3 and requires a personal access token for authentication.

## Features

- Export commits from all repositories you own or collaborate on
- Traverse all branches in each repository
- Save commit metadata (author, date, message) to a structured text file
- Automatic pagination support for large repos and many commits

## Requirements

- Python 3.6+
- `requests` library

Install dependencies:

```bash
pip install requests
```

## Authentication

You need a GitHub Personal Access Token (PAT) with access to your repositories.

Set it via an environment variable:

```bash
export GITHUB_TOKEN=your_token_here
```

Or pass it directly as a flag when running the script.

## Usage

```bash
python github_commit_exporter.py --token YOUR_GITHUB_TOKEN --affiliation owner,collaborator --output commits.txt
```

### Arguments

| Flag           | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `--token`      | GitHub Personal Access Token. Can also be set via `GITHUB_TOKEN` env var.   |
| `--affiliation`| Comma-separated values: `owner`, `collaborator`, `organization_member`.     |
| `--output`     | Output file to save commit data (default is `commits.txt`).                  |

## Output Format

The output text file is structured as:

```
owner/repo-name
    branch-name
        author-name
            2024-04-25T12:34:56Z Commit message summary
```

