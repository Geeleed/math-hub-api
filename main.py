from header import *

from api_calc import *
from api_color import *
from api_utils import *

@app.get('/')
def root():
    return '<Geeleed/> สวัสดีครับ api นี้พยายามรวบรวมคณิตศาสตร์ต่าง ๆ ที่ใช้งานบ่อย ๆ มาทำเป็น api ไว้ และยังมี api อรรถประโยชน์อื่น ๆ ที่ใช้เป็นเครื่องมือสำหรับนักพัฒนาอีกด้วย โดยสามารถไปที่ /docs เพื่อดูรายละเอียดของ api ต่าง ๆ ได้ ขอบคุณครับ'