from flask import session


class Home:
    name = "TFG"
    title = None
    category = 0
    dynamic = 0
    scope = None
    logged = False

    def __init__(self):
        print(self.name)

    def get_base_params(self, _title, _dynamic):
        if 'logged_in' in session:
            self.title = _title
            self.name = session['name']
            self.category = session['category']
            self.logged = True
            self.dynamic = _dynamic

        return self
