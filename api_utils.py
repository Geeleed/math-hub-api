from header import *

# สุ่มคำสร้างประโยคเพื่อใช้ทดลอง
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
@app.get("/lorem")
def generate_lorem(length: int=5):
    lorem_text = " ".join(random.choice(lorem_words) for _ in range(length))
    return {"lorem_text": lorem_text}

# api เข้ารหัสข้อความ sha256
@app.get('/sha256/{text}')
def sha256(text:str):
    hashlib.sha512
    inst = hashlib.sha256()
    inst.update(text.encode('utf-8'))
    hash_binary = inst.digest()
    hash_hex = hash_binary.hex()
    return {"hash_hex":hash_hex}

# api เข้ารหัสข้อความ sha512
@app.get('/sha512/{text}')
def sha256(text:str):
    inst = hashlib.sha512()
    inst.update(text.encode('utf-8'))
    hash_binary = inst.digest()
    hash_hex = hash_binary.hex()
    return {"hash_hex":hash_hex}

# delay in second
@app.get('/delay/{second}')
async def delay(second:float):
    await time.sleep(second)

# api เข้ารหัสไฟล์แปลงเป็นข้อความ base64
@app.post('/file2base64')
async def convert_file_to_base64(file:UploadFile):
    filedata = await file.read()
    base64_data = base64.b64encode(filedata).decode('utf-8')
    return {"base64_data":base64_data}


# api เข้ารหัสไฟล์แปลงเป็นข้อความ base64 แบบรับมาทีละหลายไฟล์
@app.post('/files2base64')
async def convert_files_to_base64(files: List[UploadFile] = File(...)):
    base64_data_list = []

    for file in files:
        data = await file.read()
        base64_data = base64.b64encode(data).decode('utf-8')
        base64_data_list.append(base64_data)

    return {"base64_data": base64_data_list}



# api สร้างภาพ qr-code แต่จะตอบกลับเป็น src ของ <img> ที่เป็น base64
@app.get("/generate-qr-code/{data:path}")
async def generate_qr_code(data: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=2,
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

# api ส่งไฟล์ภาพไปแล้วรับกลับมาเป็น src ของ <img src=srcที่ได้> ของ html
@app.post('/getSrcImgHtml')
async def get_src_img_html(file:UploadFile):
    data = await file.read()
    base64_data = base64.b64encode(data).decode('utf-8')
    return {"src":"data:image;base64,"+base64_data}


# api คำนวณ BMI โดยใช้ method POST
@app.post('/bmi')
def calc_BMI(weight_kg: float=Form(...), height_cm: float=Form(...)):
    height_m = height_cm / 100
    your_BMI = weight_kg / (height_m ** 2)
    return {"your_BMI": your_BMI}

# api รับ src ที่เป็น base64 ของ <img> จาก image url
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

random_image_url = lambda : requests.get('https://source.unsplash.com/random').url

# api generate post จะสร้างโพสต์ที่มี id title image description แบบสุ่มให้ เลือกได้ว่าจะเอากี่โพสต์
@app.get('/gen-post')
def gen_posts(n:int=1):
    temp = []
    image_unsplash_url = 'https://source.unsplash.com/random/400x400/?sig='
    for i in range(n):
        title = generate_lorem(random.randint(3,5))['lorem_text']
        image_url = image_unsplash_url+str(i)
        description = generate_lorem(random.randint(25,100))['lorem_text']
        temp.append({"id":i,"title":title,"img_src":image_url,"description":description})
    return temp

# api คำภาษาอังกฤษ
@app.get('/en-words')
def en_words():
    words = requests.get('https://raw.githubusercontent.com/Geeleed/CollectTheWords/main/EN_words.json')
    data = json.loads(words.text)
    return data

# api คำภาษาไทย
@app.get('/th-words')
def th_words():
    words = requests.get('https://raw.githubusercontent.com/Geeleed/CollectTheWords/main/TH_words.json')
    data = json.loads(words.text)
    return data

# api dictionary english to thai
@app.get('/en2th')
def en2th():
    words = requests.get('https://raw.githubusercontent.com/Geeleed/CollectTheWords/main/EN2TH_Dict.json')
    data = json.loads(words.text)
    return data

# # WebSocket endpoint
# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await websocket.accept()
#     while True:
#         data = await websocket.receive_text()
#         await websocket.send_text(f"Message text was: {data} ")

# api ตรวจสอบสิทธิ์การเข้าถึงข้อมูล
# @app.post('/auth/{token}')
# def authentication():
#     pass