import logging

logger = logging.getLogger(__name__)

# a subset of response codes; we won't use all of them!
CODES = {
    200: "OK",
    201: "Created",
    400: "Bad Request",
    401: "Unauthorized",
    404: "Not Found",
}


class HttpResponse:
    def __init__(self, status):
        self.headers = {}
        self.status = status
        self.content = None

    def setTextContent(self, content, content_type):
        self.content = bytes(content, 'utf-8')
        self.headers["Content-Type"] = content_type
        self.headers["Content-Length"] = len(self.content)

    def setByteContent(self, content, content_type):
        self.content = content
        self.headers["Content-Type"] = content_type
        self.headers["Content-Length"] = len(self.content)

    def writeResponse(self, writer):
        # First write the initial status line
        writer.writeLine(f"HTTP/1.1 {self.status} {CODES[self.status]}")

        # Write headers
        for (header, value) in self.headers.items():
            writer.writeLine(f"{header}: {value}")

        # Terminate header block with a blank line
        writer.writeLine("")

        # Write content if it exists
        if self.content:
            writer.writeBytes(self.content)

