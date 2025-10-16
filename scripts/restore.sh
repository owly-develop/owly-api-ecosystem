#!/bin/bash

# OWLY CRM API - Database Restore Script

set -e

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh <backup_file.sql.gz>"
    echo ""
    echo "Available backups:"
    ls -lh ./backups/*.gz 2>/dev/null || echo "No backups found"
    exit 1
fi

BACKUP_FILE=$1

if [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

echo "⚠️  WARNING: This will replace the current database!"
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "❌ Restore cancelled"
    exit 0
fi

echo "📦 Extracting backup..."
gunzip -c "$BACKUP_FILE" > /tmp/restore.sql

echo "🔄 Restoring database..."
docker-compose exec -T db psql -U owly_user owly_crm < /tmp/restore.sql

rm /tmp/restore.sql

echo "✅ Database restored successfully!"

