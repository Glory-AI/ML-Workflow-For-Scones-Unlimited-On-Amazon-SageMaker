import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))  # Debugging line
    
    try:
        key = event['s3_key']  # Corrected key for S3 object
        bucket = event['s3_bucket']  # Corrected key for S3 bucket

        # Download the data from S3 to /tmp/image.png
        s3.download_file(bucket, key, "/tmp/image.png")

        # Read the data from the file
        with open("/tmp/image.png", "rb") as f:
            image_data = base64.b64encode(f.read())

        # Pass the data back to the Step Function
        return {
            'statusCode': 200,
            'body': {
                "image_data": image_data.decode('utf-8'),  # Decode to string for JSON compatibility
                "s3_bucket": bucket,
                "s3_key": key,
                "inferences": []
            }
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }


import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))  # Debugging line
    
    try:
        key = event['s3_key']  # Corrected key for S3 object
        bucket = event['s3_bucket']  # Corrected key for S3 bucket

        # Download the data from S3 to /tmp/image.png
        s3.download_file(bucket, key, "/tmp/image.png")

        # Read the data from the file
        with open("/tmp/image.png", "rb") as f:
            image_data = base64.b64encode(f.read())

        # Pass the data back to the Step Function
        return {
            'statusCode': 200,
            'body': {
                "image_data": image_data.decode('utf-8'),  # Decode to string for JSON compatibility
                "s3_bucket": bucket,
                "s3_key": key,
                "inferences": []
            }
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

import json

THRESHOLD = 0.93  # Set the threshold for confidence

def lambda_handler(event, context):
    
    # Grab the inferences from the event
    inferences = event['inferences']  
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = any(value > THRESHOLD for value in inferences)  # Check if any inference meets the threshold
    
    # If our threshold is met, pass our data back out of the Step Function,
    # else, end the Step Function with an error
    if meets_threshold:
        return {
            'statusCode': 200,
            'body': json.dumps(event)  # Return the original event if the threshold is met
        }
    else:
        raise Exception("THRESHOLD_CONFIDENCE_NOT_MET")  # Raise an exception if the threshold is not met

