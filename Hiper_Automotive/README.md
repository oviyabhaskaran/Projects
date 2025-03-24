# FastAPI File Upload Service

This FastAPI application provides an endpoint to upload files in chunks and assemble them on the server.

## Features

- Supports chunked file uploads
- Verifies chunk integrity using checksums
- Assembles uploaded chunks into a complete file
- Provides file status (complete, pending, or missing)

## Installation

Ensure you have Python 3.11 installed. Then, install dependencies:

```sh
pip install fastapi uvicorn
```

## Running the Application

Start the FastAPI server:

```sh
uvicorn main:app --reload
```

The application will be available at: `http://127.0.0.1:8000`

## Uploading a File

Use the following `curl` command to upload a file:

```sh
curl -X 'POST' \
  'http://127.0.0.1:8000/upload/' \
  -H 'accept: application/json' \
  -H 'content-range: bytes 0-1023/5000' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_file.pdf;type=application/pdf'
```

## Checking File Status

To check the status of an uploaded file, use:

```sh
curl -X 'GET' 'http://127.0.0.1:8000/status?filename=your_file.pdf'
```

## API Endpoints

- `POST /upload/` - Uploads a file chunk
- `GET /status` - Checks file upload status

## Authentication

If the API requires authentication, ensure you pass the appropriate token:

```sh
-H 'Authorization: Bearer YOUR_JWT_TOKEN'
```

## License

This project is licensed under the MIT License.
