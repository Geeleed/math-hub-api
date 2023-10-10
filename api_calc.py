from header import *

import math
import numpy as np

# api แปลงเลขฐาน
@app.get('/convert-base/{number}/{from_base}/{to_base}/')
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