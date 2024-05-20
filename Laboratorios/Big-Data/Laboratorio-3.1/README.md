# ST0263 Tópicos Especiales en Telemática

**Estudiante: Miguel Sosa, msosav@eafit.edu.co**

**Profesor: Edwin Montoya, emontoya@eafit.edu.co**

## Laboratorio 3.1: Gestión de archivos en HDFS y S3 para Big Data

### 1. Breve descripción de la actividad

En este laboratorio se realizará la gestión de archivos en HDFS y S3 para Big Data. Se realizarán las siguientes actividades:

- Copiar (gestión) de archivos hacia el HDFS vía HUE.
- Copiar (gestión) de archivos hacia el HDFS vía SSH.
- Copiar (gestión) de archivos hacia AWS S3 vía HUE.
- Copiar (gestión) de archivos hacia el AWS S3 vía SSH.

#### 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

- [x] Copiar (gestión) de archivos hacia el HDFS vía HUE.
- [x] Copiar (gestión) de archivos hacia el HDFS vía SSH.
- [x] Copiar (gestión) de archivos hacia AWS S3 vía HUE.
- [x] Copiar (gestión) de archivos hacia el AWS S3 vía SSH.

#### 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

No se dejó ningún aspecto sin cumplir.

### 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

Para el desarrollo del laboratorio se utilizó el servicio de **Amazon EMR** para la creación de un cluster de Hadoop. Se utilizó el servicio de **HUE** para la gestión de archivos en HDFS y **S3**.

### 3. Desarrollo del laboratorio

Para el desarrollo del laboratorio se realizaró lo siguiente:

1. Crear un cluster siguiendo [las instrucciones del laboratorio 0](https://github.com/st0263eafit/st0263-241/tree/main/bigdata/00-lab-aws-emr).

2. Cambiar el puerto de HDFS de 14000 a 9870

   1. Conecatarse con el nodo master del cluster

      ```bash
      ssh -i "vockey.pem" ec2-user@...
      ```

   2. Editar el archivo `/etc/hue/conf/hue.ini`

      ```bash
      sudo vi /etc/hue/conf/hue.ini
      ```

   3. Cambiar el puerto de `14000` a `9870`, buscar `/hdfs_clusters` y cambiar el puerto

      ```bash
      webhdfs_url=http://...:9870/webhdfs/v1
      ```

   4. Reiniciar el servicio de hue

      ```bash
      sudo systemctl restart hue.service
      ```

#### 3.1. Copiar (gestión) de archivos hacia el HDFS vía HUE.

1.  Ingresar a HUE.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/c047ebe8-56f5-47c1-8f33-181a5ba94601">
    </p>

2.  Ingresar con el usuario `hadoop` y la contraseña configurada.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/4271e68c-81a1-4621-afea-82749e869249" />
    </p>

3.  Ir a la sección de `Files`.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/1e50a81b-a9a7-4848-b84e-0de520b88cac" />
    </p>

4.  Darle a `New` y seleccionar `Directory`.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/0e7e12b9-7790-45e2-a232-71cede7f237c" />
    </p>

5.  Crear un directorio `datasets`.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/5455d9fd-602a-4de3-a992-7675fdd691ca" />
    </p>

6.  Crear un directorio `gutenberg-small` dentro de `datasets`.

7.  Subir los archivos del dataset `gutenberg-small` a la carpeta `datasets`.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/8ddc553d-d5a1-4bf9-99be-64b04731aef0" />
    </p>

8.  Listar los archivos en HDFS para verificar que se copiaron correctamente.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/a0fbc36b-ceae-4ce0-9f3f-35cc6c4ba45e" />
    </p>

#### 3.2. Copiar (gestión) de archivos hacia el HDFS vía SSH.

_Nota: se debe hacer en el nodo master del cluster EMR_

1. Conectarse con el nodo master del cluster.

   ```bash
   ssh -i "vockey.pem" hadoop@...
   ```

1. Crear un directorio `datasets` en HDFS.

   ```bash
   hdfs dfs -mkdir /user/hadoop/datasets
   ```

1. Crear un directorio `gutenberg-small` en HDFS.

   ```bash
   hdfs dfs -mkdir /user/hadoop/datasets/gutenberg-small
   ```

1. Copiar los archivos del dataset `gutenberg-small` a la carpeta `gutenberg-small`.

   ```bash
   hdfs dfs -put $HOME/st0263-241/bigdata/datasets/gutenberg-small/*.txt /user/hadoop/datasets/gutenberg-small/
   ```

1. Listar los archivos en HDFS para verificar que se copiaron correctamente.

   ```bash
   hdfs dfs -ls /user/hadoop/datasets/gutenberg-small/
   ```

#### 3.3. Copiar (gestión) de archivos hacia AWS S3 vía HUE.

1.  Crear un bucket llamado `datasets-lab3-1`.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/bb6a7796-8e55-410b-a35e-1e2c71a5a36a" />
    </p>

1.  Ir al bucket `datasets-lab3-1`.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/af5fbe68-19d2-47dc-8229-f33055270779" />
    </p>

1.  Ir a `Permissions`

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/233197ed-af1f-4f9f-9e68-38effed6efba" />
    </p>

1.  Editar `Block public access (bucket settings)` y desmarcar `Block all public access`.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/86c1f229-6825-4b22-a2c2-e70ff4d8ebcd" />
    </p>

1.  Cambiar la política del bucket para que sea público.

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Sid": "PublicReadGetObject",
          "Effect": "Allow",
          "Principal": "*",
          "Action": ["s3:GetObject"],
          "Resource": ["arn:aws:s3:::datasets-lab3-1/*"]
        }
      ]
    }
    ```

1.  Guardar la política.

1.  Ingresar a HUE de la misma forma que en el paso 3.1.

1.  Ir a la sección de S3.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/9bb98e5e-0b00-4ef1-b137-e9319e1aeed3" />
    </p>

1.  Seleccionar el bucket `datasets-lab3-1`.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/c1b45f61-ebe4-47b6-8cb3-921d251e8f6e" />
    </p>

1.  Crear un directorio llamado `gutenberg-small`.

1.  Subir los archivos del dataset `gutenberg-small` a la carpeta `gutenberg-small`.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/98788b09-721a-431b-be18-b5490e00372b" />
    </p>

1.  Listar los archivos en S3 para verificar que se copiaron correctamente.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/c03de421-d920-45a2-8685-0442fd943a31" />
    </p>

#### 3.4. Copiar (gestión) de archivos hacia el AWS S3 vía SSH.

1.  Conectar por SSH al nodo master del cluster.

    ```bash
    ssh -i "vockey.pem" ec2-user@...
    ```

1.  Clonar el repositorio de la materia.

    ```bash
    git clone https://github.com/st0263eafit/st0263-241.git
    ```

1.  Copiar los archivos del dataset `gutenberg-small` a S3.

    ```bash
    aws s3 cp $HOME/st0263-241/bigdata/datasets/gutenberg-small s3://datasets-lab3-1/gutenberg-small-ssh --recursive
    ```

1.  Listar los archivos en S3 para verificar que se copiaron correctamente.

    ```bash
    aws s3 ls s3://datasets-lab3-1/gutenberg-small-ssh/
    ```

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/d95b03b1-924d-46ad-861b-41fd7d83e954" />
    </p>

## Referencias

- [ST0263 Tópicos Especiales en Telemática]()
- [How to Make an S3 Bucket Public](https://saturncloud.io/blog/how-to-make-an-s3-bucket-public/)
- [Uploading files to S3 account from Linux command line](https://superuser.com/questions/279986/uploading-files-to-s3-account-from-linux-command-line)
