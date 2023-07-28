import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Create a file handler
handler = logging.FileHandler('app.log')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)
