# คำสั่งเปิดเซิฟเวอร์ uvicorn main:app --port 8002 --reload

from fastapi import FastAPI
import math
import numpy as np
import scipy as sp

app = FastAPI()

@app.get('/')
async def root():
    return '<Geeleed/> สวัสดีครับ api นี้พยายามรวบรวมคณิตศาสตร์ต่าง ๆ ที่ใช้งานบ่อย ๆ มาทำเป็น api ไว้ โดยสามารถไปที่ /docs เพื่อดูรายละเอียดของ api ต่าง ๆ ได้ ขอบคุณครับ'

# api เข้ารหัสข้อความ sha256
import hashlib
@app.get('/sha256/{text}/')
async def sha256(text:str):
    inst = hashlib.sha256()
    inst.update(text.encode('utf-8'))
    hash_binary = inst.digest()
    hash_hex = hash_binary.hex()
    return hash_hex

# api แปลงเลขฐาน
@app.get('/convert_base/{number}/{from_base}/{to_base}/')
async def convert_base(number,from_base=10,to_base=16):
    keyValue = {
        '0':'0','1':'1','2':'2','3':'3','4':'4','5':'5','6':'6','7':'7','8':'8','9':'9','10':'a','11':'b','12':'c','13':'d','14':'e','15':'f','a':'10','b':'11','c':'12','d':'13','e':'14','f':'15'
        }
    from_base = int(from_base)
    to_base = int(to_base)
    dec = int(str(number),from_base)
    result = ''
    while dec>0:
        remainder = dec%to_base
        result = keyValue[str(remainder)]+result
        dec //= to_base
    return result

# สุ่มตัวเลข
@app.get("/random/{min}/{max}/{num}/")
async def randomNumber(min:float,max:float,num:int):
    return np.random.uniform(float(min),float(max),int(num)).tolist()

# การจัดเรียงแบบ permutation
@app.get("/permutation/{n}/{r}/")
async def permuation(n: int , r : int ):
    return math.factorial(int(n))/math.factorial(int(n)-int(r))

# การจัดเรียงแบบ commutation
@app.get("/commutation/{n}/{r}/")
async def commutation(n: int , r : int ):
    return math.factorial(int(n))/math.factorial(int(n)-int(r))/math.factorial(int(r))

