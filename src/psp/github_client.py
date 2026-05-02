import os
import base64
import requests

GITHUB_API = "https://api.github.com"


class GitHubClient:
    def __init__(self, token=None):
        self.token = token or os.environ.get("GITHUB_TOKEN")
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })
        if self.token:
            self.session.headers["Authorization"] = f"Bearer {self.token}"

    def _get(self, path, **params):
        url = f"{GITHUB_API}{path}"
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def get_repo(self, owner, repo):
        return self._get(f"/repos/{owner}/{repo}")

    def get_refs(self, owner, repo):
        return self._get(f"/repos/{owner}/{repo}/branches", per_page=100)

    def get_tags(self, owner, repo):
        return self._get(f"/repos/{owner}/{repo}/tags", per_page=100)

    def get_workflow_files(self, owner, repo):
        try:
            items = self._get(f"/repos/{owner}/{repo}/contents/.github/workflows")
            return [i for i in items if i["name"].endswith((".yml", ".yaml"))]
        except Exception:
            return []

    def get_file_content(self, owner, repo, path):
        data = self._get(f"/repos/{owner}/{repo}/contents/{path}")
        return base64.b64decode(data["content"]).decode()

    def get_commits(self, owner, repo, per_page=20):
        return self._get(f"/repos/{owner}/{repo}/commits", per_page=per_page)
