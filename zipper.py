import pdb
import os
import zipfile
import tempfile
from pyramid.response import FileIter
from pyramid.response import Response
from pyramid.config import Configurator
from pyramid.view import view_config
from wsgiref.simple_server import make_server
 
@view_config(route_name='home', renderer='__main__:template.pt')
def my_view(request):
    return {}
 
 
@view_config(route_name='zipper')
def zipper(request):
    fp = tempfile.NamedTemporaryFile('w+b', delete=True)
 
    ## creating zipfile and adding files
    z = zipfile.ZipFile(fp, "w")
    z.write('mushroom.jpg')
    z.write('ladybug.png')
    z.close()
 
    # rewind fp back to start of the file
    fp.seek(0)
 
    response = request.response
    response.content_type = 'application/zip'
    response.content_disposition = 'attachment; filename="somefilegroup.zip"'
    response.app_iter = FileIter(fp)
    return response
 
 
if __name__ == '__main__':
    config = Configurator(settings={})
    config.add_route('home', '/')
    config.add_route('zipper', '/zipper')
    config.scan('.')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()