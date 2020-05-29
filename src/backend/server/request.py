import logging

from backend.server.util import BufferedSocket

logger = logging.getLogger(__name__)

BUFFER_SIZE = 1024

METHODS = {
    "GET",
    "HEAD",
    "POST",
    "PUT",
    "DELETE",
    "CONNECT",
    "OPTIONS",
    "TRACE",
}


class HttpRequest:
    def __init__(self, reader):
        # Consume the first line: should be <VERB> <RESOURCE> <HTTP VERSION>
        line = reader.readLine()
        # This is cute but not very fault tolerant, but we want to abort on a malformed line anyhow
        (verb, resource, version) = line.split(" ", 2)
        if verb not in METHODS:
            raise ValueError(f"Invalid HTTP verb {verb}")
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
            self.headers[header.strip()] = value.strip()
            line = reader.readLine()

        if self.headers.get("Content-Length"):
            length = int(self.headers["Content-Length"])
            if length < 0:
                raise ValueError(
                    f"Request had negative content length {length}"
                )
            self.content = reader.readBytes(length)
