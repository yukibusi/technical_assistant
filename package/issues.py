import requests
from bs4 import BeautifulSoup

def _get_all_issues(repo):
    issues = []
    url = f"https://api.github.com/repos/{repo}/issues"
    params = {
        "state": "all",  # get all issues
        "per_page": 100, # Number of issues per page
        "page": 1
    }
    
    while True:
        response = requests.get(url, params=params)
        response.raise_for_status()
        page_issues = response.json()
        
        # Exclude pull requests
        page_issues = [issue for issue in page_issues if 'pull_request' not in issue]
        
        if not page_issues:
            break
        
        issues.extend(page_issues)
        params["page"] += 1
    
    return issues

def _scrape_comments(issue_url):
    comment_list = []
    response = requests.get(issue_url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        comments = soup.find_all('div', class_='timeline-comment')
        
        for comment in comments:
            comment_body = comment.find('td', class_='comment-body')
            if comment_body:
                comment_text = comment_body.get_text(strip=True)
                comment_list.append(comment_text)
        return comment_list
    else:
        print(f"Failed to retrieve page: {issue_url}")
        return []

def get_text_from_issue(repo):
    issues = _get_all_issues(repo)
    all_comments = []
    for issue in issues:
        issue_url = issue["html_url"]
        comments = _scrape_comments(issue_url)
        if comments:
            all_comments.append((comments, issue_url))
    return all_comments

if __name__ == "__main__":
    repo = "oreilly-japan/deep-learning-from-scratch"
    comments = get_text_from_issue(repo)
    for comment in comments:
        print('URL:', comment[1])
        print('Comments:')
        for text in comment[0]:
            print(text)
