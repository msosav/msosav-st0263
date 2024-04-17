# Load Balancer

## Especificaciones

- **AMI:** Ubuntu Server 20.04 LTS.
- **Key Pair:** la clave pem utilizada en el reto 3.
- **VPC:** VPC creada en el reto 3.
- **Subnet:** Subnet pública.
- **Asignación de IP:** IP pública.
- **Puerto SSH:** 22.
- **Puerto HTTP:** 80.
- **Puerto HTTPS:** 443.

## Prerequisitos

### IP Elástica

1. Ir a la consola de AWS.
2. Ir a la sección de EC2.
3. Darle click en "Elastic IPs".
4. Darle click en "Allocate Elastic IP address".
5. Darle click en "Allocate".
6. Darle click derecho en la IP y seleccionar "Associate address".
7. Seleccionar la instancia y la ip privada.
8. Darle click en "Associate".

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

## Configuración

1. Se beben crear las entradas en el DNS para los subdominios

   ```plaintext
   reto3.sudominio.com -> IP Elastica
   www.reto3.sudominio.com -> misma IP Elastica
   ```

1. Se debe instalado el certbot

   ```bash
   sudo apt update
   sudo add-apt-repository ppa:certbot/certbot
   sudo apt install letsencrypt -y
   sudo apt install nginx -y
   ```

1. Se debe generar el certificado

   ```bash
   sudo mkdir -p /var/www/letsencrypt
   sudo certbot --server https://acme-v02.api.letsencrypt.org/directory -d *.sudominio.com --manual --preferred-challenges dns-01 certonly
   ```

   _Este comando queda pausado indicando que debe crear un registro TXT en su dominio, una vez lo cree y verifique, dele ENTER para Continuar. Debe terminar con éxito._

1. Se debe crear los directorios para el docker compose

   ```bash
   mkdir loadbalancer
   mkdir loadbalancer/ssl
   ```

1. Se debe copiar los certificados

   ```bash
   sudo cp /etc/letsencrypt/live/sudominio.com/* /home/ubuntu/loadbalancer/ssl
   ```

1. Se debe crear el archivo de configuración de Nginx en el directorio `loadbalancer` y cambiar `<wordpress_ip_1>` y `<wordpress_ip_2>` por las direcciones IP de las instancias de Wordpress

   ```bash
   nano loadbalancer/nginx.conf
   ```

   ```nginx
   worker_processes auto;
   error_log /var/log/nginx/error.log;
   pid /run/nginx.pid;

   events {
      worker_connections 1024;  ## Default: 1024
   }

   http {
      upstream backend {
         server <wordpress_ip_1>;
         server <wordpress_ip_2>;
      }

      server {
         listen 80;
         listen [::]:80;
         server_name _;
         rewrite ^ https://$host$request_uri permanent;
      }

      server {
         listen 443 ssl http2 default_server;
         listen [::]:443 ssl http2 default_server;
         server_name _;

         # enable subfolder method reverse proxy confs
         #include /config/nginx/proxy-confs/*.subfolder.conf;

         # all ssl related config moved to ssl.conf
         include /etc/nginx/ssl.conf;

         client_max_body_size 0;

         location / {
               proxy_pass http://backend;
               proxy_redirect off;
               proxy_set_header Host $host;
               proxy_set_header X-Real-IP $remote_addr;
               proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
               proxy_set_header X-Forwarded-Host $host;
               proxy_set_header X-Forwarded-Server $host;
               proxy_set_header X-Forwarded-Proto $scheme;
         }
      }
   }
   ```

   Donde:

   - `worker_processes auto`: Número de procesos a utilizar
   - `error_log /var/log/nginx/error.log`: Archivo de log de errores
   - `pid /run/nginx.pid`: Archivo de PID
   - `events`: Configuración de eventos
   - `http`: Configuración de HTTP
   - `upstream backend`: Configuración de los servidores backend
   - `server`: Configuración del servidor HTTP
   - `listen 80`: Puerto de escucha
   - `server_name _`: Nombre del servidor
   - `rewrite ^ https://$host$request_uri permanent;`: Redirección a HTTPS
   - `listen 443 ssl http2 default_server;`: Puerto de escucha
   - `server_name _;`: Nombre del servidor
   - `include /etc/nginx/ssl.conf;`: Incluye la configuración de SSL
   - `client_max_body_size 0;`: Tamaño máximo del cuerpo
   - `location /`: Configuración de la ubicación
   - `proxy_pass http://backend;`: Redirección al backend
   - `proxy_redirect off;`: Desactiva la redirección
   - `proxy_set_header Host $host;`: Configura la cabecera Host
   - `proxy_set_header X-Real-IP $remote_addr;`: Configura la cabecera X-Real-IP
   - `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`: Configura la cabecera X-Forwarded-For
   - `proxy_set_header X-Forwarded-Host $host;`: Configura la cabecera X-Forwarded-Host
   - `proxy_set_header X-Forwarded-Server $host;`: Configura la cabecera X-Forwarded-Server
   - `proxy_set_header X-Forwarded-Proto $scheme;`: Configura la cabecera X-Forwarded-Proto

1. Se debe crear el archivo de configuración de SSL en el directorio `loadbalancer`

   ```bash
   nano loadbalancer/ssl.conf
   ```

   ```nginx
   ## Version 2018/05/31 - Changelog: https://github.com/linuxserver/docker-letsencrypt/commits/master/root/defaults/ssl.conf

   # session settings
   ssl_session_timeout 1d;
   ssl_session_cache shared:SSL:50m;
   ssl_session_tickets off;

   # Diffie-Hellman parameter for DHE cipher suites
   # ssl_dhparam /etc/nginx/ssl/ssl-dhparams.pem;

   # ssl certs
   ssl_certificate /etc/nginx/ssl/fullchain.pem;
   ssl_certificate_key /etc/nginx/ssl/privkey.pem;

   # protocols
   ssl_protocols TLSv1.1 TLSv1.2;
   ssl_prefer_server_ciphers on;
   ssl_ciphers 'ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:ECDHE-ECDSA-AES128-SHA256:ECDHE-RSA-AES128-SHA:ECDHE-ECDSA-AES128-SHA:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES256-SHA:ECDHE-ECDSA-AES256-SHA:DHE-RSA-AES128-SHA256:DHE-RSA-AES128-SHA:DHE-RSA-AES256-SHA256:DHE-RSA-AES256-SHA:!aNULL:!eNULL:!EXPORT:!DES:!RC4:!MD5:!PSK:!aECDH:!EDH-DSS-DES-CBC3-SHA:!EDH-RSA-DES-CBC3-SHA:!KRB5-DES-CBC3-SHA';

   # HSTS, remove # from the line below to enable HSTS
   add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

   # OCSP Stapling
   ssl_stapling on;
   ssl_stapling_verify on;

   # Optional additional headers
   #add_header Content-Security-Policy "upgrade-insecure-requests";
   #add_header X-Frame-Options "SAMEORIGIN" always;
   #add_header X-XSS-Protection "1; mode=block" always;
   #add_header X-Content-Type-Options "nosniff" always;
   #add_header X-UA-Compatible "IE=Edge" always;
   #add_header Cache-Control "no-transform" always;
   #add_header Referrer-Policy "same-origin" always;
   ```

1. Se debe crear el archivo de docker compose en el directorio `loadbalancer`

   ```bash
   nano loadbalancer/docker-compose.yml
   ```

   ```yaml
   version: "3.1"
   services:
   nginx:
     container_name: nginx
     restart: always
     image: nginx
     volumes:
       - ./nginx.conf:/etc/nginx/nginx.conf:ro
       - ./ssl:/etc/nginx/ssl
       - ./ssl.conf:/etc/nginx/ssl.conf
     ports:
       - 80:80
       - 443:443
   ```

   Donde:

   - `container_name`: Nombre del contenedor
   - `restart`: Que siempre se reinicie el contenedor
   - `image`: Imagen de Nginx
   - `volumes`: Volumenes a montar
   - `ports`: Puertos a exponer
   - `./nginx.conf:/etc/nginx/nginx.conf:ro`: Monta el archivo de configuración de Nginx
   - `./ssl:/etc/nginx/ssl`: Monta el directorio de los certificados
   - `./ssl.conf:/etc/nginx/ssl.conf`: Monta el archivo de configuración de SSL
   - `80:80`: Expone el puerto 80
   - `443:443`: Expone el puerto 443

1. Se debe detener cualquier proceso de nginx

   ```bash
   ps ax | grep nginx
   netstat -an | grep 80

   sudo systemctl disable nginx
   sudo systemctl stop nginx
   exit
   ```

1. Se debe ejecutar el docker compose (cuando se vuelva a iniciar la sesión)

   ```bash
   cd loadbalancer
   docker-compose up -d
   ```
