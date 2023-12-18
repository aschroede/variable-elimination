import logging


logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

handler = logging.FileHandler('VE.log')

#formatter = logging.Formatter('%(asctime)s - %(levelname)s\n - %(message)s')

formatter = logging.Formatter('\n%(message)s')

handler.setFormatter(formatter)

logger.addHandler(handler)