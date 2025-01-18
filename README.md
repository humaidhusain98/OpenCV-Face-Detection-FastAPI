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

Installation Instructions
Clone the Repository
Open your terminal and clone the FastAPI project repository:

bash
Copy
Edit
git clone <repository_url>
cd <repository_directory>
Create a Virtual Environment
It's best practice to create a virtual environment for your Python projects:

bash
Copy
Edit
python3 -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
Install Dependencies
Install the required Python packages using pip and the requirements.txt file:

bash
Copy
Edit
pip install -r requirements.txt
Set Up Environment Variables
Create a .env file in the root directory and add the necessary environment variables (if applicable). For example:

env
Copy
Edit
DATABASE_URL=postgresql://user:password@localhost/db_name
SECRET_KEY=your_secret_key
DEBUG=True
Run Database Migrations
If the project uses database migrations, apply them:

bash
Copy
Edit
alembic upgrade head  # If Alembic is used
Start Instructions
Run the FastAPI Development Server
Use the uvicorn command to start the development server:

bash
Copy
Edit
uvicorn app.main:app --reload
Replace app.main with the actual module and app instance path in your project (e.g., src.main:app).

Access the API
Once the server is running, the API will be available at:

arduino
Copy
Edit
http://127.0.0.1:8000
Explore the Documentation
FastAPI automatically generates interactive API docs:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc

