import hashlib
import random

class Point:
    def __init__(self, x=None, y=None, compressed=None):
        if compressed:
            self.x, self.y = self.decompress(compressed)
        else:
            self.x = x
            self.y = y
    
    def __repr__(self):
        return self.compress()
    
    def compress(self):
        xHex = hex(self.x)[2:].zfill(64)
        prefix = '02' if self.y % 2 == 0 else '03'
        return prefix + xHex

    @staticmethod
    def decompress(compressed):
        prefix = compressed[:2]
        xHex = compressed[2:]
        x = int(xHex, 16)
        
        y_squared = (pow(x, 3, p) + a * x + b) % p
        y = pow(y_squared, (p + 1) // 4, p)
        
        if (prefix == '02' and y % 2 != 0) or (prefix == '03' and y % 2 == 0):
            y = (-y) % p
        
        return x, y

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x, self.y) == (other.x, other.y)
        return False
    
    def __add__(self, other):
        return add(self, other)

    def __sub__(self, other):
        return sub(self, other)
    
    def __mul__(self, scalar):
        return mul(self, scalar)
    
    def __truediv__(self, scalar):
        return div(self, scalar)
    
    def __neg__(self):
        return neg(self)

    @staticmethod
    def hash(message):
        """Compute the SHA-256 hash of the input message."""
        return int(hashlib.sha256(message.encode()).hexdigest(), 16)

    def sign(self, message, private_key):
        """Generate an ECDSA signature (r, s) for a message."""
        z = self.hash(message) % N
        k = random.randint(1, N)
        R = mul(G, k)
        r = R.x % N
        s = ((z + r * private_key) * modInv(k, N)) % N
        return r, s

    def trinity(self):
        P1 = self
        P2 = self * R1
        P3 = self * R2
        return P1, P2, P3

def modInv(a, m):
    return pow(a, -1, m)

def add(P, Q):
    if isinstance(P, Point):
        P = P
    else:
        P = Point(compressed=P)
    if isinstance(Q, int):
        Q = mul(G, Q)
    if P is None:
        return Q
    if Q is None:
        return P
    if P.x == Q.x and P.y == (-Q.y) % p:
        return None

    if P.x == Q.x:
        slope = ((3 * P.x**2 + a) * modInv(2 * P.y, p)) % p
    else:
        slope = ((Q.y - P.y) * modInv(Q.x - P.x, p)) % p

    Rx = (slope**2 - P.x - Q.x) % p
    Ry = (slope * (P.x - Rx) - P.y) % p

    return Point(Rx, Ry)

def mul(K, scalar):
    result = None
    for _ in range(scalar.bit_length()):
        if scalar & 1:
            if result is None:
                result = K
            else:
                result = add(result, K)
        K = add(K, K)
        scalar >>= 1
    return result

def div(K, scalar):
    return mul(K, modInv(scalar, N))

def sub(P, Q):
    if isinstance(P, Point):
        P = P
    else:
        P = Point(compressed=P)
        
    if isinstance(Q, int):
        Q = mul(G, Q)
    Q_neg = Point(x=Q.x, y=(-Q.y) % p)
    return add(P, Q_neg)
    
def neg(P):
    return (Point(P.x, -P.y % p))

def verify(message, signature, pubkey):
    r, s = signature
    if not (1 <= r < N and 1 <= s < N):
        return False
    z = Point.hash(message) % N
    w = modInv(s, N)
    u1 = (z * w) % N
    u2 = (r * w) % N
    R = add(mul(G, u1), mul(pubkey, u2))
    return R is not None and R.x % N == r

a = 0
b = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = Point(x=Gx, y=Gy)
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F

R1 = 37718080363155996902926221483475020450927657555482586988616620542887997980018
R2 = 78074008874160198520644763525212887401909906723592317393988542598630163514318