import string
from fastapi import FastAPI
from google.cloud import storage
import json
import datetime
import sys
import os
from pydantic import BaseModel
from vertexai.preview.vision_models import ImageGenerationModel
import vertexai

app = FastAPI()

#if not sys.platform.startswith("linux"):
#    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Google/image-generator-api-455015-381fd368b2df.json"

# Initialize the Google Cloud Storage client
storage_client = storage.Client()
bucket_name = "image-generator-api"
bucket = storage_client.bucket(bucket_name)

class Prompt(BaseModel):
    description: str

@app.post("/generate-image")
async def generate_image_controller(prompt: Prompt):
    generated_image = generate_image(prompt.description)
    blob_name = f"image_{datetime.datetime.utcnow().isoformat()}.jpg"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(generated_image, content_type="image/jpg")
    return blob.public_url

@app.get("/")
async def read_root():
    response_json = {"message": "Hello World"}
    json_bytes = json.dumps(response_json).encode('utf-8')
    blob_name = f"hello_{datetime.datetime.utcnow().isoformat()}.json"
    blob = bucket.blob(blob_name)
    blob.upload_from_string(json_bytes, content_type="application/json")
    return response_json

def generate_image(description: str):
    vertexai.init(project="image-generator-api-455015", location="us-central1")
    generation_model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
    images = generation_model.generate_images(
        prompt=description,
        number_of_images=1,
        aspect_ratio="1:1",
        negative_prompt="",
        person_generation="",
        safety_filter_level="",
        add_watermark=True,
    )
    return images[0].get_bytes()  # Ensure this is the correct way to get image bytes