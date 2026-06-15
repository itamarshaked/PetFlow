import os


class Config:
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME", "petflow")
    DB_USER = os.getenv("DB_USER", "petflow_admin")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "change-me-in-production")

    # Bandit: B105 / B106 possible findings:
    #JWT_SECRET_KEY = os.getenv("JWT_SECRET")

        #if not JWT_SECRET_KEY:
            #raise RuntimeError(
                #"JWT_SECRET environment variable is not configured."
            #)

    AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")
    S3_BUCKET = os.getenv("S3_BUCKET")
