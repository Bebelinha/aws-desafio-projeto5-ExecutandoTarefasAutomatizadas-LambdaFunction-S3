# Executando Tarefas Automatizadas com Lambda Function e S3

Foi criada mais uma Stake no CloudFormation para o desafio 5 - Executando Tarefas Automatizadas com Lambda Function, S3 e IAM Role, o objetivo é gerar uma execução no Lambda Function para criar um arquivo em txt no bucket S3 juntamente com um IAM Role que cria uma função de execução que dá pemissão à Lambda para gravar os logs no CloudWatch e interagir com o S3.

O nome da Stake consta como desafio5-lambda-s3, nela o Lambda function contém uma função em Pthon 3.9 que, ao executada, cria um arquivo .txt dentro do bucket S3.

O nome do bucket S3 foi criado como FunctionName: !Sub "desafio5-lambda-isa-${AWS::AccountId}", que o ${AWS::AccountId} é o ID da conta AWS e ficou: desafio5-s3-isa-099597654193.

O nome do lambda function é desafio5-lambda-isa-099597654193 (FunctionName: !Sub "desafio5-lambda-isa-${AWS::AccountId}"), assim como o bucket s3.

A Stake foi executada com êxito.

No primeiro momento, ao executar um teste no lambda function, o arquivo .txt não foi gerado devido ao nome do bucket na função python que estava como "MyBucket".

Então foi feito uma alteração no código com a correção do nome do bucket correto com o nome lambda_function.py, essa alteração foi feita dentro do próprio lambda function na aba Code (Código):

anterior:

import boto3
import datetime

	def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = "${MyBucket}"
              

atual:

import boto3
import datetime

	def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = "desafio5-s3-isa-099597654193"
    
Ao fazer essa alteração, o arquivo .txt com o nome arquivo_s3_20251031_213457.txt com o conteúdo em string escrito "Meu primeiro arquivo gerado no lambda, incluso no S3 e automatizado pelo CloudFormation!!!", o arquivo foi criado com êxito no S3.

Segue em anexo o arquivo lambda_function.py, o template em YAML com o nome desafio5.yaml, o arquivo_s3_20251031_213457.txt e o arquivo lambda_function.zip compactado.

Segue também os prints na pasta images.


Segue abaixo os códigos em YAML, referente a stake:

```
AWSTemplateFormatVersion: "2010-09-09"
Description: Desafio DIO 5 - Tarefas Automatizadas com Lambda Function e S3

Resources:
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      Path: /
      Policies:
        - PolicyName: LambdaS3Execution
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action:
                  - logs:CreateLogGroup
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                Resource: "arn:aws:logs:*:*:*"
              - Effect: Allow
                Action:
                  - s3:PutObject
                  - s3:GetObject
                Resource: !Sub "arn:aws:s3:::${MyBucket}/*"

  MyBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub "desafio5-s3-isa-${AWS::AccountId}"

  MyLambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "desafio5-lambda-isa-${AWS::AccountId}"
      Handler: lambda_function.lambda_handler
      Runtime: python3.9
      Role: !GetAtt LambdaExecutionRole.Arn
      Timeout: 15
      Code:
        ZipFile: |
          import boto3
          import datetime

          def lambda_handler(event, context):
              s3 = boto3.client('s3')
              bucket_name = "${MyBucket}"
              file_name = f"arquivo_s3_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
              content = "Meu primeiro arquivo gerado no Lambda, incluso no S3 e automatizado pelo CloudFormation!!!"

              s3.put_object(Bucket=bucket_name, Key=file_name, Body=content)
              print(f"Arquivo {file_name} criado no bucket {bucket_name}")

              return {
                  "statusCode": 200,
                  "body": f"Arquivo {file_name} criado com sucesso no bucket {bucket_name}"
              }
```

 Segue código da função em python gerada em .py

```
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
```
