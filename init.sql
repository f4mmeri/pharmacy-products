-- Archivo de inicialización de la base de datos
-- Se ejecuta automáticamente cuando se crea el contenedor de MySQL

-- Asegurarse de que la base de datos existe
CREATE DATABASE IF NOT EXISTS farmacia;

-- Usar la base de datos
USE farmacia;

-- Establecer el conjunto de caracteres
ALTER DATABASE farmacia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verificar que el usuario tiene los permisos correctos
GRANT ALL PRIVILEGES ON farmacia.* TO 'farmacia_user'@'%';
FLUSH PRIVILEGES;