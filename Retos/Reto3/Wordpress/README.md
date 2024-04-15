# Wordpress

## Especificaciones

- **AMI:** Ubuntu Server 20.04 LTS.
- **Key Pair:** la clave pem utilizada en el reto 3.
- **VPC:** VPC creada en el reto 3.
- **Subnet:** Subnet privada.
- **Puerto HTTP:** 80.

## Prerequisitos

Para conectase a esta máquina es necesario conectarse desde el JumpServer.

Para montar el contenedor de Wordpress se necesita tener una instancia de MySQL y una instancia de NFS.

### Instalación de Docker y Docker Compose

Para instalar Docker y Docker Compose en la instancia de Ubuntu, se deben seguir los siguientes pasos:

1. Instalar Docker:

   ```bash
   sudo apt update
   sudo apt install docker.io -y
   sudo apt install docker-compose -y
   sudo apt install git -y
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

1. Agregar el usuario al grupo de Docker:

   ```bash
   sudo usermod -aG docker $USER
   ```

1. Cerrar la sesión y volver a iniciarla.

### Montar NFS

1. Instalar `nfs-common`:

   ```bash
   sudo apt update
   sudo apt install nfs-common -y
   ```

1. Crear el directorio de montaje:

   ```bash
    sudo mkdir -p /mnt/wordpress
   ```

1. Montar el directorio:

   ```bash
   sudo mount <ip_nfs>:/mnt/wordpress /mnt/wordpress
   ```

## Configuración

Este Docker Compose se utiliza para crear un entorno de WordPress utilizando contenedores Docker. Se debe crear un archivo llamado `docker-compose.yml` con el siguiente contenido:

```yaml
version: "3.1"
services:
  wordpress:
    container_name: wordpress
    image: wordpress
    ports:
      - 80:80
    restart: always
    environment:
      WORDPRESS_DB_HOST: <ip-privada>
      WORDPRESS_DB_USER: exampleuser
      WORDPRESS_DB_PASSWORD: examplepass
      WORDPRESS_DB_NAME: exampledb
    volumes:
      - /mnt/wordpress:/var/www/html
```

Donde:

- **container_name:** Especifica el nombre del contenedor como "wordpress".
- **image:** Especifica la imagen de Docker a utilizar, en este caso, "wordpress".
- **ports:** Mapea el puerto 80 del contenedor al puerto 80 del host para permitir el acceso a WordPress a través del navegador.
- **restart:** Indica que el contenedor se reiniciará siempre que se detenga.
- **environment:** Configura las variables de entorno necesarias para la base de datos de WordPress. La WORDPRESS_DB_HOST debe ser reemplazada por la dirección IP privada de la base de datos, y se proporcionan las credenciales de usuario, contraseña y nombre de la base de datos.
- **volumes:** Monta un volumen llamado "wordpress" en el directorio /var/www/html dentro del contenedor, que es donde se alojan los archivos de WordPress.

## Despliegue

Para desplegar el entorno de WordPress, se debe ejecutar el siguiente comando en el directorio donde se encuentra el archivo docker-compose.yml:

```bash
docker-compose up -d
```

Esto creará y ejecutará los contenedores necesarios para WordPress. Una vez que el contenedor esté en funcionamiento, se puede acceder a WordPress a través del navegador web utilizando la dirección IP del host y el puerto 80.

> [!NOTE]
> Se debe crear otra instancia de Wordpress de esta misma manera.
