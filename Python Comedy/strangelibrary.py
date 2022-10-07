import numpy as np
import logging

with open('error.txt', encoding='utf8') as f:
    lines = f.readlines()
msg =(" ".join(lines))

def strange_function():
    try:
        1/0
    except BaseException:
        logging.exception(msg)