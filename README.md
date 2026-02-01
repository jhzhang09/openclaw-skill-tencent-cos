# OpenClaw Skill: Tencent COS

A utility skill for [OpenClaw](https://github.com/openclaw/openclaw) agents to manage file uploads and backups to Tencent Cloud Object Storage (COS).

[中文说明](#中文说明)

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

---

## <a id="中文说明"></a>中文说明

这是一个为 [OpenClaw](https://github.com/openclaw/openclaw) Agent 设计的工具技能，用于将文件上传和备份到腾讯云对象存储 (COS)。

### 功能特性

- **文件上传**: 将本地文件上传到指定的 COS 存储桶。
- **备份轮转**: 自动管理备份保留策略（例如：仅保留最近 N 个备份）。
- **路径管理**: 可配置的远程存储路径。

### 安装

将此仓库克隆到您的 OpenClaw skills 目录中：

```bash
cd /root/clawd/skills
git clone https://github.com/jhzhang09/openclaw-skill-tencent-cos.git tencent-cos
```

### 配置

在您的 OpenClaw agent 的 `.env` 文件或环境变量中设置以下内容：

```bash
COS_SECRET_ID=your_secret_id
COS_SECRET_KEY=your_secret_key
COS_REGION=ap-guangzhou
COS_BUCKET=your-bucket-name-1234567890
```

### 使用方法

此技能提供了一个 `scripts/upload.py` 脚本。

```bash
# 上传文件
python3 scripts/upload.py /path/to/local/file.zip --remote-path backups/
```

## License

MIT
