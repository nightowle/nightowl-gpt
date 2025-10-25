import os
from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"


def gh_headers():
    if not GITHUB_TOKEN:
        raise RuntimeError("GITHUB_TOKEN environment variable is not set")

    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }


@app.route("/repos", methods=["GET"])
def list_repos():
    # List repositories for the authenticated user
    response = requests.get(f"{GITHUB_API_URL}/user/repos", headers=gh_headers())
    response.raise_for_status()
    return jsonify(response.json())


@app.route("/repos/<owner>/<repo>/create_file", methods=["POST"])
def create_file(owner, repo):
    data = request.json
    file_path = data["path"]
    content = data["content"]
    b64_content = base64.b64encode(content.encode()).decode()
    message = data.get("message", f"Create {file_path}")
    branch = data.get("branch", "main")
    payload = {
        "message": message,
        "content": b64_content,
        "branch": branch
    }
    url = f"{GITHUB_API_URL}/repos/{owner}/{repo}/contents/{file_path}"
    response = requests.put(url, headers=gh_headers(), json=payload)
    response.raise_for_status()
    return jsonify(response.json())


@app.route("/repos/<owner>/<repo>/zapier_webhook", methods=["POST"])
def create_zapier_webhook(owner, repo):
    data = request.json or {}
    zapier_url = data.get("zapier_hook_url") or data.get("target_url")
    if not zapier_url:
        return jsonify({"error": "zapier_hook_url is required"}), 400

    events = data.get("events") or ["push"]
    if not isinstance(events, list) or not events:
        return jsonify({"error": "events must be a non-empty list"}), 400

    config = {
        "url": zapier_url,
        "content_type": data.get("content_type", "json"),
    }

    secret = data.get("secret")
    if secret:
        config["secret"] = secret

    insecure_ssl = data.get("insecure_ssl")
    if insecure_ssl is not None:
        config["insecure_ssl"] = "1" if insecure_ssl else "0"

    payload = {
        "name": "web",
        "active": data.get("active", True),
        "events": events,
        "config": config,
    }

    response = requests.post(
        f"{GITHUB_API_URL}/repos/{owner}/{repo}/hooks",
        headers=gh_headers(),
        json=payload,
    )
    response.raise_for_status()
    return jsonify(response.json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
