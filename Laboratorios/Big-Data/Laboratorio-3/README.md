# ST0263 Tópicos Especiales en Telemática

**Estudiante: Miguel Sosa, msosav@eafit.edu.co**

**Profesor: Edwin Montoya, emontoya@eafit.edu.co**

## Laboratorio 3: HIVE y SparkSQL, gestión de datos via SQL

### 1. Breve descripción de la actividad

En este laboratorio, se gestionarán y consultarán datos utilizando HIVE y SparkSQL en un entorno Hadoop, accesible a través de HUE en Amazon EMR. Se crearán tablas para almacenar datos de desarrollo humano (HDI) y exportaciones, tanto en HDFS como en S3. Los datos serán cargados y consultados usando comandos SQL, incluyendo operaciones de selección, filtrado y joins.

#### 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

- [x] Crear tablas en HIVE y SparkSQL para almacenar datos de desarrollo humano (HDI) y exportaciones.
- [x] Cargar datos en las tablas creadas.
- [x] Consultar datos usando comandos SQL, incluyendo operaciones de selección, filtrado y joins.

#### 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

### 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

### 3. Desarrollo

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

3. Ingresar a HUE. En el navegador, ingresar la dirección del nodo master del cluster seguido del puerto `8888`.

   ```bash
   http://ec2-...compute.amazonaws.com:8888
   ```

4. Ingresar con el usuario `hadoop` y la contraseña configurada.

   <p align="center">
   <img src="https://github.com/msosav/msosav-st0263/assets/85181687/4271e68c-81a1-4621-afea-82749e869249" />
   </p>

5. Ir a la sección de `Files`.

   <p align="center">
   <img src="https://github.com/msosav/msosav-st0263/assets/85181687/1e50a81b-a9a7-4848-b84e-0de520b88cac" />
   </p>

6. Darle a `New` y seleccionar `Directory`.

   <p align="center">
   <img src="https://github.com/msosav/msosav-st0263/assets/85181687/0e7e12b9-7790-45e2-a232-71cede7f237c" />
   </p>

7. Crear un directorio `datasets`.

   <p align="center">
   <img src="https://github.com/msosav/msosav-st0263/assets/85181687/5455d9fd-602a-4de3-a992-7675fdd691ca" />
   </p>

8. Crear un directorio `onu` dentro de `datasets`.

9. Crear un directorio `hdi` dentro de `onu`.

10. Subir los archivos `hdi-data.csv` y `export-data.csv` a la carpeta `hdi`.

    <p align="center">
    <img src="https://github.com/msosav/msosav-st0263/assets/85181687/ac613daa-d598-4a83-8f95-fd66e98fb5f4" />
    </p>

11. Conectarse con el nodo master del cluster.

    ```bash
    ssh -i "vockey.pem" hadoop@<dns-publica-nodo-master>
    ```

12. Cambiar los permisos de los archivos `hdi-data.csv` y `export-data.csv`.

    ```bash
    hdfs dfs -chmod -R 777 /user/hadoop/datasets/onu/hdi
    ```

13. Acceder a `beeline` para ejecutar comandos SQL.

    ```bash
    beeline
    ```

14. Conectarse a la instancia de HIVE.

    ```sql
    !connect jdbc:hive2://ec2-54-85-91-65.compute-1.amazonaws.com:10000/default
    ```

    Y crear un usuario.

15. Crear la base de datos `msosavdb` (si no existe).

    ```sql
    CREATE DATABASE IF NOT EXISTS msosavdb;
    ```

16. Crear la tabla `hdi` en la base de datos `msosavdb`.

    ```sql
    USE msosavdb;
    ```

    ```sql
    CREATE TABLE HDI (
        id INT,
        country STRING,
        hdi FLOAT,
        lifeex INT,
        mysch INT,
        eysch INT,
        gni INT
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    STORED AS TEXTFILE;
    ```

17. Cargar los datos del archivo `hdi-data.csv` en la tabla `hdi`.

    ```sql
    LOAD DATA INPATH '/user/hadoop/datasets/onu/hdi/hdi-data.csv' INTO TABLE msosavdb.hdi;
    ```

18. Crear la tabla `export` en la base de datos `msosavdb`.

    ```sql
    CREATE TABLE EXPORT (
        country STRING,
        expct FLOAT
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY ','
    STORED AS TEXTFILE;
    ```

19. Cargar los datos del archivo `export-data.csv` en la tabla `export`.

    ```sql
    LOAD DATA INPATH '/user/hadoop/datasets/onu/hdi/export-data.csv' INTO TABLE msosavdb.export;
    ```

20. Consultar los datos de la tabla `hdi`.

    ```sql
    SELECT * FROM msosavdb.hdi;
    ```

21. Consultar los datos de la tabla `export`.

    ```sql
    SELECT * FROM msosavdb.export;
    ```

22. Realizar un join entre las tablas `hdi` y `export`.

    ```sql
    SELECT h.country, gni, expct FROM HDI h JOIN EXPO e ON (h.country = e.country) WHERE gni > 2000;
    ```

## Referencias

- [Repositorio de la materia](https://github.com/st0263eafit/st0263-241/tree/main)
