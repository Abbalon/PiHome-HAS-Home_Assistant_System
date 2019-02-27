from PiHome import app

if __name__ == 'run':
    try:
        print("Arrancando la aplicación.")
        app.run(port=8000, debug=True)
    except Exception as e:
        print(e)
