from app import create_app 
from app import setup_database

app = create_app()

if __name__ == "__main__":
    app.run()