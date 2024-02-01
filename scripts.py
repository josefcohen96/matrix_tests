import requests
from typing import Tuple, Optional, List


class Issue:
    def __init__(self, number, url) -> None:
        self.number = number
        self.url = url


def get_github_issues(api_token: str, labels: Optional[List[str]] = None) -> list[Issue]:
    if not api_token:
        return "Not api token supply"
    url = "https://api.github.com/issues"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {api_token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    all_issues = []

    page = 1
    while True:
        params = {
            "page": page,
            "filter": "all",
            "labels": labels,
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        issues = response.json()
        if not issues:
            break  # No more issues, exit the loop

        all_issues.extend(issues)
        page += 1

    # Create a list of Issue objects
    issue_objects = []
    if not labels:
        for issue in all_issues:
            issue_objects.append(Issue(issue['number'], issue['url']))

        return issue_objects

    for issue in all_issues:
        if issue['labels'][0]['name'] == labels[0]:
            issue_objects.append(Issue(issue['number'], issue['url']))

    return issue_objects


def create_github_issue(api_token: str, owner: str, repo: str, title: str, body=None, assignee=None, milestone=None,
                        labels=None, assignees: list = None) -> Tuple[Optional[dict], int]:
    url = f"https://api.github.com/repos/{owner}/{repo}/issues"

    headers = {
        "Accept": "application/vnd.github.v3+json",  # Use the GitHub API v3
        "Authorization": f"Bearer {api_token}",
    }
    if assignee is not None:
        assignees[0] = assignee

    data = {
        "title": title,
        "body": body,
        "milestone": milestone,
        "labels": labels,
        "assignees": assignees,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        return response.json(), response.status_code

    else:
        return None


def close_github_issue(api_token: str, owner: str, repo: str, issue_number: str) -> Tuple[Optional[dict], int]:
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"Bearer {api_token}",
    }

    data = {
        "state": "closed",
        "state_reason": "not_planned",
    }

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"Issue #{issue_number} closed successfully.")
        return response.json(), response.status_code
    else:
        print(
            f"Failed to close issue #{issue_number}. Status code: {response.status_code}, Error message: {response.text}")

        return response.json(), response.status_code
