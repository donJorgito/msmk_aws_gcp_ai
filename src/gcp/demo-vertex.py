from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai
import requests
import base64

# Configurar proyecto
vertexai.init(project="mkms-demo-vertexai", location="us-central1")

# URL de la imagen
imagen_url = "https://storage.googleapis.com/mkms-demo-bucket/demo-image.jpg"

# Descargar imagen como bytes
response = requests.get(imagen_url)
response.raise_for_status()
imagen_bytes = response.content

# Convertir a base64 (formato que Vertex AI espera)
imagen_base64 = base64.b64encode(imagen_bytes).decode("utf-8")

# Crear objeto Part para Gemini
imagen_part = Part.from_data(
    data=base64.b64decode(imagen_base64),
    mime_type="image/jpeg"
)

# Generar respuesta
model = GenerativeModel("gemini-pro-vision")
respuesta = model.generate_content(
    contents=["Describe esta imagen en detalle:", imagen_part]
)

print(respuesta.text)
