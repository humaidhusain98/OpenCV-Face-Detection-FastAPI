import sys
import time

# Loading Environment Variable
from dotenv import load_dotenv
load_dotenv()

# Inserting Folders and its python files to our path
sys.path.insert(0, 'opencv')
sys.path.insert(0, 'helpers')
sys.path.insert(0, 'routers')
sys.path.insert(0, 'models')

from fastapi import FastAPI,Request
from fastapi.staticfiles import StaticFiles
import opencv

# CORS Configuration
from fastapi.middleware.cors import CORSMiddleware
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

# Initializing Fast API app
app = FastAPI()

# Adding CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mounting the assets folder in /assets route
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Adding OpenCV Router
app.include_router(opencv.router)

# Middleware controlling every request
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f'Processing Time process_time :{process_time}')
    return response

# Main 
@app.get("/")
async def root():
    return {"message": "PYTHON MODELS"}





