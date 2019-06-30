#######Grupo 70##########
#######Entrega 4 ##########

#La entrega fue realizada entera, todas las consultas deberían funcionar
#Supuestos:
- A los mensajes fue necesario agregales un id único a cada uno. Para realizar esto los datos fueron convertidos desde json a csv con la página https://json-csv.com/. Al documento generado   se agrego una columna id  y luego ese documento de excel se transformó a json, al igual que los usuarios. Para esto utilizamos la página http://www.convertcsv.com/csv-to-json.htm. Así, obtuvimos ambos documento en json  a utilizar, cada uno con sus id correspondientes.
- Para pasar los datos de los usuarios de la base de datos relacional, que estaban contenidos en un documento de Excel a json lo metimos a una wea en internet q te lo hacia solo y ahi el archivo json a mongodb
- En la consulta en la que piden "agregar una o más frases que si o si deben estar en el mensaje", las frases deben ser entregadas separadas por guiones
- La consulta en la que se pide "agregar una o más frases que deseablemente deben estar " se realizó basándose en la respuesta del issue #122, donde se indica que no deben utilizarse comillas dobles para obtener palabras que se desean que esten, pero que no es estrictamente necesario.
- En la consulta que se pide "agregar un conjunto de palabras que no pueden estar en el mensaje", los resultados son todos aquellos mensajes que no contienen **ninguna** de las palabras de dicho conjunto. Es decir, si algún mensaje contiene algunas, pero no todas, de las palabras que no pueden estar, también es parte del resultado.


## Para correr la aplicación

### Windows con una sola version de python
En primer lugar se debe cargar la base de datos. Esto se hace en la terminal en la carpeta donde estan los archivos, incluyendo el ```main.py```.  Los comandos utilizados son:
1. mongoimport --db entrega4 --collection usuarios --drop --file usuarios1.json --jsonArray
2. mongoimport --db entrega4 --collection mensajes --drop --file messages1.json --jsonArray
Los archivos  usuarios1.json y messages1.json son los que hemos entregados adjuntos.
Además, es necesario tener corriendo en otra consola el servidor de mongo. La ubicación  Para realizar esto, se debe correr el comando "mongod".
Luego, se debe correr el archivo ```main.py``` en la misma consola en que se corrieron los comandos 1 y 2. Para hacer esto se utiliza el comando :
- python main.py
