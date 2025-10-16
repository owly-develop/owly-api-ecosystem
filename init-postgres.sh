#!/bin/bash
set -e

echo "🔧 Configurando PostgreSQL para aceptar conexiones externas..."

# Esperar a que PostgreSQL esté listo
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "⏳ Esperando a que PostgreSQL esté listo..."
  sleep 2
done

echo "✅ PostgreSQL está listo"

# Configurar pg_hba.conf para permitir conexiones con md5
cat > "${PGDATA}/pg_hba.conf" << 'EOF'
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             all                                     md5

# IPv4 local connections:
host    all             all             127.0.0.1/32            md5

# IPv6 local connections:
host    all             all             ::1/128                 md5

# Allow replication connections
local   replication     all                                     md5
host    replication     all             127.0.0.1/32            md5
host    replication     all             ::1/128                 md5

# Allow connections from Docker network and external hosts
host    all             all             172.16.0.0/12           md5
host    all             all             192.168.0.0/16          md5
host    all             all             10.0.0.0/8              md5
host    all             all             0.0.0.0/0               md5
host    all             all             ::/0                    md5
EOF

# Configurar postgresql.conf para escuchar en todas las interfaces
cat >> "${PGDATA}/postgresql.conf" << EOF

# Configuración personalizada para permitir conexiones externas
listen_addresses = '*'
max_connections = 200
shared_buffers = 128MB
EOF

echo "✅ Configuración de PostgreSQL completada"

# Recargar la configuración
pg_ctl reload -D "${PGDATA}"

echo "✅ PostgreSQL reconfigurado y listo para aceptar conexiones"
