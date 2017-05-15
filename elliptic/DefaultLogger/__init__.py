import logging
import colorlog


def init(level=logging.INFO):
    logger = colorlog.getLogger('elliptic.Mesh.Mesh')
    logger.setLevel(level)

    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s:%(name)s:%(message)s'))
    logger.addHandler(handler)
