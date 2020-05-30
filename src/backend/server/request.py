import logging

from backend.server.util import BufferedSocket

logger = logging.getLogger(__name__)

BUFFER_SIZE = 1024

HTTP_GET = "GET"
HTTP_HEAD = "HEAD"
HTTP_POST = "POST"
HTTP_PUT = "PUT"
HTTP_DELETE = "DELETE"
HTTP_CONNECT = "CONNECT"
HTTP_OPTIONS = "OPTIONS"
HTTP_TRACE = "TRACE"


class HttpRequest:
    def __init__(self, reader):
        # Consume the first line: should be <VERB> <RESOURCE> <HTTP VERSION>
        line = reader.readLine()
        # This is cute but not very fault tolerant, but we want to abort on a malformed line anyhow
        (verb, resource, version) = line.split(" ", 2)
        # I will only support HTTP 1.1
        if version != "HTTP/1.1":
            raise ValueError(f"Invalid HTTP version {version}")

        self.verb = verb
        # Ignoring query params
        self.resource = resource.split("?", 1)[0]
        self.headers = {}
        self.content = None

        # We want to read until there is a blank line--this indicates the end of the header block
        line = reader.readLine()
        while line:
            (header, value) = line.split(":", 1)
            header = header.strip().lower()
            value = value.strip()
            # Special case: headers can be specified multiple times; collapse to one line
            if header in self.headers:
                self.headers[header] = f"{self.headers[header]}; {value}"
            self.headers[header] = value
            line = reader.readLine()

        if self.headers.get("content-length"):
            length = int(self.headers["content-length"])
            if length < 0:
                raise ValueError(
                    f"Request had negative content length {length}"
                )
            self.content = reader.readBytes(length)

    def getCookies(self):
        if "cookie" not in self.headers:
            return {} 
        cookies = self.headers["cookie"].split(";")
        ret = {}
        for cookie in cookies:
            (name, value) = cookie.split("=", 1)
            ret[name] = value
        return ret

    def getCookie(self, cookie):
        return self.getCookies().get(cookie)
