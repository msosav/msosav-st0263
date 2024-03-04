# ST0263 Tópicos Especiales en Telemática

**Estudiante: Miguel Sosa, msosav@eafit.edu.co**

**Profesor: Edwin Montoya, emontoya@eafit.edu.co**

## P2P - Comunicación entre procesos mediante API REST, RPC y MOM

### 1. Breve descripción de la actividad

El reto consiste en implementar un sistema de subida y baja de archivos entre peers, utilizando una arquitectura de comunicación entre procesos mediante API REST y gRPC.

#### 1.1. Que aspectos cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

- Conexión entre peers mediante gRPC.
- Conexión pserver-server mediante API REST.
- Subida de archivos entre peers.
- Baja de archivos entre peers.
- Ping del pserver al server.
- Index de archivos en el pserver al server.
- Despliegue en AWS con Docker.
- Documentación.
- Diagrama de arquitectura.

#### 1.2. Que aspectos NO cumplió o desarrolló de la actividad propuesta por el profesor (requerimientos funcionales y no funcionales)

Se implementaron todas las funcionalidades requeridas.

### 2. Información general de diseño de alto nivel, arquitectura, patrones, mejores prácticas utilizadas.

#### 2.1. Arquitectura

El sistema está compuesto por tres componentes principales: el pclient, el pserver y el server. El pclient es el encargado de decirle al pserver que debe hacer, si hacer Login, Logout, Subir o Bajar archivos. El pserver es el encargado de manejar la conexión entre los peers y el server. El server es el encargado de manejar la subida y bajada de archivos entre los pservers manejando un index de los archivos que tiene cada pserver.

[Arquitectura]()

#### 2.2. Patrones

- Se utilizó el patrón de arquitectura P2P para la comunicación entre los peers.
- Se utilizó el patrón de arquitectura Cliente-Servidor para la comunicación entre el pserver y el server.

#### 2.3. Mejores prácticas

- Se utilizó siempre el mismo tipo de retorno, es decir, siempre se retorna un status y un mensaje (cuando se requiere).
- Se utilizó el protocolo gRPC para la comunicación entre los peers.
- Se utilizó el protocolo HTTP para la comunicación entre el pserver y el server.
- Se utilizó Docker para el despliegue en AWS.
- Se utilizó un archivo .env para manejar las variables de ambiente.
- Se manejó un ambiente virtual con Pipenv.
- Se utilizó un archivo requirements.txt para manejar las dependencias del proyecto a la hora de desplegarlo en AWS.

### 3. Descripción del ambiente de desarrollo y técnico: lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

- **Como se compila y ejecuta.**

  Se debe de tener instalado Python 3.12 y Pipenv.

  Para instalar las dependencias del proyecto se debe de correr el siguiente comando (en la raíz del proyecto):

  ```bash
  pipenv install
  ```

  - **Server**

  ```bash
  pipenv run python server/server.py <.env_server>
  ```

  - **Peer**

    La idea es correr el pclient con dos archivos .env, uno para el pclient y otro para el pserver.

    ```bash
    pipenv run python peer/pclient.py <.env_pclient> <.env_pserver>
    ```

    Además, para el correcto funcionamiento se debe tener dos peers corriendo en dos terminales diferentes.

- Detalles del desarrollo.
- Detalles técnicos
- Descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
- Opcional - detalles de la organización del código por carpetas o descripción de algún archivo. (ESTRUCTURA DE DIRECTORIOS Y ARCHIVOS IMPORTANTE DEL PROYECTO, comando 'tree' de linux)
  ```bash
    .
    ├── bootstrap
    ├── peer
    │   ├── Dockerfile
    │   ├── pclient.py
    │   ├── pserver_pb2_grpc.py
    │   ├── pserver_pb2.py
    │   ├── pserver_pb2.pyi
    │   └── pserver.py
    ├── Pipfile
    ├── Pipfile.lock
    ├── protobufs
    │   └── pserver.proto
    ├── README.md
    ├── requirements.txt
    └── server
        ├── Dockerfile
        └── server.py
  ```
- Opcional - si quiere mostrar resultados o pantallazos

### 4. Descripción del ambiente de ejecución (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

- IP o nombres de dominio en nube o en la máquina servidor.
- Descripción y como se configura los parámetros del proyecto (ej: ip, puertos, conexión a bases de datos, variables de ambiente, parámetros, etc)
- Como se lanza el servidor.
- Una mini guia de como un usuario utilizaría el software o la aplicación
- Opcional - si quiere mostrar resultados o pantallazos

### 5. Otra información que considere relevante para esta actividad.

#### Sustentación

<iframe width="560" height="315" src="https://www.youtube.com/embed/EmKVDCq57so?si=CwHbdLDMm2ZmxL6P" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Referencias:
