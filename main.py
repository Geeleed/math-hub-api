# คำสั่งเปิดเซิฟเวอร์ uvicorn main:app --port 8002 --reload

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# อนุญาตให้เข้าถึง API จากทุกๆ โดเมนหรือ URL
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)

import math
import numpy as np
import scipy as sp
import hashlib

@app.get('/')
def root():
    return '<Geeleed/> สวัสดีครับ api นี้พยายามรวบรวมคณิตศาสตร์ต่าง ๆ ที่ใช้งานบ่อย ๆ มาทำเป็น api ไว้ โดยสามารถไปที่ /docs เพื่อดูรายละเอียดของ api ต่าง ๆ ได้ ขอบคุณครับ'

# api เข้ารหัสข้อความ sha256
@app.get('/sha256/{text}/')
def sha256(text:str):
    inst = hashlib.sha256()
    inst.update(text.encode('utf-8'))
    hash_binary = inst.digest()
    hash_hex = hash_binary.hex()
    return {"hash_hex":hash_hex}

# api แปลงเลขฐาน
@app.get('/convert_base/{number}/{from_base}/{to_base}/')
def convert_base(number,from_base=10,to_base=16):
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
    return {"result":result}

# สุ่มตัวเลข
@app.get("/random/{Min}/{Max}/{Num}/")
def random_number(Min:float,Max:float,Num:int):
    return {"result":np.random.uniform(Min,Max,Num).tolist()}

# การจัดเรียงแบบ permutation
@app.get("/permutation/{n}/{r}/")
def permuation(n: int , r : int ):
    return {"result":math.factorial(n)/math.factorial(n-r)}

# การจัดเรียงแบบ commutation
@app.get("/commutation/{n}/{r}/")
def commutation(n: int , r : int ):
    return {"result":math.factorial(n)/math.factorial(n-r)/math.factorial(r)}

# delay in second
import time
@app.get('/delay/{second}/')
def delay(second:float):
    time.sleep(second)

# linear fitting from csv
# example:
# x,y
# 1.0,2.3
# 2.0,3.5
# 3.0,4.2
# 4.0,5.0
# 5.0,6.1
from scipy.stats import linregress
from io import StringIO

def read_csv(file_contents):
    data = []
    csv_file = StringIO(file_contents.decode('utf-8'))
    data = np.genfromtxt(csv_file, delimiter=',', skip_header=1, dtype=float)
    return data

@app.post("/linear-fit-2d/")
async def linear_fit_2D(file: UploadFile):
    # อ่านข้อมูล CSV
    try:
        data = read_csv(await file.read())
    except Exception as e:
        return {'error': f'Failed to read CSV file: {str(e)}'}
    
    # ตรวจสอบว่ามีข้อมูลอย่างน้อย 2 จุด
    if len(data) < 2:
        return {'error': 'CSV file must have at least 2 data points'}

    # ทำ linear fitting
    x,y = np.transpose(data)
    result = linregress(x, y)
    
    # คำนวณค่าสถิติเพิ่มเติม
    residuals = y - (result.slope * x + result.intercept)
    sse = np.sum(residuals ** 2)  # Sum of Squares Error (SSE)
    sst = np.sum((y - np.mean(y)) ** 2)  # Total Sum of Squares (SST)
    rsquared = 1 - (sse / sst)  # R-squared (R^2)
    
    # ส่งผลลัพธ์กลับเป็น JSON
    response = {
        'Slope': result.slope,
        'y_intercept': result.intercept,
        'R_value': result.rvalue,
        'P_value': result.pvalue,
        'Standard_Error_of_Slope': result.stderr,
        'R_squared': rsquared,
        'Sum_of_Squares_Error__SSE': sse,
        'Total_Sum_of_Squares__SST': sst
    }
    return response

# สร้าง API สำหรับแปลงสี RGB เป็น HSL
# https://www.rapidtables.com/convert/color/rgb-to-hsl.html
def rgb_to_hsl(red:float,green:float,blue:float):
    r = red/255; g = green/255; b = blue/255
    cmin = min(r,g,b); cmax = max(r,g,b); d = cmax-cmin
    if cmax == 0 or d == 0: h = 0
    elif r == cmax: h = 60*((g-b)%6)/d
    elif g == cmax: h = 60*(2+(b-r)/d)
    elif b == cmax: h = 60*(4+(r-g)/d)
    l = (cmax+cmin)/2
    if d==0: s = 0
    else: s = d/(1-abs(2*l-1))
    return {"hue": h, "saturation": s, "lightness": l}
@app.get("/rgb2hsl/{red}/{green}/{blue}/")
def rgb2hsl(red:float,green:float,blue:float):
    hsl = rgb_to_hsl(red,green,blue)
    return {"hue": hsl['hue'], "saturation": hsl['saturation'], "lightness": hsl['lightness']}

# สร้าง API สำหรับแปลงสี HSL เป็น RGB
# https://www.rapidtables.com/convert/color/hsl-to-rgb.html
def hsl_to_rgb(hue:float,saturation:float,lightness:float):
    h, s, l = hue, saturation, lightness
    c = (1-abs(2*l-1))*s
    x = c*(1-abs(((h/60)%2)-1))
    m = l-c/2
    if 0<=h<60: r,g,b = c,x,0.
    elif 60<=h<120: r,g,b = x,c,0
    elif 120<=h<180: r,g,b = 0,c,x
    elif 180<=h<240: r,g,b = 0,x,c
    elif 240<=h<300: r,g,b = x,0,c
    elif 300<=h<360: r,g,b = c,0,x
    red = (r+m)*255
    green = (g+m)*255
    blue = (b+m)*255
    return {"red": red, "green": green, "blue": blue}
@app.get("/hsl2rgb/{hue}/{saturation}/{lightness}/")
def hsl2rgb(hue:float,saturation:float,lightness:float):
    rgb = hsl_to_rgb(hue,saturation,lightness)
    return {"red": rgb['red'], "green": rgb['green'], "blue": rgb['blue']}

# สร้าง API สำหรับแปลงสี RGB เป็น HSV
# https://www.rapidtables.com/convert/color/rgb-to-hsv.html
def rgb_to_hsv(red:float,green:float,blue:float):
    r = red/255; g = green/255; b = blue/255
    cmin = min(r,g,b); cmax = max(r,g,b); d = cmax-cmin
    if cmax == 0 or d == 0: h = 0
    elif r == cmax: h = 60*((g-b)%6)/d
    elif g == cmax: h = 60*(2+(b-r)/d)
    elif b == cmax: h = 60*(4+(r-g)/d)
    v = cmax/2
    if cmax==0: s = 0
    else: s = d/cmax
    return {"hue": h, "saturation": s, "value": v}
@app.get("/rgb2hsv/{red}/{green}/{blue}/")
def rgb2hsv(red:float,green:float,blue:float):
    hsv = rgb_to_hsv(red,green,blue)
    return {"hue": hsv['hue'], "saturation": hsv['saturation'], "value": hsv['value']}

# สร้าง API สำหรับแปลงสี HSV เป็น RGB
# https://www.rapidtables.com/convert/color/hsv-to-rgb.html
def hsv_to_rgb(hue:float,saturation:float,value:float):
    h, s, v = hue, saturation, value
    c = v*s
    x = c*(1-abs(((h/60)%2)-1))
    m = v-c
    if 0<=h<60: r,g,b = c,x,0.
    elif 60<=h<120: r,g,b = x,c,0
    elif 120<=h<180: r,g,b = 0,c,x
    elif 180<=h<240: r,g,b = 0,x,c
    elif 240<=h<300: r,g,b = x,0,c
    elif 300<=h<360: r,g,b = c,0,x
    red = (r+m)*255
    green = (g+m)*255
    blue = (b+m)*255
    return {"red": red, "green": green, "blue": blue}
@app.get("/hsv2rgb/{hue}/{saturation}/{value}/")
def hsv2rgb(hue:float,saturation:float,value:float):
    rgb = hsv_to_rgb(hue,saturation,value)
    return {"red": rgb['red'], "green": rgb['green'], "blue": rgb['blue']}


# สร้าง API สำหรับแปลงสี RGB เป็น CMYK
# https://www.rapidtables.com/convert/color/rgb-to-cmyk.html
def rgb_to_cmyk(red:float,green:float,blue:float):
    r = red/255; g = green/255; b = blue/255
    k = 1-max(r,g,b) # black
    c = (1-r-k)/(1-k)
    m = (1-g-k)/(1-k)
    y = (1-b-k)/(1-k)
    return {"cyan":c,"magenta":m,"yellow":y,"key":k}
@app.get("/rgb2cmyk/{red}/{green}/{blue}/")
def rgb2cmyk(red:float,green:float,blue:float):
    cmyk = rgb_to_cmyk(red,green,blue)
    return {"cyan":cmyk['cyan'],"magenta":cmyk['magenta'],"yellow":cmyk['yellow'],"key":cmyk['key']}

# สร้าง API สำหรับแปลงสี CMYK เป็น RGB
# https://www.rapidtables.com/convert/color/cmyk-to-rgb.html
def cmyk_to_rgb(cyan:float,magenta:float,yellow:float,key:float):
    c,m,y,k = cyan,magenta,yellow,key
    r = 255*(1-c)*(1-k)
    g = 255*(1-m)*(1-k)
    b = 255*(1-y)*(1-k)
    return {"red": r, "green": g, "blue": b}
@app.get("/cmyk2rgb/{cyan}/{magenta}/{yellow}/{key}/")
def cmyk2rgb(cyan:float,magenta:float,yellow:float,key:float):
    rgb = cmyk_to_rgb(cyan,magenta,yellow,key)
    return {"red": rgb['red'], "green": rgb['green'], "blue": rgb['blue']}

# api แปลงโหมดสี
import json
@app.get('/convert-color-mode/{color_array}/{from_mode}/{to_mode}')
def convert_color_mode(color_array:str,from_mode:str,to_mode:str):
    color_array = json.loads(color_array)
    if from_mode == 'rgb' and to_mode == 'hsl':
        return rgb_to_hsl(*color_array)
    elif from_mode == 'rgb' and to_mode == 'hsv':
        return rgb_to_hsv(*color_array)
    elif from_mode == 'rgb' and to_mode == 'cmyk':
        return rgb_to_cmyk(*color_array)
    elif from_mode == 'hsl' and to_mode == 'rgb':
        return hsl_to_rgb(*color_array)
    elif from_mode == 'hsl' and to_mode == 'hsv':
        rgb = hsl_to_rgb(*color_array)
        return rgb_to_hsv(rgb['red'],rgb['green'],rgb['blue'])
    elif from_mode == 'hsl' and to_mode == 'cmyk':
        rgb=hsl_to_rgb(*color_array)
        return rgb_to_cmyk(rgb['red'],rgb['green'],rgb['blue'])
    elif from_mode == 'hsv' and to_mode == 'rgb':
        return hsv_to_rgb(*color_array)
    elif from_mode == 'hsv' and to_mode == 'hsl':
        rgb = hsv_to_rgb(*color_array)
        return rgb_to_hsl(rgb['red'],rgb['green'],rgb['blue'])
    elif from_mode == 'hsv' and to_mode == 'cmyk':
        rgb = hsv_to_rgb(*color_array)
        return rgb_to_cmyk(rgb['red'],rgb['green'],rgb['blue'])
    elif from_mode == 'cmyk' and to_mode == 'rgb':
        return cmyk_to_rgb(*color_array)
    elif from_mode == 'cmyk' and to_mode == 'hsl':
        rgb = cmyk_to_rgb(*color_array)
        return rgb_to_hsl(rgb['red'],rgb['green'],rgb['blue'])
    elif from_mode == 'cmyk' and to_mode == 'hsv':
        rgb = cmyk_to_rgb(*color_array)
        return rgb_to_hsv(rgb['red'],rgb['green'],rgb['blue'])