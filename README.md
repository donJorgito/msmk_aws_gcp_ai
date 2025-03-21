# Taller de Cloud AI: AWS Rekognition vs Google Vertex AI

Taller práctico para comparar servicios de análisis de imágenes usando AWS Rekognition + Lambda y Google Vertex AI con Gemini.

## Ejercicio 1: AWS Rekognition + Lambda

### Prerrequisitos
- Cuenta AWS (Free Tier)
- AWS CLI configurado
- Python 3.8+

### Pasos

1. **Crear bucket S3**
\```bash
aws s3api create-bucket --bucket msmk-rekognition-demo --region us-east-1
\```

2. **Subir imagen de prueba**
\```bash
aws s3 cp demo-imagen.jpg s3://msmk-rekognition-demo/
\```

3. **Crear Rol IAM**
   - Servicio: Lambda
   - Políticas adjuntas:
     - `AWSRekognitionFullAccess`
     - `AmazonS3ReadOnlyAccess`
     - `AWSLambdaBasicExecutionRole`

4. **Crear función Lambda (Python 3.12)**
\```python
import boto3

def lambda_handler(event, context):
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_labels(
        Image={'S3Object': {
            'Bucket': 'msmk-rekognition-demo',
            'Name': 'demo-imagen.jpg'
        }},
        MaxLabels=10
    )
    return [label['Name'] for label in response['Labels']]
\```

5. **Configurar**
   - Timeout: 30 segundos
   - Rol: El creado en paso 3

6. **Probar**
\```bash
aws lambda invoke --function-name analizar-imagen-rekognition output.txt
\```

## Ejercicio 2: Google Vertex AI + Gemini

### Prerrequisitos
- Cuenta Google Cloud ($300 free trial)
- Proyecto creado en GCP Console

### Pasos

1. **Habilitar APIs**
   - Vertex AI API
   - Generative Language API

2. **Crear bucket Cloud Storage**
\```bash
gsutil mb -l us-central1 gs://msmk-demo-gemini
gsutil cp demo-imagen.jpg gs://msmk-demo-gemini
gsutil iam ch allUsers:objectViewer gs://msmk-demo-gemini
\```

3. **Crear entorno Python**
\```bash
python -m venv venv
source venv/bin/activate
pip install google-cloud-aiplatform pillow requests
\```

4. **Código de análisis (gemini_analysis.py)**
\```python
from vertexai.preview.generative_models import GenerativeModel, Part
import vertexai
import requests

vertexai.init(project="TU_PROYECTO", location="us-central1")

# Descargar imagen
image_url = "https://storage.googleapis.com/msmk-demo-gemini/demo-imagen.jpg"
image_data = requests.get(image_url).content

# Crear input para Gemini
model = GenerativeModel("gemini-pro-vision")
response = model.generate_content([
    "Describe esta imagen en detalle técnico:",
    Part.from_data(image_data, mime_type="image/jpeg")
])

print(response.text)
\```

5. **Ejecutar**
\```bash
export GOOGLE_APPLICATION_CREDENTIALS="ruta/tus-credenciales.json"
python gemini_analysis.py
\```

## Comparación de Servicios

| Característica          | AWS Rekognition                          | Google Gemini                          |
|-------------------------|------------------------------------------|----------------------------------------|
| Tipo de análisis         | Pre-entrenado (objetos, texto, caras)    | Multimodal (imagen + texto conversacional) |
| Integración nativa      | S3, Lambda, API Gateway                  | Cloud Storage, BigQuery, Firebase      |
| Mejor uso               | Moderación de contenido, reconocimiento  | Chatbots creativos, análisis contextual |
| Precio (1k imágenes)    | ~$1.00                                   | ~$2.50                                 |
| Latencia típica         | 500-1500ms                               | 1000-3000ms                            |

## Solución de Problemas Comunes

### AWS
- **AccessDeniedException**: Verificar políticas del rol IAM
- **InvalidS3ObjectException**: Revisar nombre del bucket/archivo
- **ImageTooLargeException**: Redimensionar imagen (<5MB)

### Google Cloud
- **PermissionDenied 403**: Verificar permisos del bucket
- **InvalidArgument 400**: Formato de imagen no soportado
- **ModelTimeout**: Reducir tamaño de imagen o usar `async`

## FAQ

**¿Necesito tarjeta de crédito?**  
Sí, para ambas plataformas (no se cobrará nada en Free Tier).

**¿Puedo usar mis propias imágenes?**  
Sí, ambos ejercicios soportan imágenes personalizadas (JPEG/PNG <4MB).

**¿Cómo evitar costos inesperados?**  
- AWS: Establecer alarmas de billing en CloudWatch  
- GCP: Configurar budget alerts en Billing Console
