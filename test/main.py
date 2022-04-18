from hashlib import sha256
from random import randint
import os

def hashThis(r, M):
    hash=sha256();
    hash.update(str(r).encode());
    hash.update(M.encode());
    return int(hash.hexdigest(),16);

def hashPDF(file, BLOCK_SIZE):
    with open(file, 'rb') as f: # Open the file to read it's bytes
        fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
    while len(fb) > 0: # While there is still data being read from the file
        hash.update(fb) # Update the hash
        fb = f.read(BLOCK_SIZE) # Read the next block from the file


## Notation
# generator g
g = 2

# Prime q (for educational purpose I use explicitly a small prime number - for cryptographic purposes this would have to be much larger)
q = 2695139

## Key generation
#Private signing key x
x = 32991
# calculate public verification key y
y = pow(g, x, q)

## Signing
# M = "This is the message"
file = "./test/test.pdf"
BLOCK_SIZE =  os.path.getsize(file) 
k = randint(1, q - 1)
r = pow(g, k, q)
# e = hashThis(r, M) % q # part 1 of signature
e = hashPDF(file, BLOCK_SIZE)
s = (k - (x * e)) % (q-1) # part 2 of signature

## Verification

rv = (pow(g, s, q) * pow (y, e, q)) % q
ev = hashThis(rv, M) % q

print ("e " + str(e) + " should equal ev " + str(ev))