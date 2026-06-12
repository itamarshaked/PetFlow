import uuid

import boto3
from flask import current_app


def upload_pet_image(file, pet_id: str) -> str:
    s3_client = boto3.client(
        "s3",
        region_name=current_app.config["AWS_REGION"]
    )

    bucket = current_app.config["S3_BUCKET"]

    file_ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else "jpg"
    object_key = f"pets/{pet_id}/{uuid.uuid4()}.{file_ext}"

    s3_client.upload_fileobj(
        file,
        bucket,
        object_key,
        ExtraArgs={"ContentType": file.content_type}
    )

    return f"s3://{bucket}/{object_key}"
