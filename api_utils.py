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

# api เข้ารหัสไฟล์แปลงเป็นข้อความ base64
import base64
@app.post('/file2base64/')
async def convert_file_to_base64(file:UploadFile):
    data = await file.read()
    base64_data = base64.b64encode(data).decode('utf-8')
    return {"base64_data":base64_data}


# api สร้างภาพ qr-code สกุลไฟล์ png แต่จะตอบกลับเป็น base64
from io import BytesIO
import qrcode
@app.get("/generate-qr-code/{data:path}")
async def generate_qr_code(data: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    # สร้าง BytesIO สำหรับเก็บภาพและส่งกลับ
    img_io = BytesIO()
    qr_img.save(img_io, "PNG")

    # กลับข้อมูลเป็นไฟล์ภาพ
    img_io.seek(0)

    img_base64 = base64.b64encode(img_io.read()).decode('utf-8')

    return {
        "data_uri_scheme": "data:image/png;base64,",
        "base64_data": img_base64,
        "img_tag_in_HTML":"<img src=data_uri_scheme+base64_data >"
    }