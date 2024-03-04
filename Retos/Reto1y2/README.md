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

  - **pserver.proto**

    Para compilar el archivo .proto se debe de correr el siguiente comando en el directorio _peer_:

    ```bash
    python -m grpc_tools.protoc -I ../protobufs --python_out=. --pyi_out=. --grpc_python_out=. ../protobufs/pserver.proto
    ```

  - **Server**

    Para correr el server se debe de correr el siguiente comando en el directorio _server_:

    ```bash
    pipenv run python server.py <.env_server>
    ```

  - **Peer**

    Para correr el peer se debe de correr el siguiente comando en el directorio _peer_:

    ```bash
    pipenv run python peer/pclient.py <.env_pclient> <.env_pserver>
    ```

    Además, para el correcto funcionamiento se debe tener dos peers corriendo en dos terminales diferentes con diferentes archivos de configuración.

- Detalles del desarrollo.
- Detalles técnicos

  - **Lenguaje de programación:** Python 3.12
  - **Librerías**:
    - flask==3.0.2
    - python-dotenv==1.0.1
    - requests==2.31.0
    - grpcio-tools==1.62.0
    - grpcio==1.62.0

- Descripción y como se configura los parámetros del proyecto.

  - **.env_server**

    ```bash
    SERVER_URL="localhost"
    SERVER_PORT=5000
    ```

  - **.env_pclient**

    ```bash
    PSERVER_URL="localhost"
    PSERVER_PORT="<PORT>"
    ```

  - **.env_pserver**

    ```bash
    PSERVER_URL="localhost"
    PSERVER_LOCAL_URL="localhost"
    PSERVER_PORT="<PORT>"
    SERVER_URL="localhost"
    SERVER_PORT=5000
    ```

- Estructura de directorios y archivos.

  ```bash
  .
  ├── bootstrap
  │   ├── .env_pclient1
  │   ├── .env_pclient2
  │   ├── .env_pserver1
  │   ├── .env_pserver2
  │   └── .env_server
  ├── peer
  │   ├── Dockerfile
  │   ├── pclient.py
  │   ├── pserver_pb2_grpc.py
  │   ├── pserver_pb2.py
  │   ├── pserver_pb2.pyi
  │   ├── pserver.py
  │   └── requirements.txt
  ├── Pipfile
  ├── Pipfile.lock
  ├── protobufs
  │   └── pserver.proto
  ├── README.md
  └── server
      ├── Dockerfile
      ├── requirements.txt
      └── server.py
  ```

### 4. Descripción del ambiente de ejecución (en producción) lenguaje de programación, librerias, paquetes, etc, con sus numeros de versiones.

- IP o nombres de dominio en nube o en la máquina servidor.

  - **Server:**
    - _IP:_ `54.174.42.217`
    - _PORT:_ `5000`
  - **Peer 1:**
    - _IP:_ `54.87.43.104`
    - _PORT:_ `5000`
  - **Peer 2:**
    - _IP:_ `54.87.43.104`
    - _PORT:_ `5001`

- Descripción y como se configura los parámetros del proyecto

  - **.env_server**

    ```bash
    SERVER_URL="0.0.0.0"
    SERVER_PORT=5000
    ```

  - **.env_pclient**

    ```bash
    PSERVER_URL="54.87.43.104"
    PSERVER_PORT="<PORT>"
    ```

  - **.env_pserver**

    ```bash
    PSERVER_URL="54.87.43.104"
    PSERVER_LOCAL_URL="0.0.0.0"
    PSERVER_PORT="<PORT>"
    SERVER_URL="54.174.42.217"
    SERVER_PORT=5000
    ```

- Como se lanza el servidor.

  **IMPORTANTE:** Para correr el peer se debe de tener instalado Docker.

  Para correr el server se debe de clonear el repositorio y correr el siguiente comando en el directorio _Retos/Reto1y2/server_:

  ```bash
  docker build -t server .
  docker run -p 5000:5000 server
  ```

- Una mini guia de como un usuario utilizaría el software o la aplicación

  **IMPORTANTE:** Para correr el peer se debe de tener instalado Docker. Además los siguientes comandos se deben de correr para cada peer.

  Para correr el peer se debe de clonear el repositorio y correr el siguiente comando en el directorio _Retos/Reto1y2/peer_ :

  ```bash
  docker build -t peer<N> .
  ```

  Luego debe de correr el contenedor con el siguiente comando:

  ```bash
  docker run -it -d -p <PORT>:<PORT> peer<N>
  ```

  Luego se debe acceder al contenedor con el siguiente comando:

  ```bash
  docker exec -it <CONTAINER_ID> /bin/bash
  ```

  Donde el `<CONTAINER_ID>` es el id del contenedor que se obtiene con el siguiente comando:

  ```bash
  docker ps
  ```

  Y dentro del contenedor correr el siguiente comando:

  ```bash
  python pclient.py <.env_pclient> <.env_pserver>
  ```

  Además, para el correcto funcionamiento se debe tener dos peers corriendo en dos terminales diferentes con diferentes archivos de configuración.

  - **Login:**

    Se ingresa el nombre de usuario y contraseña.

  - **Subir archivo:**

    Se indica la opción `1` y se ingresa el nombre del archivo que se quiere subir.

  - **Bajar archivo:**

    Se indica la opción `2` y se ingresa el nombre del archivo que se quiere bajar.

  - **Logout:**

    Se indica la opción `3`.

### 5. Otra información que considere relevante para esta actividad.

#### Sustentación

<iframe width="560" height="315" src="https://www.youtube.com/embed/EmKVDCq57so?si=CwHbdLDMm2ZmxL6P" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Referencias:

- [Python gRPC Tutorial - Create a gRPC Client and Server in Python with Various Types of gRPC Calls](https://youtu.be/WB37L7PjI5k?si=3V4YKClNlm_N-DW6)
- [Flask Documentation](https://flask.palletsprojects.com/en/3.0.x/)
- [How can I delete all local Docker images?](https://stackoverflow.com/questions/44785585/how-can-i-delete-all-local-docker-images)
- [Python Requirements.txt – How to Create and Pip Install Requirements.txt in Python](https://www.freecodecamp.org/news/python-requirementstxt-explained/)
