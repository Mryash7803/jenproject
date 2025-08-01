import boto3
import os

s3_client = boto3.client('s3')
polly_client = boto3.client('polly')

def lambda_handler(event, context):
    # Get the bucket and key (file name) from the S3 event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # Ensure the file is a .txt file and is in the 'text/' folder
    if not key.startswith('text/') or not key.endswith('.txt'):
        print(f"File {key} is not a valid text file in the 'text/' folder. Exiting.")
        return

    print(f"Processing file: {key} from bucket: {bucket_name}")

    try:
        # Get the text content from the S3 object
        response = s3_client.get_object(Bucket=bucket_name, Key=key)
        text_content = response['Body'].read().decode('utf-8')

        # Synthesize speech using Amazon Polly
        polly_response = polly_client.synthesize_speech(
            Text=text_content,
            OutputFormat='mp3',
            VoiceId='Joanna'  # You can choose other voices like 'Matthew', 'Salli', etc.
        )

        # Define the output file name and path in the 'audio/' folder
        audio_key = 'audio/' + os.path.splitext(os.path.basename(key))[0] + '.mp3'

        # Save the audio stream to the S3 bucket in the 'audio' folder
        s3_client.put_object(
            Bucket=bucket_name,
            Key=audio_key,
            Body=polly_response['AudioStream'].read(),
            ContentType='audio/mpeg'
        )

        print(f"Successfully converted {key} to {audio_key}")
        return {
            'statusCode': 200,
            'body': 'File converted successfully!'
        }

    except Exception as e:
        print(f"Error processing file: {e}")
        raise e