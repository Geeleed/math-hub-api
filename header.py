# คำสั่งเปิดเซิฟเวอร์ uvicorn main:app --port 8002 --reload
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
# อนุญาตให้เข้าถึง API จากทุกๆ โดเมนหรือ URL
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)