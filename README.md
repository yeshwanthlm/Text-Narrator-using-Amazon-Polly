# Text narrator using Amazon Polly

### Project Overview:
In this project, we will be developing a text narrator using Amazon Polly. A piece of text (book, article, newsletter) will be uploaded in an Amazon S3 bucket and converted to speech. The voice, pitch and speed parmeters can be adjusted.

### Video Tutorial:
<img width="1920" height="1080" alt="Amazon Polly (1)" src="https://github.com/user-attachments/assets/37474fa9-7b59-45e4-b6b6-0e15ea2c9e01" />

Video Link:

### Steps to be Performed:
In this video, we'll be going through the following steps.
1. Exploring Amazon Polly
2. Creating an IAM role: 
```sh
RoleName: PollyTranslationRole
Policies:
AmazonPollyFullAccess
AmazonS3FullAccess
AWSLambdaBasicExecutionRole
```
3. Creating an Source and Destiation S3 Buckets:
```sh
Source S3 Bucket Name: twy-polly-text-files-storage-bucket
Destiation S3 Bucket Name: twy-polly-audio-files-storage-bucket
```

4. Writing Lambda function code:
```python
import boto3
import time
import json

polly = boto3.client("polly")
s3 = boto3.client("s3")

def lambda_handler(event, context):  # ✅ This name is required
    try:
        # Get S3 file details from trigger event
        record = event["Records"][0]["s3"]
        source_bucket = record["bucket"]["name"]
        file_key = record["object"]["key"]

        # Read text file from twy-polly-text-files-storage-bucket
        obj = s3.get_object(Bucket="twy-polly-text-files-storage-bucket", Key=file_key)
        text = obj["Body"].read().decode("utf-8")

        # Convert text → speech
        polly_response = polly.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId="Joanna"
        )

        if "AudioStream" not in polly_response:
            raise Exception("Polly did not return audio data")

        # Read audio stream
        audio_bytes = polly_response["AudioStream"].read()

        # Destination audio file name
        audio_key = f"speech-{int(time.time()*1000)}.mp3"

        # Upload audio to twy-polly-audio-files-storage-bucket
        s3.put_object(
            Bucket="twy-polly-audio-files-storage-bucket",
            Key=audio_key,
            Body=audio_bytes,
            ContentType="audio/mpeg",
            ContentLength=len(audio_bytes)
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Conversion successful",
                "source_file": file_key,
                "audio_file": audio_key
            })
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

```

6. Checking the output of Amazon Polly

### Services Used: 
1. Amazon Polly: Converts text to life like speech with customizable features.
2. AWS Management Console: Manages accounts and configures Amazon Polly.
3. AWS IAM: Ensures secure access by managing user permissions.

### Estimated Time & Cost:
* This project is estimated to take about 20-30 minutes
* Cost: Free (When using the AWS Free Tier)

Congratulations! You have successfully completed the project of text to speech translation using Amazon Polly, Lambda and S3 bucket.

### What’s Next? Here is an idea that you can try out to make the project more interesting:
Create a website that will take the user input of text to be converted to speech, which will be passed to Lambda function for processing and the results are shown back on the website by providing the audio file.

Good luck exploring.
