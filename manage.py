from werkzeug.wsgi import DispatcherMiddleware
from spyne.server.wsgi import WsgiApplication

from apps import Service1
from apps.flasked import app

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/soapAPI1': WsgiApplication(Service1.create_app(app)),
    # '/soapAPI2': WsgiApplication(spyned2.create_app(app))
})


if __name__ == '__main__':
    app.run(host = '127.0.0.1', port= 8000)