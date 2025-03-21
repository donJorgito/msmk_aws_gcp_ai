iimport boto3

def lambda_handler(event, context):
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': 'mkms-demo-bucket', 'Name': 'imagen.jpg'}},
        MaxLabels=10
    )
    return response['Labels']
