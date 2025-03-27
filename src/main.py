from fastapi import FastAPI, HTTPException
from google.cloud import storage
import openai
import os
import base64

# Configurar API Key de Gemini
openai.api_key = os.getenv("GEMINI_API_KEY")

app = FastAPI()

# Configurar cliente de Cloud Storage
storage_client = storage.Client()
BUCKET_NAME = "tu-bucket-name"

@app.post("/generate-image/")
async def generate_image(prompt: str):
    try:
        # 1. Enviar solicitud a Gemini
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response["data"][0]["url"]

        # 2. Descargar la imagen
        image_data = openai.util.download_file(image_url)

        # 3. Guardar en Cloud Storage
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"images/{prompt.replace(' ', '_')}.png")
        blob.upload_from_string(image_data, content_type="image/png")

        return {"message": "Imagen generada", "image_url": f"gs://{BUCKET_NAME}/{blob.name}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))