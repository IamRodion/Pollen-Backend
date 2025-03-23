# Pollen-Backend

Pollen-Backend es una aplicación desarrollada con Django Rest Framework que sirve como backend para una aplicación de encuestas. Permite a los usuarios iniciar sesión y responder encuestas de manera simple.

## Requisitos

Para ejecutar esta aplicación, asegúrate de tener las versiones correctas de las dependencias especificadas en `requirements.txt`.

## Autenticación

La autenticación en Pollen-Backend se maneja mediante JWT. Para más detalles sobre la implementación de autenticación, consulta el documento [Autenticación](docs/Autenticación.md).

## Endpoints

### Autenticación

- **POST /api/token/**: Obtiene un par de tokens (acceso y refresco) para un usuario autenticado.
- **POST /api/token/refresh/**: Obtiene un nuevo token de acceso usando un token de refresco válido.

### Encuestas

- **GET /api/surveys/**: Recupera una lista de todas las encuestas disponibles.
- **GET /api/surveys/{id}/**: Recupera los detalles de una encuesta específica por su ID.
- **POST /api/surveys/**: Crea una nueva encuesta (requiere autenticación y permisos adecuados).

### Preguntas

- **GET /api/surveys/{survey_id}/questions/**: Recupera todas las preguntas asociadas a una encuesta específica.
- **GET /api/questions/{id}/**: Recupera los detalles de una pregunta específica por su ID.
- **POST /api/questions/**: Crea una nueva pregunta en una encuesta (requiere autenticación y permisos adecuados).

### Respuestas de Usuario

- **POST /api/user-responses/**: Permite a un usuario enviar sus respuestas a las preguntas de una encuesta (requiere autenticación).
