**V5.0: Cambios en el sprint final**

- Ahora el usuario puede importar una lista de peliculas vistas
- Ahora el usuario puede exportar su lista de peliculas vistas

- Ahora el usuario puede cancelar las operaciones añadir y editar pelicula

- Ahora el usuario puede validar una película:
	- Si el nombre es incorrecto y no se encuentran similares se avisa
	- Si el nombre es incorrento y se encuentran similares, se muestran

- Ahora dialog tiene su propia clase(aumento de modularidad) 

- Inclusion de CP
- Las llamadas a la API ahora las realiza un thread:
	- Mientras un spinner indica al usuario que espere
	- Se pueden realizar operaciones de añadir, exportar y cambiar vista
	- No se pueden borrar, editar, marcar como vistas, importar o validar peliculas

- La API ahora tiene un limite de conexion

- Al cerrar la aplicacion se envía una señal a los threads activos:
	- Pueden tardar un poco en cerrarse

- Se elimina el boton validate
