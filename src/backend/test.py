import unittest
import threading
import requests
import logging

from backend.server.server import Server
from backend.server.response import HttpResponse

logger = logging.getLogger(__name__)

def reflectBody(req, args):
    resp = HttpResponse(200)
    if req.content:
        resp.setByteContent(req.content, "text/plain")
    return resp

test_headers = {
    "content-type": "text/plain",
    "foo": "bar"
}

def checkHeaders(req, args):
    expected = args
    resp = HttpResponse(200)
    try:
        for (header, value) in expected.items():
            assert header in req.headers
            assert value == req.headers[header]
    finally:
        return resp


class TestServer(unittest.TestCase):

    def setUp(self):
        self.ip_addr = "127.0.0.1"
        self.port = 8081
        self.origin = f"http://{self.ip_addr}:{self.port}"
        logger.info(f"Starting server at {self.origin}")
        self.server = Server(self.ip_addr, self.port)

        self.server.bindResource("/reflect", reflectBody, None)
        self.server.bindResource("/headers", checkHeaders, test_headers)

        self.server.run()
    
    def test_request(self):
        data = "Hello world!"
        response = requests.post(f"{self.origin}/reflect", data=data)
        assert data == response.text

        response = requests.get(f"{self.origin}/headers", headers=test_headers)

    def tearDown(self):
        logger.info("Shutting down")
        self.server.stop()

if __name__ == '__main__':
    logging.basicConfig(
        filename="test.log",
        filemode="w",
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s %(message)s",
    )
    unittest.main()
