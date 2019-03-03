from flask import session


class Home:
    name = None
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
        self.name = None
        self.title = "PiHome - TFG"
        self.category = 0
        self.dynamic = 1
        self.scope = None
        self.logged = False
