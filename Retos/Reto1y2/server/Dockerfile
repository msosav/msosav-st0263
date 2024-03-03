# start by pulling the python image
FROM python:3.12-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# copy the server config into the image
COPY ./.env_server /app/.env_server
RUN export $(cat .env_server | xargs)

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["python", "server.py", ".env_server"]