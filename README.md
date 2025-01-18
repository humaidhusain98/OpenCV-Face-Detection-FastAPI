# OpenCV-Face-Detection-FastAPI
This is a FASTAPI backend server which leverages OpenCV Python Library to perform tasks on Images.  <br />
These tasks include: <br />
- convert Images to Gray and upload it on our local assets folder which will be server by the backend as static files <br />
- convert Images to Gray and upload it to AWS S3 Bucket  <br />
- detect faces in Images using the pre trained face classifiers and upload to local server  <br />
- detect faces in Images using the pre trained face classifiers and upload to AWS S3 Bucket <br />
- detect eyes in faces in Images using the pre trained classifiers and upload to Local server <br />
- detect eyes in faces in Images using the pre trained classifiers and upload to s3 Bucket <br />
- resizing operations can also be performed. <br />

# 🚀 FastAPI Project


---

## 🛠 Features
- 🔗 RESTful APIs with FastAPI
- 📜 Auto-generated Swagger & ReDoc API documentation
- 🗄️ Database integration with migrations support
- 🧪 Ready for development and production setups

---

## 📦 Installation Instructions

### 1. Clone the Repository
```bash
git clone git@github.com:humaidhusain98/OpenCV-Face-Detection-FastAPI.git
cd OpenCV-Face-Detection-FastAPI
```

### 2. Create a Virtual Environment
It's best practice to create a virtual environment for your Python projects:
```bash
python3 -m venv env
# Activate the virtual environment
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies
Install the required Python packages using pip and the requirements.txt
```bash
pip install -r requirements.txt
```

### 4.Set Up Environment Variables
Create a .env file in the root directory and add the necessary environment variables (if applicable). For example:
```env
localUrl=http://127.0.0.1:8000
prodUrl=
isDev=
AWS_SECRET_KEY_ID=
AWS_SECRET_ACCESS_KEY=
S3_BUCKET_URL=
```
