# JumpServer

El jump server es un servidor que se utiliza para acceder a otros servidores con ip privadas.

## Especificaciones

- **AMI:** Ubuntu Server 20.04 LTS.
- **Key Pair:** la clave pem utilizada en el reto 3.
- **VPC:** VPC creada en el reto 3.
- **Subnet:** Subnet pública.
- **Asignación de IP:** Asignar una IP pública.
- **Puerto SSH:** 22.

## Configuración

Para copiar la clave pem a jump server se debe ejecutar el siguiente comando:

```bash
scp -i "Reto3.pem" ./Reto3.pem ubuntu@<id_aws>:~
```
