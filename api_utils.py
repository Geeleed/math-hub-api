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
    "aliqua"
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
    filedata = await file.read()
    base64_data = base64.b64encode(filedata).decode('utf-8')
    return {"base64_data":base64_data}


# api เข้ารหัสไฟล์แปลงเป็นข้อความ base64 แบบรับมาทีละหลายไฟล์
from typing import List
@app.post('/files2base64/')
async def convert_files_to_base64(files: List[UploadFile] = File(...)):
    base64_data_list = []

    for file in files:
        data = await file.read()
        base64_data = base64.b64encode(data).decode('utf-8')
        base64_data_list.append(base64_data)

    return {"base64_data": base64_data_list}



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

    return {"src":"data:image;base64,"+img_base64}

# api ดูข้อมูลใน <input type='file' multiple> ของ html
# api ส่งไฟล์ภาพไปแล้วรับกลับมาเป็น src ของ <img src=srcที่ได้> ของ html
@app.post('/getSrcImgHtml/')
async def get_src_img_html(file:UploadFile):
    data = await file.read()
    base64_data = base64.b64encode(data).decode('utf-8')
    return {"src":"data:image;base64,"+base64_data}


# api คำนวณ BMI โดยใช้ method POST
@app.post('/bmi/')
def calc_BMI(weight_kg: float=Form(...), height_cm: float=Form(...)):
    height_m = height_cm / 100
    your_BMI = weight_kg / (height_m ** 2)
    return {"your_BMI": your_BMI}

# api รับ src ที่เป็น base64 ของ <img> จาก image url
import requests
@app.get("/url-to-img-src/{image_url:path}")
def download_image_to_img_src(image_url: str):
    # โหลดรูปภาพจาก URL ด้วย requests
    response = requests.get(image_url)
    if response.status_code != 200: return "Failed to download image"
    # อ่านข้อมูลรูปภาพและสร้างไฟล์รูปภาพ
    image_data = BytesIO(response.content)
    image_data.seek(0)
    img_base64 = base64.b64encode(image_data.read()).decode('utf-8')
    return {"img_src":"data:image;base64,"+img_base64}
    # return FileResponse(temp_image, media_type="image/jpeg")

# api generate post จะสร้างโพสต์ที่มี id title image description แบบสุ่มให้ เลือกได้ว่าจะเอากี่โพสต์
@app.get('/gen-post/{numOfPost}/')
def gen_posts(numOfPost:int):
    temp = []
    # image_unsplash_url = 'https://source.unsplash.com/random/400x400/?fruit,night,people,city,star'
    image_unsplash_url = 'https://source.unsplash.com/random/400x400'
    for i in range(numOfPost):
        title = generate_lorem(random.randint(3,5))['lorem_text']
        image_url = requests.get(image_unsplash_url).url
        description = generate_lorem(random.randint(25,100))['lorem_text']
        temp.append({"id":i,"title":title,"img_src":image_url,"description":description})
    return temp

