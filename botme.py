from tornado import gen
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado import web
from tornado.options import define, options
from tornado.options import parse_config_file

import psycopg2
import momoko

define("port", default=8888, help="run on the given port", type=int)
define("dbport", default=5423, help="Run the db on the given port", type=int)
define("host", default="127.0.0.1", help="blog database host")
define("dbname", default="blog", help="blog database name")
define("user", default="blog", help="blog database user")
define("password", default="blog", help="blog database password")

class BaseHandler(web.RequestHandler):
    @property
    def db(self):
        return self.application.db


class TutorialHandler(BaseHandler):
    def get(self):
        self.write('Hello World!')
        self.finish()

if __name__ == '__main__':
    parse_config_file("./dev.conf")
    print("OLA")
    application = web.Application([
        (r'/', TutorialHandler)
    ], debug=True)

    ioloop = IOLoop.instance()

    dsn_string = "dbname=" + options.dbname + " user=" + options.user + " password=" + options.password + " host=" + options.host + " port=" + str(options.dbport)
    print(dsn_string)
    application.db = momoko.Pool(
        dsn=dsn_string,
        size=4,
        ioloop=ioloop,
    )

    # this is a one way to run ioloop in sync
    future = application.db.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()
    future.result()  # raises exception on connection error

    http_server = HTTPServer(application)
    http_server.listen(options.port, '0.0.0.0')
    ioloop.start()