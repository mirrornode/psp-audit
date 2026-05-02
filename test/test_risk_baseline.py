from src.psp.risk.engine import baseline_findings

def test_baseline_findings_present():
    findings = baseline_findings()
    assert len(findings) >= 1
    assert findings[0]["severity"] in {"High", "Medium", "Low", "Info"}
