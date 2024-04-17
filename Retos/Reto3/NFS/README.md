# NFS

## Especificaciones

- **AMI:** Ubuntu Server 20.04 LTS.
- **Key Pair:** la clave pem utilizada en el reto 3.
- **VPC:** VPC creada en el reto 3.
- **Subnet:** Subnet privada.
- **Puerto SSH:** 22.
- **Puerto NFS:** 2049.

## Prerequisitos

Para conectase a esta máquina es necesario conectarse desde el JumpServer.

## Configuración

1. Instalar el paquete `nfs-kernel-server`:

   ```bash
   sudo apt update
   sudo apt install nfs-kernel-server -y
   ```

1. Crear el directorio de wordpress:

   ```bash
   sudo mkdir -p /mnt/wordpress
   ```

1. Cambiar el propietario del directorio:

   ```bash
   sudo chown nobody:nogroup /mnt/wordpress
   ```

1. Cambiar los permisos del directorio:

   ```bash
    sudo chmod 777 /mnt/wordpress
   ```

1. Cambiar los exports

   ```bash
   sudo nano /etc/exports
   ```

   ```plaintext
   /mnt/wordpress *(rw,sync,no_subtree_check)
   ```

1. Reiniciar el servicio de NFS:

   ```bash
    sudo systemctl restart nfs-kernel-server
   ```

1. Activar el firewall:

   ```bash
   sudo ufw enable
   ```

1. Agregar la regla para el NFS:

   ```bash
    sudo ufw allow nfs
   ```

1. Agregar la regla para el ssh:

   ```bash
   sudo ufw allow ssh
   ```

## Referencias

- [How To Set Up an NFS Mount on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-20-04)
