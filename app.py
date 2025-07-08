from flask import Flask, request, jsonify
from models import save_event, get_latest_events
from datetime import datetime

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json
    author = payload["sender"]["login"]
    timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")

    if event_type == "push":
        branch = payload["ref"].split("/")[-1]
        message = f'"{author}" pushed to \"{branch}\" on {timestamp}'
    elif event_type == "pull_request":
        from_branch = payload["pull_request"]["head"]["ref"]
        to_branch = payload["pull_request"]["base"]["ref"]
        action = payload["action"]
        if action == "closed" and payload["pull_request"]["merged"]:
            message = f'"{author}" merged branch \"{from_branch}\" to \"{to_branch}\" on {timestamp}'
        else:
            message = f'"{author}" submitted a pull request from \"{from_branch}\" to \"{to_branch}\" on {timestamp}'
    else:
        message = f'"{author}" performed {event_type} on {timestamp}'

    save_event({"event": message})
    return jsonify({"status": "success"}), 200

@app.route("/events", methods=["GET"])
def get_events():
    data = get_latest_events()
    return jsonify([e["event"] for e in data])

if __name__ == "__main__":
    app.run(debug=True, port=5000)
