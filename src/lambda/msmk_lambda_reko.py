import boto3
import time
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    start_time = time.time()

    try:
        # Configuración
        bucket = "mkms-demo-reko-bucket"  # <-- Reemplaza con tu bucket
        imagen = "demo-image.jpg"                # <-- Nombre exacto de la imagen

        # Inicializa clientes
        s3 = boto3.client('s3')
        rekognition = boto3.client('rekognition')

        # Verifica que la imagen existe en S3 (debug)
        print("Verificando acceso a S3...")
        s3.head_object(Bucket=bucket, Key=imagen)

        # Procesa la imagen con Rekognition
        print("Analizando imagen con Rekognition...")
        response = rekognition.detect_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': imagen}},
            MaxLabels=10
        )

        # Resultados
        labels = [label['Name'] for label in response['Labels']]
        print("Etiquetas detectadas:", labels)

        return {
            'statusCode': 200,
            'body': f"Análisis exitoso en {time.time() - start_time:.2f}s. Etiquetas: {labels}"
        }

    except ClientError as e:
        print("Error de AWS:", e)
        return {
            'statusCode': 500,
            'body': f"Error: {e.response['Error']['Message']}"
        }

