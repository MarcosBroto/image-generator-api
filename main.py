from fastapi import FastAPI
from google.cloud import storage
import json
import datetime
import sys
import os

app = FastAPI()

#if not sys.platform.startswith("linux"):
#    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/joanenricgarcias/Repositories/gcp-cr_genai-api/skiller-sandbox-ai-b7987e8977bc.json"


# Initialize the Google Cloud Storage client
storage_client = storage.Client()
bucket_name = "image-generator-api"
bucket = storage_client.bucket(bucket_name)


@app.get("/")
async def read_root():
    # The JSON response you want to return and store
    response_json = {"message": "Hello World"}

    # Convert the JSON data to a string and then encode to bytes
    json_bytes = json.dumps(response_json).encode('utf-8')

    # Generate a unique blob name using the current UTC timestamp
    blob_name = f"hello_{datetime.datetime.utcnow().isoformat()}.json"
    blob = bucket.blob(blob_name)

    # Upload the JSON data to the bucket
    blob.upload_from_string(json_bytes, content_type="application/json")

    # Return the JSON response to the client
    return response_json
