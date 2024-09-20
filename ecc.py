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
        """Overload the + operator for adding two points."""
        return add(self, other)

    def __sub__(self, other):
        """Overload the - operator for subtracting two points."""
        return sub(self, other)
    
    def __mul__(self, scalar):
        """Overload the * operator for point multiplication with a scalar."""
        return mul(self, scalar)
    
    def __truediv__(self, scalar):
        """Overload the / operator for dividing a point by a scalar."""
        return div(self, scalar)
    
    def __neg__(self):
        """Overload the negation operator (-) for a point."""
        return neg(self)

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

a = 0
b = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = Point(x=Gx, y=Gy)
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
