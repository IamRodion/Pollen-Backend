# Autenticación

En el backend se implementará JWT para manejar la autenticación del usuario. Esta autenticación funcionará con 2 tokens, un **token de acceso** y un **token de refresco**.

Para el manejo de estos tokens, el backend tendrá a disposición los siguientes **endpoints**:

- /api/token/
- /api/token/refresh/

## /api/token/

#### Cuerpo de la Solicitud

Este endpoint se debe utilizar a través del método **POST** y en el cuerpo de la solicitud deben estar los datos 'username' y 'password' de la siguiente forma:

```json
{
  "username": "usuario_correcto",
  "password": "contraseña_correcta"
}
```

#### Solicitud Correcta

Al enviar una solicitud correctamente, el cuerpo de la respuesta se verá como este:

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NTY3ODkwLCJ1c2VyX3R5cGUiOiJ1c2VyIiwicm9sZSI6InVzZXIiLCJleHBpcmVkX3N0YWdlX2lkIjoxMjM0NTY3ODkwfQ.3gHkJnlD8U5Xg0of2h_mV7XfiRtOqPSkLNY-XpF53gs",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NTY3ODkwLCJ1c2VyX3R5cGUiOiJ1c2VyIiwicm9sZSI6InVzZXIiLCJleHBpcmVkX3N0YWdlX2lkIjoxMjM0NTY3ODkwfQ.K_UvXU0qW31YocTx9c_bSg0WMLuk7yBf5Fq9KT9Xx1c"
}
```

#### Solicitud incorrecta

Al enviar una solicitud con usuario o contraseña incorrectos, el cuerpo de la respuesta se verá como este:

```json
{
  "detail": "No authentication credentials were provided."
}
```

Al enviar una solicitud sin usuario ni contraseña, el cuerpo de la respuesta se verá como este:

```json
{
  "username": ["This field is required."],
  "password": ["This field is required."]
}
```

### Access Token y Refresh Token

El **access token** será el que se utilice en el header de cada solicitud que realice el frontend al backend para obtener datos por parte del backend sobre los endpoints protegidos por autenticación.

El **refresh token** le permitirá al frontend obtener un nuevo _access token_ cuando el actual caduque.

## /api/token/refresh/

#### Cuerpo de la Solicitud

Este endpoint se debe utilizar a través del método **POST** y en el cuerpo de la solicitud debe estar el **refresh token** del usuario que realiza la solicitud.

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NTY3ODkwLCJ1c2VyX3R5cGUiOiJ1c2VyIiwicm9sZSI6InVzZXIiLCJleHBpcmVkX3N0YWdlX2lkIjoxMjM0NTY3ODkwfQ.K_UvXU0qW31YocTx9c_bSg0WMLuk7yBf5Fq9KT9Xx1c"
}
```

#### Solicitud Correcta

Al enviar una solicitud correctamente se obtendrá un nuevo **access token** y el cuerpo de la respuesta se verá como este:

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NTY3ODkwLCJ1c2VyX3R5cGUiOiJ1c2VyIiwicm9sZSI6InVzZXIiLCJleHBpcmVkX3N0YWdlX2lkIjoxMjM0NTY3ODkwfQ.3gHkJnlD8U5Xg0of2h_mV7XfiRtOqPSkLNY-XpF53gs"
}
```

#### Solicitud incorrecta

Si el `refresh token` es inválido o ha expirado, el servidor devolverá un error 401 (Unauthorized) con un mensaje indicando que el token no es válido. Al enviar una solicitud con un token inválido o caducado, el cuerpo de la respuesta se verá como este:

```json
{
  "detail": "Token is invalid or expired"
}
```

Al enviar una solicitud sin el `refresh token`, el cuerpo de la respuesta se verá como este:

```json
{
  "refresh": ["This field is required."]
}
```

### _Refresh Token_ Caducado

En caso de tener un refresh token caducado, la aplicación de Frontend debe **borrar los tokens almacenados** y **re-dirigir** al usuario al formulario de **login nuevamente** para obtener un nuevo par de tokens. El **tiempo de vida útil** del token de refresh será **configurado en el backend**.

## Accediendo a un _Endpoint Protegido_

Teniendo en cuenta todo lo anterior, el **Access Token** se puede utilizar para acceder a endpoints de la API que estén protegidos bajo autenticación. Para hacer esto, se debe indicar en **el header de la solicitud** el token bajo la llave `Authorization` y con el texto `Bearer ` antes del **Access Token**. **El header de la solicitud** debe contener esto:

```json
{
  "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMjM0NTY3ODkwLCJ1c2VyX3R5cGUiOiJ1c2VyIiwicm9sZSI6InVzZXIiLCJleHBpcmVkX3N0YWdlX2lkIjoxMjM0NTY3ODkwfQ.3gHkJnlD8U5Xg0of2h_mV7XfiRtOqPSkLNY-XpF53gs"
}
```

#### Solicitud Correcta

Al enviar una solicitud correctamente se obtendrá la respuesta con los datos solicitados sin ningún problema.

#### Solicitud incorrecta

Al enviar una solicitud sin el `access token` el servidor devolverá un error 401 (Unauthorized) y el cuerpo de la respuesta se verá como este:

```json
{
  "detail": "Authentication credentials were not provided."
}
```

Si el `access token` es inválido o ha expirado, el servidor devolverá un error 401 (Unauthorized) con un mensaje indicando que el token no es válido. Al enviar una solicitud con un token inválido o caducado, el cuerpo de la respuesta se verá como este:

```json
{
  "detail": "Token is invalid or expired"
}
```

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
