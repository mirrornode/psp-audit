from src.psp.cli.audit import run_audit

def test_owner_repo_validation():
    try:
        run_audit("invalid")
        assert False
    except ValueError:
        assert True

def test_valid_audit_payload():
    payload = run_audit("Acme/stellar")
    assert payload["schema_version"] == 1
    assert payload["owner"] == "Acme"
    assert payload["repo"] == "stellar"
