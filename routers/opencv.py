import numpy as np
import cv2
from fastapi import  UploadFile,APIRouter, Response, status
from helpers import s3Bucket
from classifiers import face_cascade,eye_cascade
from opencvOperations import convertFastApiFileToOpenCVObject,generateFileNames,addReactangeToOpenCVObject,addTextToOpenCVObject
from uuid import uuid4
from env import url
from fileCheck import fileChecks
from pydantic import BaseModel
from models import response

ResponseWrapper = response.ResponseWrapper

# Router
router = APIRouter(
    prefix='/opencv'
)

async def convertImageToGrayLocally(file):
    try:
        contents,file_type = await fileChecks(file)
        image = await convertFastApiFileToOpenCVObject(contents)
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        filename = await generateFileNames(file,s3Bucket.SUPPORTED_FILE_TYPES)
        fileLocation = f'assets/{filename}'
        cv2.imwrite(fileLocation,gray)
        data = {"url":f'{url}/{fileLocation}'}
        response = ResponseWrapper(status.HTTP_201_CREATED,"Successfully Converted Image To Gray and Uploaded Locally",data)
        return response
    except Exception as error:
        response = ResponseWrapper(status.HTTP_500_INTERNAL_SERVER_ERROR,"Error Occured "+error,{error})
        return response 
        
    
async def convertImageToGrayUploads3(file):
    try:    
        contents,file_type = await fileChecks(file)
        image = await convertFastApiFileToOpenCVObject(contents)
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        img_encode =  cv2.imencode(f'.{s3Bucket.SUPPORTED_FILE_TYPES[file_type]}', gray)[1]
        data_encode = np.array(img_encode) 
        byte_encode = data_encode.tobytes()
        resp = await s3Bucket.s3_upload(contents=byte_encode, key=f'{uuid4()}.{s3Bucket.SUPPORTED_FILE_TYPES[file_type]}')
        response = ResponseWrapper(status.HTTP_201_CREATED,"Successfully Converted Image To Gray and Uploaded to s3 Bucket",resp)
        return response
    except Exception as error:
        response = ResponseWrapper(status.HTTP_500_INTERNAL_SERVER_ERROR,"Error Occured "+error,{error})
        return response 
    
async def detectFacesAndUploads3(file: UploadFile):
    try:
        contents,file_type = await fileChecks(file)
        arr= np.asarray(bytearray(contents), dtype="uint8")
        image = cv2.imdecode(arr, cv2.IMREAD_COLOR) 
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray ,1.1,4)
        for (x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),3)
        img_encode =  cv2.imencode(f'.{s3Bucket.SUPPORTED_FILE_TYPES[file_type]}', image)[1]
        data_encode = np.array(img_encode) 
        byte_encode = data_encode.tobytes()
        resp = await s3Bucket.s3_upload(contents=byte_encode, key=f'{uuid4()}.{s3Bucket.SUPPORTED_FILE_TYPES[file_type]}')
        response = ResponseWrapper(status.HTTP_201_CREATED,"Successfully Detected Faces and Uploaded to s3",resp)
        return response
    except Exception as error:
        response = ResponseWrapper(status.HTTP_500_INTERNAL_SERVER_ERROR,"Error Occured "+error,{error})
        return response 

async def detectFacesAndUploadLocally(file: UploadFile):
    try:
        contents,file_type = await fileChecks(file)      
        arr= np.asarray(bytearray(contents), dtype="uint8")
        image = cv2.imdecode(arr, cv2.IMREAD_COLOR) 
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray ,1.1,4)
        count =0 
        for (x,y,w,h) in faces:
            count = count + 1
            font = cv2.FONT_HERSHEY_SIMPLEX 
            org = (x, y-50)    
            fontScale = 1
            color = (255, 0, 0)  
            thickness = 2
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),3)
            cv2.putText(image, 'Face '+str(count), org, font,  
                   fontScale, color, thickness, cv2.LINE_AA) 
        filename = f'{uuid4()}.{s3Bucket.SUPPORTED_FILE_TYPES[file_type]}'
        fileLocation = f'assets/{filename}'
        cv2.imwrite(fileLocation, image)
        resp = {"url":f'{url}/{fileLocation}'}
        response = ResponseWrapper(status.HTTP_201_CREATED,"Successfully Detected Faces and saved locally",resp)
        return response
    except Exception as error:
        response = ResponseWrapper(status.HTTP_500_INTERNAL_SERVER_ERROR,"Error Occured "+error,{error})
        return response 
    
async def detectFacesEyesUploadLocally(file: UploadFile):
    try:
        contents,file_type = await fileChecks(file)      
        arr= np.asarray(bytearray(contents), dtype="uint8")
        image = cv2.imdecode(arr, cv2.IMREAD_COLOR) 
        gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray ,1.1,4)
        count =0 
        for (x,y,w,h) in faces:
            count = count + 1
            image = await addReactangeToOpenCVObject(image,x,y,w,h,(255,0,0),3)
            image = await addTextToOpenCVObject(image,x,y-40,"Face "+str(count),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
            roi_gray =  gray[y:y+h, x:x+w]
            roi_color = image[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            countEye = 0
            for(ex,ey,ew,eh) in eyes:
                countEye = countEye + 1
                roi_color = await addReactangeToOpenCVObject(roi_color,ex,ey,ew,eh,(255,0,0),3)
                roi_color = await addTextToOpenCVObject(roi_color,ex,ey-20,'Eye'+str(countEye),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),3)
        filename = f'{uuid4()}.{s3Bucket.SUPPORTED_FILE_TYPES[file_type]}'
        fileLocation = f'assets/{filename}'
        cv2.imwrite(fileLocation, image)
        resp = {"url":f'{url}/{fileLocation}'}
        response = ResponseWrapper(status.HTTP_201_CREATED,"Successfully Detected Faces with eyes and saved locally",resp)
        return response
    except Exception as error:
        response = ResponseWrapper(status.HTTP_500_INTERNAL_SERVER_ERROR,"Error Occured "+error,{error})
        return response 

async def resizeImage(file: UploadFile,percent: int):
    try:
        contents,file_type = await fileChecks(file)
        image = await convertFastApiFileToOpenCVObject(contents)
        (height_img,width_img) = image.shape[0:2]
        widht_k = int(width_img*percent/100)
        height_k = int(height_img*percent/100)
        image_keep_rt = cv2.resize(image,(widht_k,height_k),cv2.INTER_LINEAR)
        filename = await generateFileNames(file,s3Bucket.SUPPORTED_FILE_TYPES)
        fileLocation = f'assets/{filename}'
        cv2.imwrite(fileLocation,image_keep_rt)
        resp = {"url":f'{url}/{fileLocation}'}
        response = ResponseWrapper(status.HTTP_201_CREATED,"Successfully Resized Image",resp)
        return response
    except Exception as error:
        print(f'{error}')
        response = ResponseWrapper(status.HTTP_500_INTERNAL_SERVER_ERROR,"Error Occured "+str(error),{error})
        return response 
    
async def resizeImageToDimensions(file: UploadFile,width: int,height: int):
    try:
        contents,file_type = await fileChecks(file)
        image = await convertFastApiFileToOpenCVObject(contents)
        image_keep_rt = cv2.resize(image,(width,height),cv2.INTER_LINEAR)
        filename = await generateFileNames(file,s3Bucket.SUPPORTED_FILE_TYPES)
        fileLocation = f'assets/{filename}'
        cv2.imwrite(fileLocation,image_keep_rt)
        resp = {"url":f'{url}/{fileLocation}'}
        response = ResponseWrapper(status.HTTP_201_CREATED,"Successfully Converted Image To Gray",resp)
        return response
    except Exception as error:
        response = ResponseWrapper(status.HTTP_500_INTERNAL_SERVER_ERROR,"Error Occured "+str(error),{error})
        return response    
        

@router.post("/convertImageToGrayLocally")
async def convertImageToGrayLocallyAPI(file: UploadFile,response:Response):
    try:
        apiResponse = await convertImageToGrayLocally(file)
        response.status_code = apiResponse.httpCode
        return apiResponse
    
    except Exception as error:
        errorResponse = ResponseWrapper(status.HTTP_500_INTERNAL_SERVER_ERROR,f"Error Occured: {error}",{error})
        response.status_code = errorResponse.httpCode
        return errorResponse



@router.post("/convertImageToGrayUploads3")
async def convertImageToGrayUploads3API(file: UploadFile,response:Response):
    try:
        apiResponse = await convertImageToGrayUploads3(file)
        response.status_code = apiResponse.httpCode
        return apiResponse
    
    except Exception as error:
        errorResponse = ResponseWrapper(status.HTTP_500_INTERNAL_SERVER_ERROR,f"Error Occured: {error}",{error})
        response.status_code = errorResponse.httpCode
        return errorResponse


@router.post("/detectFacesAndUploadToS3")
async def detectFacesAndUploads3API(file: UploadFile,response:Response):
    try:
        apiResponse = await detectFacesAndUploads3(file)
        response.status_code = apiResponse.httpCode
        return apiResponse
    
    except Exception as error:
        errorResponse = ResponseWrapper(status.HTTP_500_INTERNAL_SERVER_ERROR,f"Error Occured: {error}",{error})
        response.status_code = errorResponse.httpCode
        return errorResponse



@router.post("/detectFacesAndUploadLocally")
async def detectFacesAndUploadLocallyAPI(file: UploadFile,response:Response):
    try:
        apiResponse = await detectFacesAndUploadLocally(file)
        response.status_code = apiResponse.httpCode
        return apiResponse
    
    except Exception as error:
        errorResponse = ResponseWrapper(status.HTTP_500_INTERNAL_SERVER_ERROR,f"Error Occured: {error}",{error})
        response.status_code = errorResponse.httpCode
        return errorResponse
    
@router.post("/detectFaceAndEyesLocally")
async def detectFacesEyesUploadLocallyAPI(file: UploadFile,response:Response):
    try:
        apiResponse = await detectFacesEyesUploadLocally(file)
        response.status_code = apiResponse.httpCode
        return apiResponse
    
    except Exception as error:
        errorResponse = ResponseWrapper(status.HTTP_500_INTERNAL_SERVER_ERROR,f"Error Occured: {error}",{error})
        response.status_code = errorResponse.httpCode
        return errorResponse
    
@router.post("/resizeImagePercent")
async def resizeImageAPI(file: UploadFile,percent: int,response:Response):
    try:
        apiResponse = await resizeImage(file,percent)
        response.status_code = apiResponse.httpCode
        return apiResponse
    
    except Exception as error:
        errorResponse = ResponseWrapper(status.HTTP_500_INTERNAL_SERVER_ERROR,f"Error Occured: {error}",{error})
        response.status_code = errorResponse.httpCode
        return errorResponse
    
@router.post("/resizeImageToDimensions")
async def resizeImageToDimensionsAPI(file: UploadFile,width: int,height: int,response:Response):
    try:
        apiResponse = await resizeImageToDimensions(file,width,height)
        response.status_code = apiResponse.httpCode
        return apiResponse
    
    except Exception as error:
        errorResponse = ResponseWrapper(status.HTTP_500_INTERNAL_SERVER_ERROR,f"Error Occured: {error}",{error})
        response.status_code = errorResponse.httpCode
        return errorResponse      