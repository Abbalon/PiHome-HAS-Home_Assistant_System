#!venv/bin/python
from PiHome import app

if __name__ == "__main__":
    try:
        print("Arrancando la aplicación.")
        app.run(host='0.0.0.0', port=8000)
    except Exception as e:
        print(e)
