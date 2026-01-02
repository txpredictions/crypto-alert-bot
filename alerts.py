import json
import os

ALERT_FILE = "data/alerts.json"

os.makedirs("data", exist_ok=True)

def load_alerts():
    if not os.path.exists(ALERT_FILE):
        return {}
    with open(ALERT_FILE, "r") as f:
        return json.load(f)

def save_alerts(alerts):
    with open(ALERT_FILE, "w") as f:
        json.dump(alerts, f, indent=2)

def add_alert(user_id, coin, target):
    alerts = load_alerts()
    alerts.setdefault(str(user_id), {})
    alerts[str(user_id)][coin] = target
    save_alerts(alerts)

def delete_alert(user_id, coin):
    alerts = load_alerts()
    alerts.get(str(user_id), {}).pop(coin, None)
    save_alerts(alerts)
