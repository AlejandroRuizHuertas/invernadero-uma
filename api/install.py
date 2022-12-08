from models.user import User
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    User().create(name='Invernadero 1', email='invernadero1@uma.es', password='PasswordInvernadero1!', endpoint="http://127.0.0.1:5000")
    User().create(name='Invernadero 2', email='invernadero2@uma.es', password='PasswordInvernadero2!', endpoint="http://127.0.0.1:5000")
    User().create(name='Administrador', email='admin@uma.es', password='Admin!1235', role="admin")