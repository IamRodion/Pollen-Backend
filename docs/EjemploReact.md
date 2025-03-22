### Ejemplo Práctico en Vite + React

### Instalación de Dependencias

Primero, asegúrate de tener las siguientes dependencias instaladas en tu proyecto Vite:

```bash
npm install axios dotenv
```

### Configuración de Variables de Entorno

Crea un archivo `.env` en el directorio raíz de tu proyecto con las siguientes variables:

```
VITE_API_URL=https://ruta-a-la-api/
```

### Autenticación con JWT en Vite + React

#### 1. Configuración de Axios

Crea un archivo `axiosConfig.js` para configurar Axios:

```javascript name=src/axiosConfig.js
import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default apiClient;
```

#### 2. Funciones de Autenticación

Crea un archivo `authService.js` para manejar las solicitudes de autenticación:

```javascript name=src/authService.js
import apiClient from "./axiosConfig";

export const login = async (username, password) => {
  const response = await apiClient.post("/api/token/", { username, password });
  return response.data;
};

export const refreshToken = async (refreshToken) => {
  const response = await apiClient.post("/api/token/refresh/", {
    refresh: refreshToken,
  });
  return response.data.access;
};
```

#### 3. Contexto de Autenticación

Crea un contexto para manejar el estado de autenticación en `AuthContext.js`:

```javascript name=src/AuthContext.js
import React, { createContext, useState, useEffect } from "react";
import { login, refreshToken } from "./authService";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [authTokens, setAuthTokens] = useState(() =>
    localStorage.getItem("tokens")
      ? JSON.parse(localStorage.getItem("tokens"))
      : null
  );
  const [user, setUser] = useState(() =>
    localStorage.getItem("user")
      ? JSON.parse(localStorage.getItem("user"))
      : null
  );

  const loginUser = async (username, password) => {
    const tokens = await login(username, password);
    setAuthTokens(tokens);
    setUser({ username });
    localStorage.setItem("tokens", JSON.stringify(tokens));
    localStorage.setItem("user", JSON.stringify({ username }));
  };

  const logoutUser = () => {
    setAuthTokens(null);
    setUser(null);
    localStorage.removeItem("tokens");
    localStorage.removeItem("user");
  };

  const refreshAccessToken = async () => {
    const newAccessToken = await refreshToken(authTokens.refresh);
    setAuthTokens({ ...authTokens, access: newAccessToken });
    localStorage.setItem(
      "tokens",
      JSON.stringify({ ...authTokens, access: newAccessToken })
    );
  };

  useEffect(() => {
    if (authTokens && authTokens.access) {
      const interval = setInterval(() => {
        refreshAccessToken();
      }, 15 * 60 * 1000); // Refresh token every 15 minutes
      return () => clearInterval(interval);
    }
  }, [authTokens]);

  return (
    <AuthContext.Provider value={{ authTokens, loginUser, logoutUser, user }}>
      {children}
    </AuthContext.Provider>
  );
};
```

#### 4. Uso del Contexto de Autenticación

En tu componente principal, utiliza el contexto de autenticación:

```javascript name=src/App.jsx
import React, { useContext, useState } from "react";
import { AuthContext, AuthProvider } from "./AuthContext";
import axios from "axios";

const App = () => {
  return (
    <AuthProvider>
      <Login />
      <ProtectedComponent />
    </AuthProvider>
  );
};

const Login = () => {
  const { loginUser } = useContext(AuthContext);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    await loginUser(username, password);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Login</button>
    </form>
  );
};

const ProtectedComponent = () => {
  const { authTokens, logoutUser } = useContext(AuthContext);

  const fetchProtectedData = async () => {
    const response = await axios.get(
      import.meta.env.VITE_API_URL + "api/data/",
      {
        headers: {
          Authorization: `Bearer ${authTokens.access}`,
        },
      }
    );
    console.log(response.data);
  };

  return (
    <div>
      <button onClick={fetchProtectedData}>Fetch Protected Data</button>
      <button onClick={logoutUser}>Logout</button>
    </div>
  );
};

export default App;
```

### Explicación

1. **Configuración de Axios:** Se configura un cliente Axios con la URL base de la API utilizando las variables de entorno de Vite.
2. **Funciones de Autenticación:** Se definen funciones para realizar las solicitudes de login y de refresco de tokens.
3. **Contexto de Autenticación:** Se crea un contexto para manejar el estado de autenticación y almacenar los tokens en el localStorage.
4. **Uso del Contexto:** Se utilizan las funciones de login y logout en los componentes de React, y se realiza una solicitud a un endpoint protegido utilizando el `access token`.

Este ejemplo muestra cómo manejar la autenticación en una aplicación Vite + React utilizando JWTs, proporcionando una solución completa desde el login hasta el uso de tokens para acceder a endpoints protegidos.
