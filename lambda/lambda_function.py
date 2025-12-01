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
