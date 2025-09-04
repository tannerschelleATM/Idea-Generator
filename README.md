# Idea-Generator

Python application that scans Airtable contributor data and Canto clip information to generate content ideas for Chive TV editors.

## Features

- Fetch active contributors from Airtable using the `Status` field and their `Tags`.
- Scan Canto albums for clips; parse file names (`Contributor_UniqueURL_IG.mp4`) to determine contributor credit and collect tags and descriptions.
- Pull trending topics from the internet (Google Trends) to enrich ideas.
- Generate ideas tagged as seasonal, trending, or silly.
- Log suggestions to Google Sheets to avoid duplication.
- Tkinter GUI with manual run button and background scheduler that runs every Monday at 07:00 ET.

## Configuration

Set these environment variables:

```
AIRTABLE_API_KEY        Airtable API key
AIRTABLE_BASE_ID        Airtable base ID containing contributors
AIRTABLE_TABLE_NAME     Table name (defaults to "Contributors")
CANTO_API_TOKEN         Canto API token
CANTO_ALBUM_ID          Canto album ID to scan
GOOGLE_SHEETS_CRED_FILE Path to service-account credentials JSON
GOOGLE_SHEETS_SHEET_ID  Google Sheet ID for logging
```

## Usage

Install dependencies:

```
pip install requests gspread google-auth
```

Run the GUI:

```
python app.py
```

The app starts a scheduler for the weekly job and provides a **Run Now** button for manual execution.

## Logging

Ideas are appended to the provided Google Sheet with clip ID, contributor, tags, and timestamp. The log can be used to suppress repeats for six months or longer.
