# MySQL

## Especificaciones

- **AMI:** Ubuntu Server 20.04 LTS.
- **Key Pair:** la clave pem utilizada en el reto 3.
- **VPC:** VPC creada en el reto 3.
- **Subnet:** Subnet privada.
- **Puerto SSH:** 22.
- **Puerto MySQL:** 3306.

## Prerequisitos

Para conectase a esta máquina es necesario conectarse desde el JumpServer.

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

2. Agregar el usuario al grupo de Docker:

```bash
sudo usermod -aG docker $USER
```

3. Cerrar la sesión y volver a iniciarla.

## Docker Compose

Este Docker Compose se utiliza para crear un entorno de MySQL utilizando contenedores Docker. Se debe crear un archivo llamado `docker-compose.yml` con el siguiente contenido:

```yaml
version: "3.1"
services:
  db:
    image: mysql:5.7
    restart: always
    ports:
      - 3306:3306
    environment:
      MYSQL_DATABASE: exampledb
      MYSQL_USER: exampleuser
      MYSQL_PASSWORD: examplepass
      MYSQL_RANDOM_ROOT_PASSWORD: "1"
    volumes:
      - db:/var/lib/mysql
```

Donde:

- **image:** Especifica la imagen de Docker a utilizar, en este caso, "mysql:5.7".
- **restart:** Indica que el contenedor se reiniciará siempre que se detenga.
- **ports:** Mapea el puerto 3306 del contenedor al puerto 3306 del host para permitir el acceso a MySQL.
- **environment:** Configura las variables de entorno necesarias para la base de datos de MySQL. Se proporcionan el nombre de la base de datos, el usuario, la contraseña y se genera una contraseña aleatoria para el usuario root.
- **volumes:** Monta un volumen llamado "db" en el directorio /var/lib/mysql dentro del contenedor, que es donde se almacenan los datos de MySQL.
- **MYSQL_DATABASE:** Especifica el nombre de la base de datos.
- **MYSQL_USER:** Especifica el nombre de usuario para la base de datos.
- **MYSQL_PASSWORD:** Especifica la contraseña del usuario de la base de datos.
- **MYSQL_RANDOM_ROOT_PASSWORD:** Genera una contraseña aleatoria para el usuario root de MySQL.

## Despliegue

Para desplegar el entorno de MySQL, se debe ejecutar el siguiente comando en el directorio donde se encuentra el archivo docker-compose.yml:

```bash
docker-compose up -d
```

Esto creará y ejecutará el contenedor necesario para MySQL. Una vez que el contenedor esté en funcionamiento, se puede acceder a MySQL a través de un cliente MySQL utilizando la dirección IP del host y el puerto 3306.
