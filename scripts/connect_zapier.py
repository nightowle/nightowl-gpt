#!/usr/bin/env python3
"""Utility to connect a GitHub repository webhook to a Zapier catch hook."""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Iterable

import requests


GITHUB_API_URL = "https://api.github.com"


def build_headers(token: str) -> dict[str, str]:
    """Return HTTP headers for GitHub API requests using the supplied token."""
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }


def normalize_events(raw_events: Iterable[str] | None) -> list[str]:
    """Return a list of webhook events from the raw CLI argument."""
    if raw_events is None:
        return ["push"]
    events: list[str] = []
    for value in raw_events:
        if not value:
            continue
        for token in value.split(","):
            token = token.strip()
            if token:
                events.append(token)
    return events or ["push"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create or update a GitHub repository webhook that forwards events to a "
            "Zapier catch hook."
        )
    )
    parser.add_argument("owner", help="GitHub repository owner (user or organization)")
    parser.add_argument("repository", help="GitHub repository name")
    parser.add_argument("zapier_hook_url", help="Zapier catch hook URL")
    parser.add_argument(
        "--token",
        help=(
            "GitHub token with repo and workflow scope. Defaults to the "
            "GITHUB_TOKEN environment variable."
        ),
    )
    parser.add_argument(
        "--events",
        nargs="*",
        help=(
            "Webhook events to subscribe to. Accepts repeated values or a single "
            "comma-separated string. Defaults to 'push'."
        ),
    )
    parser.add_argument(
        "--secret",
        help=(
            "Optional secret used by GitHub to sign webhook payloads. Should match "
            "the secret configured in Zapier."
        ),
    )
    parser.add_argument(
        "--inactive",
        dest="active",
        action="store_false",
        help="Create the webhook in an inactive state.",
    )
    parser.add_argument(
        "--insecure-ssl",
        action="store_true",
        help="Allow GitHub to send payloads to Zapier over insecure SSL.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = args.token or os.environ.get("GITHUB_TOKEN")
    if not token:
        print(
            "error: provide a GitHub token via --token or the GITHUB_TOKEN environment variable",
            file=sys.stderr,
        )
        return 1

    events = normalize_events(args.events)

    payload = {
        "name": "web",
        "active": args.active,
        "events": events,
        "config": {
            "url": args.zapier_hook_url,
            "content_type": "json",
        },
    }

    if args.secret:
        payload["config"]["secret"] = args.secret

    if args.insecure_ssl:
        payload["config"]["insecure_ssl"] = "1"

    url = f"{GITHUB_API_URL}/repos/{args.owner}/{args.repository}/hooks"

    response = requests.post(url, headers=build_headers(token), json=payload, timeout=30)

    if response.status_code >= 400:
        print("GitHub API error:", file=sys.stderr)
        try:
            data = response.json()
        except ValueError:
            data = response.text
        print(json.dumps(data, indent=2) if isinstance(data, dict) else data, file=sys.stderr)
        return 1

    print(json.dumps(response.json(), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
