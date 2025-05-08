# pyzid

A sortable unique identifier generator.

## Usage

```python
import pyzid

print( pyzid.generate() )
```

## Specification

Raw ZID is a 15 bytes binary data, which consists of 4 parts:

| Part | Size | Description |
| --- | --- | --- |
| Timestamp | 6 | Timestamp in milliseconds. |
| MachineID | 4 | Machine unique identifier. |
| ProcessID | 3 | Process ID. |
| Sequence  | 2 | Sequence. |

All parts are integer value, and they are encoded to bytes in Big-Endian.

---

ZID is a customized base32 encoded string from raw ZID, which is a 24 characters string consists of numbers and lower-case letters.