import logging

from server.server import Server

logger = logging.getLogger(__name__)

# this will be our entrypoint
if __name__ == "__main__":
    logging.basicConfig(
        filename="backend.log",
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(threadName)s %(message)s",
    )
    logger.info("Server starting up")

    #TODO move to config file
    server = Server("127.0.0.1", 8080)
    server.run()

    logger.info("Server shutting down normally")

