#gcd.py
def gcd(x: int, y: int) -> int:
    while y:
        x, y = y, x % y 
    return x

print(gcd(56, 42))  # Output: 14
print(gcd(42, 56))  # Output: 14
print(gcd(15, 18))  # Output: 3
print(gcd(70, 500))
print(gcd(45, 180))