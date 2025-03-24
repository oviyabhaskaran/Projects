from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header
from fastapi.responses import StreamingResponse
import os
import shutil
from auth import verify_token
from utils import verify_chunk, assemble_file, get_file_status
from background import cleanup_old_files

app = FastAPI()

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    token: str = Depends(verify_token),
    content_range: str = Header(None)
):
    """Handles file chunk uploads and assembles files when complete."""
    if not content_range:
        raise HTTPException(status_code=400, detail="Content-Range header missing")
    
    start_byte, end_byte, checksum = verify_chunk(file.file, content_range)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "ab") as f:
        f.seek(start_byte)
        shutil.copyfileobj(file.file, f)

    return {"message": "Chunk received", "start_byte": start_byte, "end_byte": end_byte}

@app.get("/download/{filename}")
async def download_file(filename: str, range: str = Header(None)):
    """Allows partial downloads using HTTP Range headers."""
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    file_size = os.path.getsize(file_path)
    
    start, end = (0, file_size - 1)  # Default to full file
    if range:
        start, end = [int(x) for x in range.replace("bytes=", "").split("-")]

    async def file_generator():
        with open(file_path, "rb") as f:
            f.seek(start)
            yield f.read(end - start + 1)

    return StreamingResponse(file_generator(), media_type="application/octet-stream", headers={"Content-Range": f"bytes {start}-{end}/{file_size}"})

@app.get("/status/{filename}")
async def file_status(filename: str):
    """Returns the current status of a file upload."""
    return get_file_status(filename, UPLOAD_DIR)

cleanup_old_files()
