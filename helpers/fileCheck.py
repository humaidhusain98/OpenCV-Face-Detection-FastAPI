from fastapi import HTTPException,status
from helpers import s3Bucket


async def fileChecks(file):
    if not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file found!!"
        )
        # Byte Format
    contents = await file.read()

    size = len(contents)
        
    if not 0 < size <= 2048*1024:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Supported file size is 0 - 1 MB'
        )
        
    file_type = file.filename.split('.')[1]
    file_type = f'image/{file_type}'
    print(file_type)
    if file_type not in s3Bucket.SUPPORTED_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail = f'Unsupported file type {file_type}. Supported types are {s3Bucket.SUPPORTED_FILE_TYPES}'
        )
    return contents,file_type