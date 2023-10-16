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
    inst = hashlib.sha256()
    inst.update(text.encode('utf-8'))
    hash_binary = inst.digest()
    hash_hex = hash_binary.hex()
    return {"hash_hex":hash_hex}

# api เข้ารหัสข้อความ sha512
@app.get('/sha512/{text}')
def sha512(text:str):
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


def circleSelect(istart,ishift,length):
    return (ishift%length+istart)%length
def convertBase(number:str,from_base:int=10,to_base:int=16,lenHex=6):
    keyValue = {
        '0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9','10':'a','11':'b','12':'c','13':'d','14':'e','15':'f','a':'10','b':'11','c':'12','d':'13','e':'14','f':'15'
        }
    dec = int(number,from_base)
    result = ''
    while dec>0:
        remainder = dec%to_base
        result = keyValue[str(remainder)]+result
        dec //= to_base
    if len(result)<lenHex:
        return "0"*(lenHex-len(result))+result
    return result
def char2hex(char,lenHex=6):
    dec = str(ord(char))
    return convertBase(dec,10,16,lenHex)
def text2hex(text,lenHex=6):
    Hex = ''
    for c in text:
        Hex += char2hex(c,lenHex)
    return Hex
# เข้ารหัสข้อความส่วนตัว
def encryptor16(key:str,text:str):
    text = text2hex(text)
    char = '0123456789abcdef'
    L = len(char)
    init = sha256(key+str(len(text)))['hash_hex']
    LK = len(init)
    LT = len(text)
    numOfBox = math.ceil(LT/LK)
    # ตัดข้อความเป็นกล่อง ๆ
    splitToBox = []
    hashBox = []
    for i in range(numOfBox):
        start = i*LK
        # end = (i+1)*LK
        end = (i+1)*LK if i < numOfBox - 1 else LT
        txt = text[start:end]
        splitToBox.append(txt)
        hashBox.append(sha256(txt)['hash_hex'])
    hashBox = [init]+hashBox
    # เข้ารหัสแล้วเก็บทีละ box
    lock = ''
    for box in range(numOfBox):
        i = 0
        rec = ''
        for letter in splitToBox[box]:
            newInx = circleSelect(char.index(letter),int(hashBox[box][i],16),L)
            i += 1
            rec += char[newInx]
        lock += rec
    return lock
# ถอดรหัสข้อมูลส่วนตัว
def decryptor16(key:str,text:str):
    # กำหนดตารางเทียบ
    char = '0123456789abcdef'
    L = len(char)
    init = sha256(key+str(len(text)))['hash_hex']
    LK = len(init)
    LT = len(text)
    numOfBox = math.ceil(LT/LK)
    # ตัดข้อความเป็นกล่อง ๆ
    splitToBox = []
    for i in range(numOfBox):
        start = i*LK
        end = (i+1)*LK if i < numOfBox - 1 else LT
        txt = text[start:end]
        splitToBox.append(txt)
    unlock16 = ''
    hashBox = init
    for box in range(numOfBox):
        i = 0
        rec = ''
        for letter in splitToBox[box]:
            newInx = circleSelect(char.index(letter),-int(hashBox[i],16),L)
            i += 1
            rec += char[newInx]
        unlock16 += rec
        hashBox = sha256(rec)['hash_hex']
    splitToHex = []
    lenHex = 6
    for i in range(int(LT/lenHex)):
        start = i*lenHex
        end = (i+1)*lenHex
        txt = unlock16[start:end]
        splitToHex.append(txt)
    unlock = ''
    for hex in splitToHex:
        decrypt = int(hex,16)
        unlock += chr(decrypt)
    return unlock

# api เข้ารหัสและถอดรหัสข้อความส่วนตัวเป็นเลขฐาน 16 รองรับทุกอักขระ
@app.get('/cryptor16/{key}/{text}')
def cryptor16(key:str,text:str,mode='lock'):
    if mode=='lock':
        result = encryptor16(key,text)
    elif mode=='unlock':
        result = decryptor16(key,text)
    return {"result":result}

# api เข้ารหัสข้อมูลส่วนตัวโดยสามารถกำหนดเซตของตัวอักษรที่ใช้เพื่อเข้ารหัสได้
@app.get('/cryptcode/{key}/{text}')
def cryptcode(key:str, text:str, mode:str='lock',
    charSet:str = "`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./"+'\\'+' '
    +'~!@#$%^&*()_+QWERTYUIOP|ASDFGHJKL:"ZXCVBNM<>?'+'{'+'}'):
    # charSet:str = "`1234567890-=qwertyuiop[]asdfghjkl;'zxcvbnm,./\ ~!@#$%^&*()_+QWERTYUIOP|ASDFGHJKL:"+
    # '"ZXCVBNM<>?{'+'}ๅภถุึคตจขชๆไำพะัีรนยบลฃฟหกดเ้่าสวงผปแอิืทมใฝ๑๒๓๔ู฿๕๖๗๘๙๐ฎฑธํ๊ณฯญฐฅฤฆฏโฌ็๋ษศซฉฮฺ์ฒฬฦ'):
    lenChr = len(charSet)
    hex_key = sha256(key)['hash_hex']
    len_hex_key = len(hex_key)
    len_text = len(text)
    numOfBox = math.ceil(len_text/len_hex_key)
    for letterHexKey in hex_key:
        hash_term = sha256(letterHexKey)['hash_hex']
        result = []
        for box in range(numOfBox):
            start = box*len_hex_key
            end = (box+1)*len_hex_key if box < numOfBox-1 else len_text
            block = text[start:end]
            i = 0; newBlock = []
            for letter in block:
                ishift = 1 if mode=='lock' else -1
                newInx = circleSelect(charSet.index(letter),ishift*int(hash_term[i],16),lenChr)
                i += 1
                newLetter = charSet[newInx]
                newBlock.append(newLetter)
            block_add_hash = ''.join(newBlock)
            result.append(block_add_hash)
            hash_term = sha256(block)['hash_hex']
        text = ''.join(result)
    return {'result':text}

# api เข้ารหัสและถอดรหัสข้อมูลส่วนตัวเป็นเลขฐาน 16
# @app.post('/cryptcode16')
# def cryptcode16(key:str,text:str,
#     mode:str='lock'):
#     charSet = '0123456789abcdef'
#     lenHex = 6
#     text = text2hex(text,lenHex) if mode == 'lock' else text
#     text = cryptcode(key,text,mode,charSet)['result']
#     if mode == 'unlock':
#         splitToHex = []
#         for i in range(int(len(text)/lenHex)):
#             start = i*lenHex
#             end = (i+1)*lenHex
#             txt = text[start:end]
#             splitToHex.append(txt)
#         unlock = []
#         for hex in splitToHex:
#             decrypt = int(hex,16)
#             unlock.append(chr(decrypt))
#         text = ''.join(unlock)
#     return {'result':text}

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