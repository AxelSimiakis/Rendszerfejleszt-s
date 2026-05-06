import os

basedir = os.path.abspath(os.path.dirname(__file__))

def load_private_key():
    
    path = os.path.abspath(os.path.dirname(__file__))
    key_path = os.path.join(path, ".ssh", "private-key.pem")
    try:
        with open(key_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print("A private-key.pem nem talalhato!")
        return "-tartalek-jwt-kulcs"

class Config:
    
    SECRET_KEY = load_private_key()
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False