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

Para más detalles puedes visualizar ejemplos de uso en [Python](EjemploPython.md) o [React](EjemploReact.md)
