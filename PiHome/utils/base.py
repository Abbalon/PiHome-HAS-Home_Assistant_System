from flask import session


class Home:
    """Clase encargada de parametrizar los valores mínimos de cualquier vista.

    Attributes
    ----------
    @:param name : String
        nombre de la vista
    @:param title : String
        Título de la vista
    @:param category : int
        Role del usuario logado
    @:param dynamic : int
        Define el comportamiento dínamico de la página
    @:param scope
        Alcance de la vista
    @:param logged
        Define si se está en una sesión activa
    """

    name = "Hi you"
    title = "PiHome - TFG"
    category = 0
    dynamic = 0
    scope = None
    logged = False

    def __init__(self, _dynamic=1):
        self.dynamic = _dynamic

    def get_base_params(self, _title="TFG", _dynamic=0):
        if 'logged_in' in session:
            self.name = session['name']
            self.category = session['category']
            self.logged = True

        self.title = _title
        self.dynamic = _dynamic

        return self

    def set_default(self):
        self.name = "Hi you"
        self.title = "PiHome - TFG"
        self.category = 0
        self.dynamic = 1
        self.scope = None
        self.logged = False


class ShowData:
    """Clase que define el modelo básico de datos que ha de recibir una vista
    que vaya a mostrar datos.

    Attributes
    ----------
    title : str
        Titulo de la tabla
    definition : str
        Descripción de la tabla
    default : str
        Mensaje de advertencia, en caso que no se hayan recibido datos
    header : [str]
        Nombre de las columnas
    data : [object]
        Valor de los datos a mostrar
    footer : [object]
        Si se tiene que mostrar algun valor resumatorio
    """
    title = ""
    definition = ""
    default = ""
    header = []
    data = []
    footer = []
