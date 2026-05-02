import json
from pathlib import Path

def test_incident_payload_shape():
    data = json.loads(Path("payloads/incident_report_example.json").read_text())
    assert data["schema_version"] == 1
    assert set(data.keys()) >= {"Changed", "Risky", "Recoverable", "NextSteps"}
