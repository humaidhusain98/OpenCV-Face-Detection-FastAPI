import cv2
import numpy as np
from uuid import uuid4

async def convertFastApiFileToOpenCVObject(contents):
    arr= np.asarray(bytearray(contents), dtype="uint8")
    imageOpenCV = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return imageOpenCV

async def generateFileNames(file,SUPPORTED_FILE_TYPES):
    file_type = file.filename.split('.')[1]
    file_type = f'image/{file_type}'
    filename = f'{uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}'
    return filename

async def addTextToOpenCVObject(image,x,y,text,font,fontScale,color,thickness):
    if not font:
        font = cv2.FONT_HERSHEY_SIMPLEX 
    if not x or not y:
        return "Undefined cordinates"
    org = (x, y) 
    if not fontScale:
        fontScale = 1
    if not color:
        color = (255, 0, 0)  
    if not thickness: 
        thickness = 2
    cv2.putText(image,text, org, font,  
                   fontScale, color, thickness, cv2.LINE_AA) 
    print(f'Add Rectangle To OpenCV')
    return image

async def addReactangeToOpenCVObject(image,x,y,w,h,color,thickness):
    if not color:
        color = (255, 0, 0) 
    if not thickness:
        thickness = 2
    cv2.rectangle(image,(x,y),(x+w,y+h),color,thickness)
    print(f'addTextToOpenCVObject')
    return image