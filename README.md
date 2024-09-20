# `ecc.py`  
A minimalistic implementation of the **secp256k1** elliptic curve in pure Python. This library allows you to perform elliptic curve operations such as point multiplication, addition, subtraction, and division, making it useful for cryptographic applications like generating public keys.

## Features
- Pure Python implementation of the **secp256k1** elliptic curve.
- Basic operations: point multiplication, addition, subtraction, and division.
- Simple and lightweight, designed for quick integration and experimentation.

### Example Usage

```python
from ecc import *

# Multiply the generator point G by a scalar
P = G * 12345

# Perform elliptic curve point addition
print(P + P)

# Subtract a point from P
print(P - G)

# Perform division (multiplying by inverse)
print(P / 12345)
```
