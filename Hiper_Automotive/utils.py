import os

def verify_chunk(file, content_range):
    """Parses and verifies chunk integrity."""
    range_info = content_range.split(" ")[1].split("/")
    start_byte, end_byte = map(int, range_info[0].split("-"))
    checksum = sum(file.read()) % 256
    
    return start_byte, end_byte, checksum

def assemble_file(file_path, chunk_dir):
    """
    Assembles the full file from its chunks.
    
    :param file_path: Path to save the assembled file.
    :param chunk_dir: Directory where file chunks are stored.
    :return: None
    """
    with open(file_path, "wb") as final_file:
        chunk_files = sorted(Path(chunk_dir).glob("*.chunk"), key=lambda x: int(x.stem))
        for chunk in chunk_files:
            with open(chunk, "rb") as f:
                final_file.write(f.read())
                
def get_file_status(filename, upload_dir):
    """Returns file status: complete, partial, or missing."""
    file_path = os.path.join(upload_dir, filename)
    
    if os.path.exists(file_path):
        return {"status": "complete", "size": os.path.getsize(file_path)}
    return {"status": "pending", "size": 0}
