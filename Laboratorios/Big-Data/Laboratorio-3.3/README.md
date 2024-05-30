# ST0263 Tópicos Especiales en Telemática

**Estudiante: Miguel Sosa, msosav@eafit.edu.co**

**Profesor: Edwin Montoya, emontoya@eafit.edu.co**

## Laboratorio 3.3: Implementación de un Data Warehouse con AWS Redshift y Redshift Spectrum

### 1. Breve descripción de la actividad

En este laboratorio, se implementará un Data Warehouse en AWS utilizando los servicios Redshift y Redshift Spectrum. Se creará un cluster de Redshift, se configurará el acceso a Redshift Spectrum y se realizarán consultas SQL en Redshift para analizar los datos almacenados en S3.

#### 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

- [x] Crear un cluster de Redshift.
- [x] Configurar el acceso a Redshift Spectrum.
- [x] Realizar consultas SQL en Redshift para analizar los datos almacenados en S3.

#### 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Sí se cumplieron todos los requerimientos propuestos.

### 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

Para el desarrollo del laboratorio se utilizó la siguiente arquitectura:

- **Redshift**: Data Warehouse.
- **Redshift Spectrum**: Consultas SQL en S3.
- **S3**: Almacenamiento de los datos.

### 3. Desarrollo

Para el desarrollo del laboratorio se realizaró lo siguiente:

1.  Crear un cluster de Redshift con las siguientes características:

    - Nombre: `msosav-cluster`.
    - Tipo: `dc2.large`.
    - Número de nodos: `1`.
    - Load sample data: `Si`.
    - Admin user name: `msosav`.
    - Associated IAM roles: `LabRole` y `myRedshiftRole`.

2.  Verificar la creación del cluster.

    <p align="center">
      <img src="https://github.com/msosav/msosav-st0263/assets/85181687/92a375bb-296f-4ae3-b13a-4041b3443656"/>
    </p>

3.  Ir al cluster de Redshift y seleccionar `Query editor v2`.

4.  Seleccionar `msosa-cluster` (conectarse con las credenciales creadas anteriormente) -> `sample_data_dev` -> `tickit` -> `Open sample notebooks`.

    _Nota: Si aparece un mensaje de "Create sample database", seleccionar `Create`._

5.  Correr las consultas SQL en el notebook.

    <p align="center">
      <img src="https://github.com/msosav/msosav-st0263/assets/85181687/35389a41-ae8d-49f3-bd36-53e94e71efa8"/>
    </p>

6.  Ir a `IAM` -> `Roles` -> `LabRole` y copiar el ARN. Ejemplo: `arn:aws:iam::590183684845:role/LabRole`.

7.  Ir a `Redshift` -> `Clusters` -> `New query`.

8.  Crear una tabla externa en Redshift Spectrum.

    ```sql
    CREATE EXTERNAL SCHEMA IF NOT EXISTS spectrum_schema
    FROM DATA CATALOG
    DATABASE 'myspectrum_db'
    IAM_ROLE 'arn:aws:iam::590183684845:role/LabRole'
    CREATE EXTERNAL DATABASE IF NOT EXISTS;
    ```

    <p align="center">
      <img src="https://github.com/msosav/msosav-st0263/assets/85181687/e8c46027-a1d4-412a-bd72-5c25c3212b6f"/>
    </p>

9.  Añadir la carpeta de `tickitdb` al bucket de S3 creado en el laboratorio 3.2.

    <p align="center">
      <img src="https://github.com/msosav/msosav-st0263/assets/85181687/54e1ec14-f517-425b-9588-b782f89b4a45" />
    </p>

10. Crear una tabla en Redshift Spectrum.

    ```sql
    CREATE EXTERNAL TABLE spectrum_schema.sales
    (
      salesid integer,
        listid integer,
        sellerid integer,
        buyerid integer,
        eventid integer,
        dateid smallint,
        qtysold smallint,
        pricepaid decimal(8,2),
        commission decimal(8,2),
        saletime timestamp
    )
    ROW FORMAT DELIMITED
    FIELDS TERMINATED BY '\t'
    STORED AS TEXTFILE
    LOCATION 's3://msosavlabs/tickitdb/sales'
    TABLE PROPERTIES ('numRows'='172000');
    ```

11. Verificar la creación de la tabla.

    ```sql
    SELECT * FROM spectrum_schema.sales LIMIT 10;
    ```

    <p align="center">
      <img src="https://github.com/msosav/msosav-st0263/assets/85181687/5f743032-3723-4757-bd1f-2cd573021c6d"/>
    </p>

12. Crear una tabla en Redshift.

    ```sql
    CREATE TABLE event2
    (
        eventid integer not null distkey,
        venueid smallint not null,
        catid smallint not null,
        dateid smallint not null sortkey,
        eventname varchar(200),
        starttime timestamp
    );
    ```

13. Insertar datos en la tabla.

    ```sql
    COPY event2 FROM 's3://msosavlabs/tickitdb/allevents_pipe.txt'
    IAM_ROLE 'arn:aws:iam::590183684845:role/LabRole'
    DELIMITER '|';
    TIMEFORMAT 'YYYY-MM-DD HH:MI:SS'
    REGION 'us-east-1';
    ```

14. Verificar la inserción de datos.

    ```sql
    SELECT * FROM event2 LIMIT 10;
    ```

    <p align="center">
      <img src="https://github.com/msosav/msosav-st0263/assets/85181687/06e6bf7c-306a-4040-becc-16027f6af0d1" />
    </p>

15. Realizar consultas SQL con tablas externas y nativas.

    ```sql
    SELECT TOP 10 spectrum_schema.sales.eventid, SUM(spectrum_schema.sales.pricepaid)
    FROM spectrum_schema.sales, event2
    WHERE spectrum_schema.sales.eventid = event2.eventid
    AND spectrum_schema.sales.pricepaid > 30
    GROUP BY spectrum_schema.sales.eventid
    ORDER BY 2 DESC;
    ```

    <p align="center">
      <img src="https://github.com/msosav/msosav-st0263/assets/85181687/67a297a8-ce5f-42bf-a436-1e333808f39b" />
    </p>

## Referencias

- [Repositorio de la materia](https://github.com/st0263eafit/st0263-241/tree/main)
- [Datos de ejemplo de Amazon Redshift](https://docs.aws.amazon.com/redshift/latest/gsg/samples/tickitdb.zip)
