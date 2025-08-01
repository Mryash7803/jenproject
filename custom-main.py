# custom_main.py
import boto3

def analyze_with_custom_model(project_version_arn, bucket_name, photo_name, access_key, secret_key):
    """
    Analyzes an image stored in an S3 bucket using your custom Amazon Rekognition model.

    :param project_version_arn: The ARN of your trained model.
    :param bucket_name: The name of the S3 bucket where the image is stored.
    :param photo_name: The name of the image file to analyze.
    :param access_key: Your AWS Access Key ID.
    :param secret_key: Your AWS Secret Access Key.
    """
    try:
        # This line creates a client to interact with the Amazon Rekognition service.
        # It correctly uses the access keys passed into the function.
        rekognition_client = boto3.client(
            'rekognition',
            region_name='us-east-1',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

        print(f"Analyzing {photo_name} with custom model {project_version_arn}...")

        # This is the key difference: we call 'detect_custom_labels'.
        # We provide the ARN of our trained model so Rekognition knows which one to use.
        response = rekognition_client.detect_custom_labels(
            ProjectVersionArn=project_version_arn,
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': photo_name,
                }
            },
            MinConfidence=10  # Lowered confidence to 10 for debugging.
        )

        # The response contains a list of 'CustomLabels'.
        labels = response['CustomLabels']

        print(f"Found {len(labels)} custom labels:")

        if not labels:
            print("No custom labels detected, even with a low confidence threshold.")
            return

        # We loop through each label found and print its name and confidence.
        for label in labels:
            label_name = label['Name']
            confidence = label['Confidence']
            print(f"- Label: {label_name}, Confidence: {confidence:.2f}%")

    except Exception as e:
        # This error handling is very important. It can tell you if your model isn't running.
        print(f"An error occurred: {e}")
        print("\nPlease check the following:")
        print(f"- Is your model '{project_version_arn}' currently running? (Status should be 'Running').")
        print(f"- Does the bucket '{bucket_name}' exist?")
        print(f"- Does the file '{photo_name}' exist in the bucket?")
        print("- Are your AWS credentials correct?")

# --- HOW TO RUN THIS SCRIPT ---
if __name__ == '__main__':
    # --- YOUR INFORMATION IS HERE ---
    
    # 1. Your AWS Access Key ID
    my_access_key = 'AKIATL4IQCMNCZ3PFHFE'
    
    # 2. Your AWS Secret Access Key
    my_secret_key = 'wEh/BGEqAzswvnxMUfbEETkLW6EIjQzUg3zmiL3/'

    # 3. The ARN of your trained model.
    my_model_arn = 'arn:aws:rekognition:us-east-1:231677629210:project/firsttime/version/firsttime.2025-08-01T18.24.43/1754052884338'

    # 4. The name of your S3 bucket.
    my_bucket = 'mryash7803'

    # 5. The name of a NEW image you want to test.
    #    Make sure you have uploaded 'thor.jpeg' to your S3 bucket.
    my_photo = 'dead.jpeg'

    # --- END OF YOUR INFORMATION ---


    # Before running, make sure your model status is "Running" in the AWS Console.
    if 'PASTE_YOUR' in my_access_key or 'PASTE_YOUR' in my_secret_key:
        print("Please open the script and paste your AWS Access Key and Secret Key into the variables.")
    else:
        analyze_with_custom_model(my_model_arn, my_bucket, my_photo, my_access_key, my_secret_key)

