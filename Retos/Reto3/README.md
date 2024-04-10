# ST0263 Tópicos Especiales en Telemática

**Estudiante: Miguel Sosa, msosav@eafit.edu.co**

**Profesor: Edwin Montoya, emontoya@eafit.edu.co**

## Nombre de la actividad

### 1. Breve descripción de la actividad

Desplegar WordPress empleando la tecnología de contenedores, con su **propio dominio** y **certificado SSL**. El sitio lo llamará: reto3._sudominio.tld_.

En este reto se utilizará un nginx como **balanceador de cargas** de la capa de aplicación del wordpress o aplicación monolítica elegida.

Además de lo anterior, se utilizarán 2 servidores adicionales, uno para base de datos (DBServer) y otro para archivos (FileServer). El DBServer podrá utilizar la BD en **docker** (recomendado) o nativa. Y el FileServer implementará un **NFSServer**.

#### 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

#### 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

### 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

### 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

#### Instalación de Docker y Docker Compose en Ubuntu 20.04

1. Se debe instalar Docker y Docker Compose en la máquina virtual.

   ```bash
   sudo apt update
   sudo apt install docker.io -y
   sudo apt install docker-compose -y
   sudo apt install git -y

   sudo systemctl enable docker
   sudo systemctl start docker
   ```

1. Se debe añadir el usuario al grupo de Docker.

   ```bash
   sudo usermod -aG docker $USER
   ```

   _Luego se tiene que cerrar la sesión y volver a iniciarla._

#### Monolito de WordPress

Se debe crear una máquina virtual en la nube con Ubuntu 20.04 (preferiblemente) con el puerto 8080 abierto. Además se debe instalar [Docker y Docker Compose](#instalación-de-docker-y-docker-compose-en-ubuntu-2004).

Los pasos a seguir son los siguientes:

1. Se debe crear una archivo `docker-compose.yml` con el siguiente contenido:

   ```yaml
   services:
     db:
       image: mariadb:10
       volumes:
         - data:/var/lib/mysql
       environment:
         - MYSQL_ROOT_PASSWORD=secret
         - MYSQL_DATABASE=wordpress
         - MYSQL_USER=manager
         - MYSQL_PASSWORD=secret
     web:
       image: wordpress:6
       depends_on:
         - db
       volumes:
         - ./target:/var/www/html
       environment:
         - WORDPRESS_DB_USER=manager
         - WORDPRESS_DB_PASSWORD=secret
         - WORDPRESS_DB_HOST=db
         - WORDPRESS_DB_NAME=wordpress
       ports:
         - 8080:80

   volumes:
     data:
   ```

1. Se debe ejecutar el siguiente comando para levantar el servicio.

   ```bash
    docker-compose up -d
   ```

1. Se debe acceder a la dirección IP de la máquina virtual en el puerto 8080.

### 4. Descripción del ambiente de ejecución (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

- IP o nombres de dominio en nube o en la máquina servidor.
- Descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
- Como se lanza el servidor.
- Una mini guia de como un usuario utilizaría el software o la aplicación
- Opcional - si quiere mostrar resultados o pantallazos

### 5. Otra información que considere relevante para esta actividad.

## Referencias:
