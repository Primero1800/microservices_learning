from hashlib import sha256
import pyshorteners

if __name__ == "__main__":
    #input_ = input("Enter value to encrypt:")
    input_ = "https://www.primero1800.store/api/v1/posts/"
    print(f"RAW INPUT: {input_}")
    input_encoded = input_.encode('utf-8')
    print(f"INPUT ENCODED: {input_encoded}")
    sha256_input = sha256(input_encoded)
    print(f"INPUT ENCODED SHA256: {sha256_input.hexdigest()}")

    print('*******************************************************')
    print("PYSHORTENERS")
    print()
    pyshorteners_input = pyshorteners.Shortener().tinyurl.short(input_)
    print(f"PYSHORTENERS: {pyshorteners_input}")

