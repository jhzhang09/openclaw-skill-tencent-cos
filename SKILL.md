---
name: tencent-cos
description: Tencent Cloud Object Storage (COS) manager. Upload files with automatic configurable retention (keep last N).
metadata: {"clawdbot":{"emoji":"☁️"}}
---

# Tencent COS Manager

Managed backups and file storage on Tencent Cloud COS.

## Setup

Requires environment variables:
- `TENCENT_SECRET_ID`
- `TENCENT_SECRET_KEY`
- `TENCENT_REGION`
- `TENCENT_BUCKET`

Optional:
- `TENCENT_PREFIX` (Default: `backups/`)
- `TENCENT_RETENTION` (Default: `0` - Disabled)

## Commands

```bash
# Check connection and storage status
python3 {baseDir}/scripts/upload.py status

# Upload a file (No automatic deletion by default)
python3 {baseDir}/scripts/upload.py upload /path/to/file.zip

# Upload with automatic retention (e.g., keep last 3)
python3 {baseDir}/scripts/upload.py upload /path/to/file.zip --retention 3

# Disable automatic deletion (set retention to 0)
python3 {baseDir}/scripts/upload.py upload /path/to/file.zip --retention 0
```

## Usage

- "Backup my database to Tencent COS"
- "Check if my COS backup is working"
- "Upload this log file to Tencent Cloud"
