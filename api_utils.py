from header import *

# สุ่มคำสร้างประโยคเพื่อใช้ทดลอง
import random
def word():
    n = random.randint(3,7)
    A = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    a = 'abcdefghijklmnopqrstuvwxyz'
    t = A[random.randint(0,25)]
    for i in range(n):
        t+=a[random.randint(0,25)]
    return t+' '

def gen_text(numOfWord:int):
    x = ''
    for i in range(numOfWord):
        x+=word()
    return x
@app.get('/rand-text/{numOfWord}')
def generate_random_text(numOfWord:int):
    return {'result': gen_text(numOfWord)}


# api Lorem
# รายการคำที่จะใช้สร้าง Lorem Ipsum
lorem_words = [
    "Lorem", "ipsum", "dolor", "sit", "amet", "consectetur",
    "adipiscing", "elit", "sed", "do", "eiusmod", "tempor",
    "incididunt", "ut", "labore", "et", "dolore", "magna",
    "aliqua", "a", "the"
]
@app.get("/lorem/{length}")
def generate_lorem(length: int):
    lorem_text = " ".join(random.choice(lorem_words) for _ in range(length))
    return {"lorem_text": lorem_text}

# api เข้ารหัสข้อความ sha256
import hashlib
@app.get('/sha256/{text}/')
def sha256(text:str):
    inst = hashlib.sha256()
    inst.update(text.encode('utf-8'))
    hash_binary = inst.digest()
    hash_hex = hash_binary.hex()
    return {"hash_hex":hash_hex}

# delay in second
import time
@app.get('/delay/{second}/')
async def delay(second:float):
    await time.sleep(second)