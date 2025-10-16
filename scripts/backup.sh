#!/bin/bash

# OWLY CRM API - Database Backup Script

set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="owly_crm_backup_${TIMESTAMP}.sql"

echo "📦 Creating backup directory..."
mkdir -p $BACKUP_DIR

echo "💾 Backing up database..."
docker-compose exec -T db pg_dump -U owly_user owly_crm > "${BACKUP_DIR}/${BACKUP_FILE}"

echo "🗜️  Compressing backup..."
gzip "${BACKUP_DIR}/${BACKUP_FILE}"

echo "✅ Backup completed: ${BACKUP_DIR}/${BACKUP_FILE}.gz"

# Keep only last 7 backups
echo "🧹 Cleaning old backups..."
cd $BACKUP_DIR
ls -t *.gz | tail -n +8 | xargs -r rm

echo "✅ Backup process finished!"

