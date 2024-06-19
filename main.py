# coding=utf-8
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.tag_extractor import TagExtractor
import pymorphy2

app = FastAPI()
origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "https://192.168.1.45:8080",
    "http://192.168.1.45:8080"
    
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/favicon.ico")
async def ignore_favicon():
    return {}


@app.get("/", )
async def get_tags(text):
    response = ""
    if text:
        tag_extractor = TagExtractor()
        tag_index = 1
        for tag in tag_extractor(text, nested=True, strings=True, limit=10):
            response += tag + ","
            tag_index += 1
    return response[:-1]


tag_extractor2 = TagExtractor()
print(tag_extractor2("Съешь ещё этих мягких французских булок да выпей же чаю", nested=True, strings=True, limit=10))