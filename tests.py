import sys
from decouple import config

# this is not pythonic and hacky, fix this later!
sys.path.append('lib')
from flask_upload import app




def test_index_route():
    response = app.test_client().get('/')
    assert response.status_code == 200

