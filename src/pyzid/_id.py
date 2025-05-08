__author__ = 'deadblue'

import time
import threading
from typing import ClassVar

from ._encoding import (
    encode as b32enc, 
    decode as b32dec
)
from ._node import node_id
from ._utils import b2i, i2b


class ZID:

    _last_seq: ClassVar[int] = 0
    _last_time: ClassVar[int] = 0
    _lock: ClassVar[threading.Lock] = threading.Lock()
    _node_id: ClassVar[bytes] = node_id()

    _raw: bytes

    def __new__(cls):
        timestamp, seq = int(time.time() * 1000), 0
        with cls._lock:
            if timestamp > cls._last_time:
                cls._last_time = timestamp
                cls._last_seq = 0
            else:
                cls._last_seq += 1
                timestamp = cls._last_time
            seq = cls._last_seq
        # Make instance
        ret = object.__new__(cls)
        ret._raw = i2b(timestamp, 6) + cls._node_id + i2b(seq, 2)
        return ret

    @property
    def machine_id(self) -> int:
        """
        Machine ID is a int value from 0 to 0xffffffff.
        """
        return b2i(self._raw[6:10])

    @property
    def process_id(self) -> int:
        """
        Process ID is a int value from 0 to 0xffffff.
        """
        return b2i(self._raw[10:13])

    @property
    def timestamp(self) -> int:
        """
        Timestamp in milliseconds, from 0 to 0xffffffffffff.
        """
        return b2i(self._raw[:6])

    @property
    def sequence(self) -> int:
        """
        Sequence number from 0 to 0xffff.
        """
        return b2i(self._raw[-2:])

    @property
    def value(self) -> bytes:
        return self._raw

    def to_str(self) -> str:
        return b32enc(self._raw)

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(machine_id={self.machine_id}, \
            process_id={self.process_id}, timestamp={self.timestamp}, \
            sequence={self.sequence})'

    @classmethod
    def from_str(cls, zid_str: str) -> 'ZID':
        """
        Decode ZID string to ZID object.
        """
        ret = object.__new__(cls)
        ret._raw = b32dec(zid_str)
        return ret

    @classmethod
    def customize(
        cls, 
        timestamp: int, 
        machine_id: int,
        process_id: int,
        sequence: int
    ) -> 'ZID':
        """
        Customize a ZID with specific timestamp, machine_id, process_id and sequence.
        """
        ret = object.__new__(cls)
        ret._raw = i2b(timestamp, 6) + i2b(machine_id, 4) \
            + i2b(process_id, 3) + i2b(sequence, 2)
        return ret
    
    @classmethod
    def minimum(cls, timestamp: int) -> 'ZID':
        """
        Make minimum ZID for specific timestamp.
        """
        return cls.customize(timestamp, 0, 0, 0)

    @classmethod
    def maximum(cls, timestamp: int) -> 'ZID':
        """
        Make maximum ZID for specific timestamp.
        """
        return cls.customize(timestamp, 0xffffffff, 0xffffff, 0xffff)


def generate() -> str:
    """
    Generate a zid.

    Returns:
        str: Encoded ZID.
    """
    return ZID().to_str()