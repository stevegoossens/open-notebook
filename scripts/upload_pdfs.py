#!/usr/bin/env python3
import os
import argparse
import mimetypes
import urllib.request
import urllib.error
import uuid

def upload_file(api_url, file_path, notebook_id, transformation_id):
    """
    Upload a single PDF file to the Open-Notebook API using multipart/form-data.
    """
    boundary = "----Boundary" + uuid.uuid4().hex
    CRLF = "\r\n"

    filename = os.path.basename(file_path)
    mime_type = mimetypes.guess_type(file_path)[0] or "application/pdf"

    # Build multipart body
    parts = []
    def add_field(name, value):
        parts.append(f"--{boundary}{CRLF}")
        parts.append(f'Content-Disposition: form-data; name="{name}"{CRLF}{CRLF}')
        parts.append(f"{value}{CRLF}")

    def add_file_field(name, filepath):
        parts.append(f"--{boundary}{CRLF}")
        parts.append(f'Content-Disposition: form-data; name="{name}"; filename="{filename}"{CRLF}')
        parts.append(f"Content-Type: {mime_type}{CRLF}{CRLF}")
        with open(filepath, "rb") as f:
            parts.append(f.read())
        parts.append(CRLF)

    # Add fields
    add_field("type", "upload")
    add_field("notebooks", f'["{notebook_id}"]')
    add_field("transformations", f'["{transformation_id}"]')
    add_file_field("file", file_path)
    add_field("embed", "true")
    add_field("delete_source", "false")
    add_field("async_processing", "true")

    # End boundary
    parts.append(f"--{boundary}--{CRLF}")

    # Join body
    body = b"".join(p.encode() if isinstance(p, str) else p for p in parts)

    headers = {
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Authorization": "Bearer not-required",
    }

    req = urllib.request.Request(api_url, data=body, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as resp:
            print(f"[OK] {filename} → {resp.status} {resp.reason}")
            print(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"[ERROR] {filename} → {e.code} {e.reason}")
        print(e.read().decode())
    except urllib.error.URLError as e:
        print(f"[ERROR] {filename} → {e.reason}")


def main():
    parser = argparse.ArgumentParser(description="Upload all PDFs in a directory to Open-Notebook API")
    parser.add_argument("pdf_dir", help="Directory containing PDF files")
    parser.add_argument("--api-url", default="http://localhost:5055/api/sources", help="Open-Notebook API URL")
    parser.add_argument("--notebook-id", required=True, help="Target notebook ID (e.g. notebook:xhp2vroodo295c5ij08a)")
    parser.add_argument("--transformation-id", required=True, help="Transformation ID (e.g. transformation:d8qv0chqj9yyhjujbrkb)")
    args = parser.parse_args()

    for fname in os.listdir(args.pdf_dir):
        if fname.lower().endswith(".pdf"):
            fpath = os.path.join(args.pdf_dir, fname)
            upload_file(args.api_url, fpath, args.notebook_id, args.transformation_id)


if __name__ == "__main__":
    main()
