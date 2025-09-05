"""Chive TV content idea generator.

This module fetches active contributors from Airtable and clips from Canto,
combines them with trending tags, and produces content ideas. Results can be
logged to Google Sheets to avoid suggesting the same clip within six months.

Environment variables:
    AIRTABLE_API_KEY       - Airtable API key.
    AIRTABLE_BASE_ID       - Airtable base identifier.
    AIRTABLE_TABLE_NAME    - Airtable table with contributor data.
    CANTO_API_TOKEN        - Canto API token.
    CANTO_ALBUM_ID         - Canto album identifier to scan.
    GOOGLE_SHEETS_CRED_FILE - Path to Google service-account credential JSON.
    GOOGLE_SHEETS_SHEET_ID  - Target Google Sheet ID for logging.
"""
from __future__ import annotations

import os
import csv
import re
from urllib.parse import urlparse
from datetime import datetime
from typing import List, Dict, Set

import requests


AIRTABLE_URL = "https://api.airtable.com/v0"
CANTO_URL = "https://api.canto.com/v1"
GOOGLE_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_airtable_contributors(api_key: str, base_id: str, table_name: str) -> List[Dict]:
    """Return contributors whose Status field contains the word 'active'."""
    if not api_key:
        raise RuntimeError("Missing Airtable API key")
    if not base_id:
        raise RuntimeError("Missing Airtable base ID")

    url = f"{AIRTABLE_URL}/{base_id}/{table_name}"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"filterByFormula": "FIND('active', LOWER({Status}))"}
    resp = requests.get(url, headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    contributors = []
    for record in resp.json().get("records", []):
        fields = record.get("fields", {})
        contributors.append(
            {
                "id": record.get("id"),
                "name": fields.get("Name"),
                "tags": fields.get("Tags", []),
            }
        )
    return contributors


def get_canto_clips(token: str, album_id: str) -> List[Dict]:
    """Fetch clip metadata from a Canto album."""
    if not token:
        raise RuntimeError("Missing Canto API token")
    if not album_id:
        raise RuntimeError("Missing Canto album ID")

    url = f"{CANTO_URL}/asset/album/{album_id}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    clips = []
    for asset in resp.json().get("assets", []):
        file_name = asset.get("name", "")
        contributor = file_name.split("_")[0] if "_" in file_name else ""
        clips.append(
            {
                "id": asset.get("id"),
                "file_name": file_name,
                "tags": asset.get("tags", []),
                "description": asset.get("description", ""),
                "upload_date": asset.get("createdDate"),
                "contributor": contributor,
            }
        )
    return clips


def read_clip_list(path: str) -> Set[str]:
    """Return a set of file names exported from JDownloader LinkGrabber.

    The export can be created via LinkGrabber → Export → Text file. Each line
    may contain a URL or a file name; the function normalises each entry to the
    base file name for comparison with Canto assets.
    """
    if not path:
        return set()
    file_names: Set[str] = set()
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            parsed = urlparse(line)
            file_name = os.path.basename(parsed.path) if parsed.scheme else line
            file_names.add(file_name)
    return file_names


def get_trending_tags() -> List[str]:
    """Fetch a simple list of trending search topics from Google Trends."""
    url = "https://trends.google.com/trends/hottrends/visualize/internal/data"
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    # Flatten results and keep unique topics
    trends = []
    for group in data:
        trends.extend(group[:3])
    return list(dict.fromkeys(trends))


def generate_content_ideas(
    contributors: List[Dict], clips: List[Dict], trends: List[str]
) -> List[Dict]:
    """Combine tags and trends to propose content ideas."""
    trend_set = {t.lower() for t in trends}
    ideas: List[Dict] = []

    for clip in clips:
        tags = [t.lower() for t in clip.get("tags", [])]
        # Include keywords from the description as additional tags
        desc = clip.get("description", "")
        desc_words = [w for w in re.findall(r"\w+", desc.lower()) if len(w) > 3]
        tags.extend(desc_words)
        matched_trends = list(trend_set.intersection(tags))
        idea_tags = tags + matched_trends
        ideas.append(
            {
                "clip_id": clip["id"],
                "contributor": clip.get("contributor"),
                "tags": idea_tags,
                "description": desc,
                "suggested": datetime.utcnow().isoformat() + "Z",
            }
        )
    return ideas


def log_to_google_sheets(cred_file: str, sheet_id: str, ideas: List[Dict]) -> None:
    """Append generated ideas to a Google Sheet.

    Requires a service-account credential JSON file.
    """
    if not cred_file or not sheet_id:
        raise RuntimeError("Google Sheets credentials or sheet ID missing")
    try:
        import gspread
        from google.oauth2.service_account import Credentials
    except Exception as exc:  # pragma: no cover - optional dependency
        raise RuntimeError("gspread and google-auth are required for Sheets logging") from exc

    creds = Credentials.from_service_account_file(cred_file, scopes=GOOGLE_SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id).sheet1
    rows = [
        [i["clip_id"], i["contributor"], ", ".join(i["tags"]), i["suggested"]]
        for i in ideas
    ]
    sheet.append_rows(rows, value_input_option="USER_ENTERED")


def log_to_csv(path: str, ideas: List[Dict]) -> None:
    """Append ideas to a local CSV file for duplicate tracking."""
    if not path:
        return
    exists = os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if not exists:
            writer.writerow(["clip_id", "contributor", "tags", "suggested"])
        for idea in ideas:
            writer.writerow([
                idea["clip_id"],
                idea.get("contributor", ""),
                ", ".join(idea.get("tags", [])),
                idea.get("suggested", ""),
            ])


def main() -> List[Dict]:
    """Run the full pipeline and return generated ideas."""
    airtable_key = os.getenv("AIRTABLE_API_KEY")
    base_id = os.getenv("AIRTABLE_BASE_ID")
    table_name = os.getenv("AIRTABLE_TABLE_NAME", "Contributors")
    canto_token = os.getenv("CANTO_API_TOKEN")
    album_id = os.getenv("CANTO_ALBUM_ID")

    list_file = os.getenv("JDOWNLOADER_LIST_FILE")
    listed_files = read_clip_list(list_file)

    contributors = get_airtable_contributors(airtable_key, base_id, table_name)
    clips = get_canto_clips(canto_token, album_id)
    if listed_files:
        clips = [c for c in clips if c.get("file_name") in listed_files]
    trends = get_trending_tags()
    ideas = generate_content_ideas(contributors, clips, trends)

    cred_file = os.getenv("GOOGLE_SHEETS_CRED_FILE")
    sheet_id = os.getenv("GOOGLE_SHEETS_SHEET_ID")
    if cred_file and sheet_id:
        log_to_google_sheets(cred_file, sheet_id, ideas)

    log_file = os.getenv("IDEAS_LOG_FILE")
    if log_file:
        log_to_csv(log_file, ideas)
    return ideas


if __name__ == "__main__":  # pragma: no cover - manual execution
    try:
        generated = main()
        for idea in generated:
            print(f"{idea['contributor']}: {', '.join(idea['tags'])}")
    except Exception as err:
        print(f"Error: {err}")
