# Proyecto final - Grupal IDWEB - A
## Nombre del proyecto: Página de comidas
## Nombre de Grupo: Nexus
**Integrantes:** 
- Achiri Cuevas, Daniel Cooper
- Cavero Ale, Leonardo Ismael
- Salas Zegarra, Marco Antonio

### 🌐 Sitio web hospedaje en pythonanywhere:

Aquí link la pagina web: [Pagina web](http://msalasze.pythonanywhere.com/)

### Lenguajes utilizados:

- HTML 
- CSS
- JS
- Python
- SQL

## ▶️ Instrucciones de ejecución

### 1️⃣ Clonar el repositorio
```bash
git https://github.com/dachiri-unsa/ProyectoGrupal_IDWEB
```
### 2️⃣ Configurar la base de datos

MySQL:

- Crear una base de datos, usa este codigo:
```
CREATE DATABASE BD_IDWEB_grupal;
USE BD_IDWEB_grupal;

CREATE TABLE usuarios (
  id_usuario int(11) NOT NULL AUTO_INCREMENT,
  gmail varchar(255) NOT NULL,
  nombre varchar(100) NOT NULL,
  contrasenia varchar(255) NOT NULL,
  recibir_correos tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (id_usuario),
  UNIQUE KEY gmail (gmail)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```
Recuerda: Para conectar con el MySQL de tu pc cambia el password al suyo en DB.py (linea 07).

### 3️⃣ Ejecutar el servidor 
Ejecuta el archivo server.py en tu computadora.

### 4️⃣ Acceder a la pagina

Abrir el navegador e ingresar a:

http://localhost:8000

Listo ahí ya puede probar todas las funcionalidades de la página.