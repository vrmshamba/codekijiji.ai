#!/bin/bash

# This script downloads the xtts_model.pth file from the S3 bucket

# Set the AWS credentials (these will be replaced with the actual credentials)
export AWS_ACCESS_KEY_ID=AKIARL6WUSPDXEBZBCWQ
export AWS_SECRET_ACCESS_KEY=${codekijijiaiforredepolyment}
export AWS_DEFAULT_REGION=us-east-1

# The S3 bucket URL
S3_BUCKET_URL="s3://social-behav-tool-bucket/xtts_model.pth"

# The local path to save the model file
LOCAL_MODEL_PATH="TTS/tts/models/xtts_model.pth"

# Download the model file from S3
aws s3 cp $S3_BUCKET_URL $LOCAL_MODEL_PATH

# Check if the download was successful
if [ -f "$LOCAL_MODEL_PATH" ]; then
    echo "Model downloaded successfully."
else
    echo "Failed to download the model."
fi
