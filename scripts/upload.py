#!/usr/bin/env python3
"""
Tencent Cloud COS Uploader with Retention Policy.
Optimized version for OpenClaw.
"""

import os
import sys
import json
import argparse
import logging
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger("tencent-cos")

def load_config():
    """Load config from env or file."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config.json")
    
    config = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
        except Exception as e:
            logger.warning(f"Error loading config.json: {e}")

    return {
        'id': os.getenv('TENCENT_SECRET_ID') or config.get('SecretId'),
        'key': os.getenv('TENCENT_SECRET_KEY') or config.get('SecretKey'),
        'region': os.getenv('TENCENT_REGION') or config.get('Region'),
        'bucket': os.getenv('TENCENT_BUCKET') or config.get('Bucket'),
        'prefix': os.getenv('TENCENT_PREFIX') or config.get('Prefix', 'backups/'),
        'retention': int(os.getenv('TENCENT_RETENTION') or config.get('Retention', 0))
    }

def get_client(conf):
    if not all([conf['id'], conf['key'], conf['region'], conf['bucket']]):
        logger.error("Missing required COS configuration (SecretId, SecretKey, Region, Bucket).")
        return None
    
    c = CosConfig(Region=conf['region'], SecretId=conf['id'], SecretKey=conf['key'])
    return CosS3Client(c)

def upload_file(client, conf, local_path, custom_prefix=None, custom_retention=None):
    if not os.path.exists(local_path):
        logger.error(f"File not found: {local_path}")
        return False

    prefix = custom_prefix or conf['prefix']
    retention = custom_retention if custom_retention is not None else conf['retention']
    
    if not prefix.endswith('/'):
        prefix += '/'
    
    file_name = os.path.basename(local_path)
    cos_key = f"{prefix}{file_name}"

    try:
        logger.info(f"Uploading {file_name} to {conf['bucket']}/{cos_key}...")
        # High-level upload handles multipart automatically for large files
        response = client.upload_file(
            Bucket=conf['bucket'],
            LocalFilePath=local_path,
            Key=cos_key,
            EnableMD5=True # Enabled for integrity
        )
        logger.info(f"Upload successful. ETag: {response.get('ETag')}")
        
        # Retention check
        if retention > 0:
            check_retention(client, conf['bucket'], prefix, retention)
        return True
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        return False

def check_retention(client, bucket, prefix, max_keep):
    try:
        response = client.list_objects(Bucket=bucket, Prefix=prefix)
        if 'Contents' in response:
            backups = [obj for obj in response['Contents'] if not obj['Key'].endswith('/')]
            backups.sort(key=lambda x: x['LastModified'])
            
            while len(backups) > max_keep:
                oldest = backups.pop(0)
                logger.info(f"Retention policy: Deleting oldest backup {oldest['Key']}")
                client.delete_object(Bucket=bucket, Key=oldest['Key'])
    except Exception as e:
        logger.warning(f"Retention policy check failed: {e}")

def check_status(client, conf):
    try:
        # Check if bucket exists/accessible
        client.head_bucket(Bucket=conf['bucket'])
        logger.info(f"✅ Connection successful to bucket '{conf['bucket']}' in {conf['region']}")
        
        # Check storage usage in prefix
        response = client.list_objects(Bucket=conf['bucket'], Prefix=conf['prefix'])
        count = len(response.get('Contents', []))
        logger.info(f"📁 Files found in prefix '{conf['prefix']}': {count}")
        return True
    except Exception as e:
        logger.error(f"❌ Connection failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Tencent Cloud COS Uploader")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Upload command
    up_parser = subparsers.add_parser("upload", help="Upload a file")
    up_parser.add_argument("path", help="Local file path")
    up_parser.add_argument("--prefix", help="Override default prefix")
    up_parser.add_argument("--retention", type=int, help="Number of backups to keep (overrides config/env)")

    # Status command
    subparsers.add_parser("status", help="Check COS connection status")

    args = parser.parse_args()
    conf = load_config()
    client = get_client(conf)

    if not client:
        sys.exit(1)

    if args.command == "upload":
        if not upload_file(client, conf, args.path, args.prefix, args.retention):
            sys.exit(1)
    elif args.command == "status":
        if not check_status(client, conf):
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
