# MyJDownloader Trigger

This simple script uses the [MyJDownloader API](https://my.jdownloader.org/) to
send a list of Instagram or YouTube profile URLs to a remote JDownloader client
(such as a Mac in the Austin office). The client then parses the profiles and
automatically starts downloading any new videos.

## Setup
1. `pip install myjdapi`
2. Export your MyJDownloader credentials and device name:
   ```bash
   export MYJD_EMAIL="you@example.com"
   export MYJD_PASSWORD="your-password"
   export MYJD_DEVICE="Name-of-Mac"
   ```
3. Put the profile or channel URLs in `channels.txt` (one per line).

## Run
```bash
python trigger.py
```

The script reads `channels.txt`, connects to the specified device, and feeds the
links into JDownloader with autostart enabled.

## Canto deduplication & upload

After downloads finish, you can automatically upload only the new files to
[Canto](https://www.canto.com/) by hashing each file and checking whether it
already exists in the DAM.

1. Install dependencies:
   ```bash
   pip install requests
   ```
2. Export your Canto credentials and download folder:
   ```bash
   export CANTO_API_BASE="https://your.canto.com/api/v1"
   export CANTO_API_TOKEN="your-canto-token"
   export DOWNLOAD_DIR="/path/to/jdownloader/downloads"
   ```
3. Run the sync script:
   ```bash
   python canto_sync.py
   ```

The script computes a SHA-256 hash for each file in `DOWNLOAD_DIR`, queries
Canto for that hash, and uploads the file only if it is missing.
