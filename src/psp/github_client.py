import os
import base64
import time
import requests

GITHUB_API = "https://api.github.com"


class RateLimitError(Exception):
    def __init__(self, reset_at):
        self.reset_at = reset_at
        wait = max(0, int(reset_at - time.time()))
        super().__init__(
            f"GitHub rate limit exceeded. Resets in {wait}s. "
            f"Set GITHUB_TOKEN to get 5,000 requests/hr (unauthenticated: 60/hr)."
        )


class AuthError(Exception):
    pass


class NotFoundError(Exception):
    pass


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

        if resp.status_code == 401:
            raise AuthError(
                "GitHub token is invalid or expired. "
                "Check your GITHUB_TOKEN environment variable."
            )
        if resp.status_code == 403:
            reset_at = float(resp.headers.get("X-RateLimit-Reset", time.time() + 60))
            remaining = resp.headers.get("X-RateLimit-Remaining", "0")
            if remaining == "0":
                raise RateLimitError(reset_at)
            raise AuthError(
                "GitHub returned 403 Forbidden. "
                "The token may lack required scopes (needs: public_repo or repo)."
            )
        if resp.status_code == 404:
            raise NotFoundError(f"Not found: {path}")

        resp.raise_for_status()
        return resp.json()

    def rate_limit_status(self):
        data = self._get("/rate_limit")
        core = data["resources"]["core"]
        return {
            "limit": core["limit"],
            "remaining": core["remaining"],
            "reset_in": max(0, int(core["reset"] - time.time())),
            "authenticated": bool(self.token),
        }

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
        except NotFoundError:
            return []

    def get_file_content(self, owner, repo, path):
        data = self._get(f"/repos/{owner}/{repo}/contents/{path}")
        return base64.b64decode(data["content"]).decode()

    def get_commits(self, owner, repo, per_page=20):
        return self._get(f"/repos/{owner}/{repo}/commits", per_page=per_page)
