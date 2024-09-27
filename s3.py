import os
import boto3
import time
from botocore.exceptions import NoCredentialsError, ClientError

def download_progress(bytes_transferred, total_bytes, start_time):
    percentage = (bytes_transferred / total_bytes) * 100
    mb_downloaded = bytes_transferred / (1024 * 1024)  # Convert to MB
    total_mb = total_bytes / (1024 * 1024)  # Convert to MB

    elapsed_time = time.time() - start_time
    speed = mb_downloaded / elapsed_time if elapsed_time > 0 else 0  # MB/s
    time_remaining = (total_mb - mb_downloaded) / speed if speed > 0 else float('inf')

    print(f"\rDownloaded {mb_downloaded:.2f} MB of {total_mb:.2f} MB ({percentage:.2f}%), "
          f"Speed: {speed:.2f} MB/s, Time remaining: {time_remaining:.2f} seconds", end='')


def download_from_s3(bucket_name, s3_folder, local_dir):
    s3 = boto3.client('s3')

    if not os.path.exists(local_dir):
        os.makedirs(local_dir)

    try:
        result = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_folder)

        if 'Contents' in result:
            for obj in result['Contents']:
                s3_file_key = obj['Key']

                relative_path = os.path.relpath(s3_file_key, s3_folder)

                local_file_path = os.path.join(local_dir, relative_path)

                local_file_dir = os.path.dirname(local_file_path)
                if not os.path.exists(local_file_dir):
                    os.makedirs(local_file_dir)

                print(f"Downloading {s3_file_key} to {local_file_path}")

                start_time = time.time()

                file_size = obj['Size']

                s3.download_file(
                    bucket_name,
                    s3_file_key,
                    local_file_path,
                    Callback=lambda bytes_transferred: download_progress(bytes_transferred, file_size, start_time)
                )

                print("\nDownload completed!")

        else:
            print("No files found in the specified S3 folder.")

    except NoCredentialsError:
        print("Credentials not available.")
    except ClientError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    bucket_name = ""
    s3_folder = "UserSounds/.../"
    local_dir = r"C:\Users\username\Music\.../"

    download_from_s3(bucket_name, s3_folder, local_dir)
