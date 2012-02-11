import cherrypy

class HttpServer(object):
    def index(self):
        return "USAGE"
    index.exposed = True


if __name__ == "__main__":
    cherrypy.quickstart(HttpServer())
