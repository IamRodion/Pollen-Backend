# Ejemplo Práctico

A continuación se mostrará un ejemplo práctico de como utilizar la autenticación del backend con un código muy simple de python.

Lo primero es importar los requerimientos:

```python
import requests # Esta librería realizará las solicitudes http
import os # Esta librería se usará para obtener las variables de entorno
from dotenv import load_dotenv # Esta librería se usará para cargar el archivo .env que contendrá las variables de entorno que almacenarán los secretos que no queremos filtrar del código
```

Para esto se debe tener en cuenta que en la misma ruta del script existe `un archivo .env` que contiene los siguientes datos:

```
USERNAME="usuario"
PASSWORD="contraseña"
URL_API="https://ruta-a-la-api/"
```

Una vez tenemos las librerías necesarias, podemos cargar las variables de entorno:

```python
# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las credenciales del archivo .env
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
URL_API = os.getenv('URL_API')
```

Ahora podemos definir las funciones:

```python
def get_tokens():
    response = requests.post(URL_API+"api/token/", data={'username': USERNAME, 'password': PASSWORD})
    response.raise_for_status()  # Lanza un error si la solicitud no fue exitosa
    return response.json() # Devuelve la respuesta en formato json
```

La función `get_tokens()` realiza una solicitud _POST_ al endpoint **/api/token/** con los datos de autenticación obtenidos del archivo _.env_ y devuelve la respuesta en formato json, que como ya vimos serán el **Access Token** y el **Refresh Token**.

</br>

```python
def refresh_access_token(refresh_token):
    response = requests.post(URL_API+"api/token/refresh/", data={'refresh': refresh_token})
    response.raise_for_status()
    return response.json()['access']
```

La función `refresh_access_token(refresh_token)` toma como argumento el **Refresh Token** y realiza una solicitud _POST_ al endpoint **/api/token/refresh** con el **Refresh Token** en el cuerpo de la solicitud, y devuelve el valor bajo la llave `access` obtenido en la respuesta, el cual será un nuevo **Access Token**.

</br>

```python
def get_data(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(URL_API+"api/data/", headers=headers)
    if response.status_code == 401:  # Si el token de acceso ha expirado
        return None
    response.raise_for_status()
    return response.json()
```

La función `get_data(access_token)` toma como argumento el **Access Token** y realiza una solicitud _GET_ al endpoint **/api/data/** que en este ejemplo es un endpoint del backend protegido con autenticación. Esta solicitud se realiza con el **Access Token** en **el header de la solicitud** bajo la llave `Authorization` y con el texto `Bearer ` antes del **Access Token** como se indicó antes. En caso de obtener un error 401, la función entenderá que el **Access Token** ha caducado y se necesitará uno nuevo, así que devuelve None (Null). En caso de obtener una respuesta, la devolverá en formato json.

Con estas funciones definidas podemos definir una función main que controlará el flujo principal de las tareas:

```python
def main():
    tokens = get_tokens() # Se obtienen los 2 tokens en la variable tokens
    access_token = tokens['access'] # Se obtiene el access token
    refresh_token = tokens['refresh'] # Se obtiene el refresh token

    data = get_data(access_token) # Se intenta realizar la solicitud para obtener los datos protegidos por autenticación

    if data is None:  # Si el token de acceso ha expirado
        print("Access token expirado, refrescando...")
        access_token = refresh_access_token(refresh_token) # Se envía una solicitud para obtener un nuevo access token
        data = get_data(access_token) # Se realiza la solicitud con el nuevo access token

    print("Data:", data) # Se muestran los datos obtenidos

main() # Se llama a la función main
```

