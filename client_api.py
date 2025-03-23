
import requests
import os
from dotenv import load_dotenv

class APIClient:
    def __init__(self):
        # Cargar las variables de entorno desde el archivo .env
        load_dotenv()
        self.username = os.getenv('USERNAME')
        self.password = os.getenv('PASSWORD')
        self.token_url = 'http://127.0.0.1:8000/api/token/'
        self.refresh_url = 'http://127.0.0.1:8000/api/token/refresh/'
        self.api_url = 'http://127.0.0.1:8000/api/UserResponse/'
        self.access_token = None
        self.refresh_token = None

    def authenticate(self):
        try:
            response = requests.post(self.token_url, data={'username': self.username, 'password': self.password})
            response.raise_for_status()
            tokens = response.json()
            self.access_token = tokens['access']
            self.refresh_token = tokens['refresh']
        except requests.exceptions.RequestException as e:
            print(f"Error during authentication: {e}")
            raise

    def refresh_access_token(self):
        try:
            response = requests.post(self.refresh_url, data={'refresh': self.refresh_token})
            response.raise_for_status()
            self.access_token = response.json()['access']
        except requests.exceptions.RequestException as e:
            print(f"Error refreshing access token: {e}")
            raise

    def get_data(self):
        headers = {'Authorization': f'Bearer {self.access_token}'}
        try:
            response = requests.get(self.api_url, headers=headers)
            if response.status_code == 401:  # Si el token de acceso ha expirado
                print("Access token expired, refreshing...")
                self.refresh_access_token()
                return self.get_data()  # Retry with new access token
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            raise

def main():
    client = APIClient()
    client.authenticate()
    data = client.get_data()
    print(data)

if __name__ == '__main__':
    main()
