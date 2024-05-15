# Laboratorio 0

## Notas

### Al borrar un cluster

1. Se debe crear un nuvo usuario de hadoop

1. Se debe cambiar el puerto de hue de 14000 a 9870

   1. Conectase con el nodo master del cluster

   2. Editar el archivo `/etc/hue/conf/hue.ini`

      ```bash
      vi /etc/hue/conf/hue.ini
      ```

   3. Cambiar el puerto de `14000` a `9870`, buscar `/hdfs_clusters` y cambiar el puerto

      ```bash
      webhdfs_url=http://...:9870/webhdfs/v1
      ```

   4. Reiniciar el servicio de hue

      ```bash
      systemctl restart hue.service
      ```

### En Jupyter Hub

Si no funciona spark, se debe reiniciar el kernel
