# คำสั่งเปิดเซิฟเวอร์ uvicorn main:app --port 8002 --reload

import requests
from io import BytesIO, StringIO
import qrcode
from typing import List
import base64
import time
import hashlib
import random
import json
from scipy.stats import linregress
import math
import numpy as np
# from bs4 import BeautifulSoup

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
app = FastAPI()
# อนุญาตให้เข้าถึง API จากทุกๆ โดเมนหรือ URL
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"],)

# from api_calc import *