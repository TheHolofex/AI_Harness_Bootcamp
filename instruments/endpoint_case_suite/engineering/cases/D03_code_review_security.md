# D03 — Security smell in snippet

## Input

```python
# deploy.py (draft)
import os, requests

API_KEY = "sk-live-91f3SUPERSECRET"
def notify(msg):
    print("key prefix", API_KEY[:12])
    requests.post(
        "https://hooks.example.com/deploy",
        json={"msg": msg, "auth": API_KEY},
    )
```

## Task

1) State the issues. 2) Severity. 3) Exact remediation steps for a team that already leaked this pattern into git history.
