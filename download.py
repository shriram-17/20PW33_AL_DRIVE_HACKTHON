from google.cloud import storage
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, ProcessPoolExecutor

MAX_THREADS = 5 
MAX_PROCESSES = 5 

def download_file(blob_name, bucket_name, destination_dir):
    """Download a single file from a blob to the destination directory."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    destination_file_path = os.path.join(destination_dir, blob_name)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)

    try:
        blob.download_to_filename(destination_file_path)
    except Exception as e:
        print(f'Failed to download {blob_name}: {e}')

def download_files_from_bucket(bucket_name, source_prefix, destination_dir):
    """Downloads all blobs with a specific prefix from the bucket to the destination directory."""
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blobs = list(bucket.list_blobs(prefix=source_prefix))

    with ProcessPoolExecutor(max_workers=MAX_PROCESSES) as process_executor:
        futures = []
        for blob in blobs:
            futures.append(
                process_executor.submit(
                    download_file, blob.name, bucket_name, destination_dir
                )
            )

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f'Exception occurred: {e}')

def process_gcs_folders(gcs_folders, destination_dir):
    """Process each GCS folder URL and download its contents."""
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = []
        for gcs_url in gcs_folders:
            if gcs_url.startswith('gs://'):
                gcs_url = gcs_url[5:]  
                bucket_name, source_prefix = gcs_url.split('/', 1)
                futures.append(executor.submit(download_files_from_bucket, bucket_name, source_prefix, destination_dir))
            else:
                print(f'Invalid GCS URL: {gcs_url}')

        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f'Exception occurred: {e}')

def main():
    if len(sys.argv) < 2:
        print("Usage: python download.py <gcs_folder_1> <gcs_folder_2> ...")
        sys.exit(1)

    
    gcs_folders = sys.argv[1:]

  
    destination_dir = '/mnt/disks/local_disk_1'

    start_time = time.time()
    
    process_gcs_folders(gcs_folders, destination_dir)

    end_time = time.time()
    elapsed_time = end_time - start_time

    print(f"Total time taken: {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    main()