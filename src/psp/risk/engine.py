RULES = [
    "pull_request_target",
    "unsafe_shell_event_payload",
    "mutable_action_tags",
    "missing_permissions_block",
    "broad_token_write_access",
]

def baseline_findings():
    return [{
        "id": "R-001",
        "description": "pull_request_target used in workflow",
        "severity": "High",
        "file": ".github/workflows/ci.yml",
        "line": 12,
        "remediation": "Use safer triggers and least-privilege permissions."
    }]
