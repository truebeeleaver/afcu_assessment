import logging

logger = logging.getLogger(__name__)

# a subset of response codes; we won't use all of them!
CODES = {
    200: "OK",
    201: "Created",
    400: "Bad Request",
    401: "Unauthorized",
    404: "Not Found",
    500: "Internal Server Error",
}


class HttpResponse:
    def __init__(self, status):
        self.headers = {"content-length": "0"}
        self.status = status
        self.content = None

    def __str__(self):
        return f"{self.status} {CODES[self.status]}"

    def setTextContent(self, content, content_type):
        self.content = bytes(content, "utf-8")
        self.headers["content-type"] = content_type
        self.headers["content-length"] = len(self.content)

    def setByteContent(self, content, content_type):
        self.content = content
        self.headers["content-type"] = content_type
        self.headers["content-length"] = len(self.content)

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

    def setHeader(self, header, value):
        current_value = self.headers.get(header)
        if current_value:
            self.headers[header] = f"{current_value}; {value}"
        else:
            self.headers[header] = value
