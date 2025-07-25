import logging
import os
import sys
import time
from datetime import datetime

from fastapi import Request

logger = logging.getLogger()

formatter = logging.Formatter(
    fmt="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

directory = 'logs/'
if not os.path.exists(directory):
    os.makedirs(directory)

stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler(f'{directory}{datetime.now():%Y-%m-%d %H.%M.%S}.log')

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.handlers = [stream_handler, file_handler]

logger.setLevel(logging.INFO)


async def log_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    execution_time = time.time() - start_time

    log_dict = {
        "request_method": request.method,
        "request_url": str(request.url),
        "execution_time": execution_time,
        "response_status_code": response.status_code,
        "remote_address": request.client.host,
        "request_headers": dict(request.headers),
    }

    logger.info(log_dict, extra=log_dict)
    return response
