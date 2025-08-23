import os
from flask import Flask, request, jsonify
import requests
import base64

app = Flask(__name__)

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_API_URL = "https://api.github.com"


def gh_headers():
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
