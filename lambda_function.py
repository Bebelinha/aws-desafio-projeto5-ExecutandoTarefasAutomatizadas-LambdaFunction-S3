import boto3
import datetime

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = "desafio5-s3-isa-099597654193"
    file_name = f"arquivo_s3_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    content = "Meu primeiro arquivo gerado no Lambda, incluso no S3 e automatizado pelo CloudFormation!!!"

    s3.put_object(Bucket=bucket_name, Key=file_name, Body=content)
    print(f"Arquivo {file_name} criado no bucket {bucket_name}")

    return {
        "statusCode": 200,
        "body": f"Arquivo {file_name} criado com sucesso no bucket {bucket_name}"
    }
