# ST0263 Tópicos Especiales en Telemática

- **Estudiante: Miguel Sosa, msosav@eafit.edu.co**
- **Estudiante: Miguel Jaramillo, mjaramil20@eafit.edu.co**
- **Estudiante: Sergio Córdoba, sacordobam@eafit.edu.co**

**Profesor: Edwin Montoya, emontoya@eafit.edu.co**

## Nombre de la actividad

### 1. Breve descripción de la actividad

Desplegar WordPress empleando la tecnología de contenedores, con su **propio dominio** y **certificado SSL**. El sitio lo llamará: reto3._sudominio.tld_.

En este reto se utilizará un nginx como **balanceador de cargas** de la capa de aplicación del wordpress o aplicación monolítica elegida.

Además de lo anterior, se utilizarán 2 servidores adicionales, uno para base de datos (DBServer) y otro para archivos (FileServer). El DBServer podrá utilizar la BD en **docker** (recomendado) o nativa. Y el FileServer implementará un **NFSServer**.

#### 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

- [x] Desplegar WordPress empleando la tecnología de contenedores.
- [x] Propio dominio y certificado SSL.
- [x] Balanceador de cargas.
- [x] Servidores adicionales para base de datos y archivos.
- [x] Dos instancias de WordPress.

#### 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Se cumplió con todos los requerimientos propuestos por el profesor.

### 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

#### Arquitectura

<div align="center">
<img src="https://github.com/msosav/msosav-st0263/assets/85181687/3e5194f6-8385-4c67-8fca-c739c2781efb" />
</div>

### 3. Descripción del ambiente de ejecución (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

#### Dominio

https://reto3.temporaladventures.tech

> [!NOTE]
> Solo funcionará la MV durante 4 horas. Entonces lo más seguro es que no funcione a la hora de probarlo.

#### VPC

[Configuración](https://github.com/msosav/msosav-st0263/blob/main/Retos/Reto3/VPC/README.md)

#### JumpServer

- **AMI:** Ubuntu Server 20.04 LTS.
- **Key Pair:** la clave pem utilizada en el reto 3.
- **VPC:** VPC creada en el reto 3.
- **Subnet:** Subnet pública.
- **Asignación de IP:** Asignar una IP pública.
- **Puerto SSH:** 22.

[Configuración](https://github.com/msosav/msosav-st0263/blob/main/Retos/Reto3/JumpServer/README.md)

#### NFS

- **AMI:** Ubuntu Server 20.04 LTS.
- **Key Pair:** la clave pem utilizada en el reto 3.
- **VPC:** VPC creada en el reto 3.
- **Subnet:** Subnet privada.
- **Puerto SSH:** 22.
- **Puerto NFS:** 2049.

[Configuración](https://github.com/msosav/msosav-st0263/blob/main/Retos/Reto3/NFS/README.md)

#### Database

- **AMI:** Ubuntu Server 20.04 LTS.
- **Key Pair:** la clave pem utilizada en el reto 3.
- **VPC:** VPC creada en el reto 3.
- **Subnet:** Subnet privada.
- **Puerto SSH:** 22.
- **Puerto MySQL:** 3306.

[Configuración](https://github.com/msosav/msosav-st0263/tree/main/Retos/Reto3/Database)

#### WordPress

- **AMI:** Ubuntu Server 20.04 LTS.
- **Key Pair:** la clave pem utilizada en el reto 3.
- **VPC:** VPC creada en el reto 3.
- **Subnet:** Subnet privada.
- **Puerto SSH:** 22.
- **Puerto HTTP:** 80.

[Configuración](https://github.com/msosav/msosav-st0263/tree/main/Retos/Reto3/Wordpress)

#### Load Balancer

- **AMI:** Ubuntu Server 20.04 LTS.
- **Key Pair:** la clave pem utilizada en el reto 3.
- **VPC:** VPC creada en el reto 3.
- **Subnet:** Subnet pública.
- **Asignación de IP:** IP pública.
- **Puerto SSH:** 22.
- **Puerto HTTP:** 80.
- **Puerto HTTPS:** 443.

[Configuración](https://github.com/msosav/msosav-st0263/tree/main/Retos/Reto3/Load%20Balancer)

#### Pantallazos

<div align="center">
<img src="https://github.com/msosav/msosav-st0263/assets/85181687/4b9794f9-9e6e-418f-b68c-8748a5e5937a" />
</div>

### 4. Otra información que considere relevante para esta actividad.

[Video]()

## Referencias:

- [Repositorio base](https://github.com/st0263eafit/st0263-241)
- [How To Set Up an NFS Mount on Ubuntu 20.04](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-ubuntu-20-04)
