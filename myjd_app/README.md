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
