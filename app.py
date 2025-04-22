import os
import sys
import argparse
import requests

API_BASE = 'https://api.github.com'


def get_repos(session, affiliation):
    repos = []
    page = 1
    while True:
        resp = session.get(f'{API_BASE}/user/repos', params={
            'affiliation': affiliation,
            'per_page': 100,
            'page': page
        })
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos


def get_branches(session, owner, repo):
    branches = []
    page = 1
    while True:
        resp = session.get(f'{API_BASE}/repos/{owner}/{repo}/branches', params={
            'per_page': 100,
            'page': page
        })
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        branches.extend(data)
        page += 1
    return branches


def get_commits(session, owner, repo, branch):
    commits = []
    page = 1
    while True:
        resp = session.get(
            f'{API_BASE}/repos/{owner}/{repo}/commits',
            params={'sha': branch, 'per_page': 100, 'page': page}
        )
        resp.raise_for_status()
        data = resp.json()
        if not data:
            break
        commits.extend(data)
        page += 1
    return commits


def main():
    parser = argparse.ArgumentParser(
        description='Export all GitHub commits from all repos and branches into a text file.'
    )
    parser.add_argument('--token', help='GitHub personal access token',
                        default=os.getenv('GITHUB_TOKEN'))
    parser.add_argument('--affiliation', help='Repo affiliation: owner,collaborator,organization_member',
                        default='owner,collaborator')
    parser.add_argument('--output', help='Output text file path', default='commits.txt')
    args = parser.parse_args()

    if not args.token:
        print('Error: GitHub token not provided. Use --token or set GITHUB_TOKEN env var.', file=sys.stderr)
        sys.exit(1)

    session = requests.Session()
    session.headers.update({'Authorization': f'token {args.token}', 'Accept': 'application/vnd.github.v3+json'})

    print('Fetching repositories...')
    repos = get_repos(session, args.affiliation)
    print(f'Found {len(repos)} repos.')

    with open(args.output, 'w', encoding='utf-8') as f:
        for repo in repos:
            owner = repo['owner']['login']
            name = repo['name']
            f.write(f'{owner}/{name}\n')
            print(f'Processing {owner}/{name}...')

            branches = get_branches(session, owner, name)
            for br in branches:
                br_name = br['name']
                f.write(f'    {br_name}\n')
                print(f'  Branch: {br_name}')
                commits = get_commits(session, owner, name, br_name)
                last_author = None
                for c in commits:
                    commit = c.get('commit', {})
                    author = commit.get('author', {}).get('name')
                    date = commit.get('author', {}).get('date')
                    message = commit.get('message', '').replace('\n', ' ')
                    if author != last_author:
                        f.write(f'        {author}\n')
                        last_author = author
                    f.write(f'            {date} {message}\n')

    print(f'All commits written to {args.output}')


if __name__ == '__main__':
    main()
