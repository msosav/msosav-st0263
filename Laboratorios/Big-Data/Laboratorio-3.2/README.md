# ST0263 Tópicos Especiales en Telemática

**Estudiante: Miguel Sosa, msosav@eafit.edu.co**

**Profesor: Edwin Montoya, emontoya@eafit.edu.co**

## Laboratorio 3.2: Implementación de un Data Warehouse sencillo con AWS S3, Glue y Athena

### 1. Breve descripción de la actividad

En este laboratorio, se implementará un Data Warehouse sencillo en AWS utilizando los servicios S3, Glue y Athena. Se creará un bucket en S3 para almacenar los datos, se creará una base de datos y tablas en Glue para catalogar los datos y se realizarán consultas SQL en Athena para analizar los datos almacenados.

#### 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

- [x] Crear un bucket en S3 para almacenar los datos.
- [x] Crear una base de datos y tablas en Glue para catalogar los datos.
- [x] Realizar consultas SQL en Athena para analizar los datos almacenados.

#### 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Todas las actividades propuestas fueron cumplidas.

### 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

Para el desarrollo del laboratorio se utilizó la siguiente arquitectura:

- **S3**: Almacenamiento de los datos.
- **Glue**: Catalogación de los datos.
- **Athena**: Consultas SQL.

### 3. Desarrollo

Para el desarrollo del laboratorio se realizaró lo siguiente:

1. Crear un bucket en S3 para almacenar los datos.

   - Nombre: `msosavlabs`.
   - `ACLs enabled` seleccionado.
   - `Block all public access` sin marcar.

2. Subir los datos de `onu2` a S3.

   - Debe contener dos carpetas `export` y `hdi`. Cada una con sus respectivos archivos.

    <p align="center">
      <img src="https://github.com/msosav/msosav-st0263/assets/85181687/46636d7d-d32f-4161-98a3-ce30e351a550"/>
    </p>

3. Ir a Glue.

4. Ir a `Crawlers` y crear un nuevo crawler.

   - Paso 1:
     - Nombre: `msosav-crawler`.
   - Paso 2:
     - Seleccionar `Data stores`.
     - Seleccionar `S3`.
     - Especificar la ruta del bucket `msosavlabs`. En este caso, `s3://msosavlabs/onu2`.
     - Añadirlo.
   - Paso 3:
     - Seleccionar `LabRole`.
   - Paso 4:
     - Seleccionar `Add database`.
     - Nombre: `msosav-db`.
     - Crear el crawler.

5. Ejecutar el crawler.

6. Ir a `S3` y seleccionar el bucket `msosavlabs`.

7. Crear un nuevo directorio `athena`.

   <p align="center">
     <img src="https://github.com/msosav/msosav-st0263/assets/85181687/bec22524-2108-483b-9f3d-1641773a62e5" />
    </p>

8. Ir a `Glue` y verificar que el crawler haya creado la base de datos `msosav-db` y las tablas.

   <p align="center">
     <img src="https://github.com/msosav/msosav-st0263/assets/85181687/f1644e5a-ff78-4b58-aca1-5e46bb312f63" />
    </p>

9. Revisar que la base de datos y las tablas estén creadas.

   <p align="center">
     <img src="https://github.com/msosav/msosav-st0263/assets/85181687/c4fcda39-fd75-404d-b9ad-ff6b80ea576c" />
    </p>

10. Ir a `Athena`.

11. Si aparece un mesaje diciendo _Before you run your first query, you need to set up a query result location in Amazon S3._, seleccionar `Edit settings`.

    - Seleccionar el bucket `msosavlabs`.
    - Seleccionar el directorio `athena`.

    La ruta debe ser `s3://msosavlabs/athena`.

12. En `Athena`, seleccionar la base de datos `msosav-db`.

13. Realizar consultas SQL.

    - Consulta 1:

      ```sql
      SELECT * FROM export LIMIT 10;
      ```

        <p align="center">
           <img src="https://github.com/msosav/msosav-st0263/assets/85181687/67b2f786-1d7a-43f1-b20c-86e4e50ec3e4" />
        </p>

    - Consulta 2:

      ```sql
      SELECT * FROM hdi WHERE lifeex < 60 LIMIT 10;
      ```

        <p align="center">
        <img src="https://github.com/msosav/msosav-st0263/assets/85181687/72c46a4d-ca82-465c-ba3f-98823d232201" />
        </p>

## Referencias

- [Repositorio de la materia](https://github.com/st0263eafit/st0263-241/tree/main)
- [Laboratorio de AWS S3 - Glue - Athena](https://www.youtube.com/watch?v=VbyVaAMF9EA)
