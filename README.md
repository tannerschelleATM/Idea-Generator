# Idea-Generator

Python application that scans Airtable contributor data and Canto clip information to generate content ideas for Chive TV editors.

## Features

- Fetch active contributors from Airtable using the `Status` field and their `Tags`.
- Read a manually exported list of clip names from JDownloader LinkGrabber and match them with Canto assets.
- Scan Canto albums for clips; parse file names (`Contributor_UniqueURL_IG.mp4`) to determine contributor credit and collect tags and descriptions.
- Consider clip descriptions as additional keywords and pull trending topics from the internet (Google Trends) to enrich ideas.
- Generate ideas tagged as seasonal, trending, or silly.
- Log suggestions to Google Sheets and/or a local CSV file to avoid duplication.
- Tkinter GUI displays the generated ideas and includes a background scheduler that runs every Monday at 07:00 ET.

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
JDOWNLOADER_LIST_FILE   Path to text file exported from JDownloader
IDEAS_LOG_FILE          Path to local CSV for logging generated ideas
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

Ideas are appended to the provided Google Sheet and/or the local CSV file with clip ID, contributor, tags, and timestamp. The log can be used to suppress repeats for six months or longer.
