import unittest

from app import app,cas
from urllib.parse import urlparse,parse_qs

class Base(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            app.debug = True
            app.testing = True
            

    def tearDown(self):
        pass


class CasTests(Base):
    def setUp(self):
        self.client = app.test_client()
        return super().setUp()


    def test_ticket(self):
        email='guest@example.com'
        pwd='justpassingby'
        resp = self.client.post('/cas/login',data={'username':email,'password':pwd})
        assert(resp.status_code == 302 )
        app.logger.info(resp.headers)
        location=resp.headers.get('Location')
        app.logger.info(location)
        up = urlparse(location)
        params = parse_qs(up.query) 
        assert(params.get('ticket') is not None )

        ticket = params.get('ticket')[0]
        resp = self.client.get(f'/cas/serviceValidate?ticket={ticket}&service=/')
        assert(resp.status_code == 200 )
        # TODO validate cas xml response
        app.logger.info(resp.text)





if __name__ == '__main__':
    unittest.main()
