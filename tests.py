import pytest
from scripts import get_github_issues, create_github_issue, close_github_issue

github_token = "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"
repository_owner = "topq-practice"
repository_name = "api-practice"


@pytest.fixture
def initial_issues_list():
    return get_github_issues(github_token)


def test_get_all_open_issues():
    issues_list = get_github_issues(github_token)
    assert isinstance(issues_list, list)
    assert len(issues_list) > 0
    print(f"\nNumber of all open issues: {len(issues_list)}")


def test_get_issues_with_label():
    list_of_labels = ["practice1"]
    issues_list = get_github_issues(github_token, labels=list_of_labels)
    assert isinstance(issues_list, list)
    assert len(issues_list) > 0
    print(f"\nNumber of issues with label {list_of_labels}: {len(issues_list)}")


def test_create_new_issue():
    initiate_list = get_github_issues(github_token)
    issue_title = "Yosef's issue"
    issue_body = "This issue was created via REST API from Python by Yosef Cohen"
    issue_labels = ["practice1"]
    assignees = ["topq-practice"]

    json, status_code = create_github_issue(
        api_token=github_token,
        owner=repository_owner,
        repo=repository_name,
        title=issue_title,
        body=issue_body,
        labels=issue_labels,
        assignees=assignees,
    )
    updated_list = get_github_issues(github_token)

    assert status_code == 201
    assert len(updated_list) == len(initiate_list) + 1
    assert updated_list[0].number == json['number']
    print(f"\nNew issue created successfully. New issue number: {json['number']}")


def test_create_and_close_issue():
    initial_issues_list = get_github_issues(github_token)
    initial_list = initial_issues_list
    print("\nLen of initial list: " + str(len(initial_list)))

    issue_title = "Yosef's issue"
    issue_body = "This issue was created via REST API from Python by Yosef Cohen"
    issue_labels = ["practice1"]
    assignees = ["topq-practice"]

    # Create a new issue
    json, status_code = create_github_issue(
        github_token,
        repository_owner,
        repository_name,
        issue_title,
        body=issue_body,
        labels=issue_labels,
        assignees=assignees,
    )

    assert json is not None
    assert status_code == 201
    print(f"New issue created successfully. Issue number: {json['number']}")

    # Close the created issue
    json, status_code = close_github_issue(
        api_token=github_token,
        owner=repository_owner,
        repo=repository_name,
        issue_number=json['number'],
    )
    assert status_code == 200
    updated_issues_list = get_github_issues(github_token)
    assert len(updated_issues_list) == len(initial_list)
    print(f"Len of current issues after adding and closing: {len(updated_issues_list)}")
