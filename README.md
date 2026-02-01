# OpenClaw Skill: Tencent COS

A utility skill for [OpenClaw](https://github.com/openclaw/openclaw) agents to manage file uploads and backups to Tencent Cloud Object Storage (COS).

## Features

- **File Upload**: Upload local files to a specified COS bucket.
- **Backup Rotation**: Automatically manage backup retention (e.g., keep last N backups).
- **Path Management**: Configurable remote storage paths.

## Installation

Clone this repository into your OpenClaw skills directory:

```bash
cd /root/clawd/skills
git clone https://github.com/jhzhang09/openclaw-skill-tencent-cos.git tencent-cos
```

## Configuration

Set the following environment variables in your OpenClaw agent's `.env` file or environment:

```bash
COS_SECRET_ID=your_secret_id
COS_SECRET_KEY=your_secret_key
COS_REGION=ap-guangzhou
COS_BUCKET=your-bucket-name-1234567890
```

## Usage

This skill exposes a `scripts/upload.py` script.

```bash
# Upload a file
python3 scripts/upload.py /path/to/local/file.zip --remote-path backups/
```

## License

MIT
