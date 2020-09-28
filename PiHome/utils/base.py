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
    header = None

    def __init__(self, _dynamic=1):
        self.dynamic = _dynamic

    def get_base_params(self, **kwargs):
        if 'logged_in' in session:
            self.name = session['name']
            self.category = session['category']
            self.logged = True

        if kwargs.get("_header"):
            self.header = kwargs.get("_header")
        else:
            self.header = "Título de la vista"

        if kwargs.get("_title"):
            self.title = kwargs.get("_title")
        else:
            self.title = "TFG"

        if kwargs.get("_dynamic"):
            self.dynamic = kwargs.get("_dynamic")
        else:
            self.dynamic = 0

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
    header : [str]
        Nombre de las columnas
    data : [object]
        Valor de los datos a mostrar
    footer : [object]
        Si se tiene que mostrar algun valor resumatorio
    """
    # title: str
    # definition: str
    # header: [str]
    # data: [str]
    # footer: [str]

    title = None
    definition = None
    header = None
    data = None
    footer = None

    def __init__(self, _title="Title not defined", _header=None, _data=None, **kwargs) -> None:
        super().__init__()

        # assert (len(_header) + 1 == len(_data[0])), \
        #     "El número de campos de la cabecera, no coincide con el cuerpo de la tabla."

        if _title is not None:
            self.title = _title

        if "_definition" in kwargs:
            self.definition = kwargs.get("_definition")

        if _header is not None:
            self.header = _header

        if _data is not None:
            self.data = _data

        if "_footer" in kwargs:
            self.footer = kwargs.get("_footer")
