__author__ = 'deadblue'

import os
import uuid
import zlib

from ._utils import i2b


def node_id() -> bytes:
    hw_addr = i2b(uuid.getnode(), 6)
    machine_id = i2b(zlib.crc32(hw_addr), 4)
    process_id = i2b(os.getpid(), 3)
    return machine_id + process_id
