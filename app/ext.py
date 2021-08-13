# coding:utf-8


from blinker import Namespace
from app.loader import load_signals, load_services, load_form


class Service(object):
    def __init__(self, app=None):
        self.app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.load_services()

    def load_services(self):
        """
        """
        services = load_services(self.app)
        for attr, service in list(services.items()):
            self.__dict__[attr.replace('Service', '').lower()] = service(self.app)


class Form(object):
    def __init__(self, app=None):
        self.app = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.load_form()

    def load_form(self):
        """
        """
        forms = load_form(self.app)
        for attr, form in list(forms.items()):
            name = attr.replace('InputModel', '')
            if name == "":
                name = "Input"
            self.__dict__[name] = form


class Signal(object):
    def __init__(self, app=None):
        self._signal = Namespace()
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.setup_signal()

    def setup_signal(self):
        executors = load_signals(self.app)
        for key in executors:
            signal_ = self._signal.signal(key)
            signal_.connect(executors[key])
            setattr(self, key, signal_)


app = None
# signal = Signal()
serv = Service()
# serv.signal = signal

v = ""


def init_ext(a):
    global app

    app = a
    serv.init_app(app)
    # signal.init_app(app)
