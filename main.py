import os
from hmac import compare_digest
from fastapi import FastAPI, HTTPException, Request, Response

API_TOKEN = os.environ['API_TOKEN']

os.makedirs('Data', exist_ok=True)

app = FastAPI()

@app.put('/')
async def main(request: Request):
    header = request.headers.get('Authorization', '')
    
    if not header.startswith('Bearer '):
        raise HTTPException(status_code = 401)

    if not compare_digest(header[7:], API_TOKEN):
        raise HTTPException(status_code = 401)
    
    file_name = request.headers.get('x-filename')

    if not file_name:
        raise HTTPException(
            status_code = 400,
            detail = "Не указан 'x-filename'",
        )
    
    file_path = f'Data/{file_name}'

    try:
        with open(file_path, "wb") as file:
            async for chunk in request.stream():                
                file.write(chunk)

    except HTTPException:
        raise
    except Exception:
        raise

    return Response(status_code=201)

