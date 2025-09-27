-- Archivo de inicialización de MySQL
-- Se ejecuta automáticamente cuando se crea el contenedor

-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS farmacia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Usar la base de datos
USE farmacia;

-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON farmacia.* TO 'farmacia_user'@'%';
FLUSH PRIVILEGES;

-- Mostrar información de inicialización
SELECT 'Base de datos farmacia inicializada correctamente' as message;