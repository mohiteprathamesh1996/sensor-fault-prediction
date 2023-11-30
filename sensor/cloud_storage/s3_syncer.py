import os

class S3Sync:
    def sync_folder_to_s3(self,folder,aws_bucket_url):
        """Uploading artifacts to AWS S3"""
        command = f"aws s3 sync {folder} {aws_bucket_url} "
        os.system(command)

    def sync_folder_from_s3(self,folder,aws_bucket_url):
        """Get data from AWS S3"""
        command = f"aws s3 sync  {aws_bucket_url} {folder} "
        os.system(command)

