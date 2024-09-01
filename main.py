import os
import time
import threading
from datetime import datetime
from google.cloud import storage
import random
import string 

N = 12
RATE_LIMIT_STATUS_CODE = [429,408]


def local_file_gen():
    file = "myfile"
    check_file = os.path.isfile(file)
    if check_file:
        print(f"{file} already exist, no need to change")
    else:
        print(f"file doesn't exist, create file {file}")
        f = open(file, "a")
        f.write("test ramp up")
        f.close()
        

def upload_blob(bucket, read_write_ratio):
    local_file_gen()

    while True:
        now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        prefix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
        blob_name = f"{prefix}-{now}"

        try:
            blob = bucket.blob(blob_name)
            blob.upload_from_filename('myfile')
            # print(f"Thread: {threading.get_native_id()} - Uploaded: {blob_name}")
            for _ in range(read_write_ratio):
                blob.reload()

            blob.delete()
            # print(f"Thread: {threading.get_native_id()} - Deleted: {blob_name}")
            time.sleep(0.1)

        except Exception as e:
            if (hasattr(e, 'code') and e.code == RATE_LIMIT_STATUS_CODE) or \
               (hasattr(e, 'response') and hasattr(e.response, 'status_code') and e.response.status_code in RATE_LIMIT_STATUS_CODE):
                    print(f"Rate limit hit")
                    return
            else:
                print(f"Error {e} Exiting thread {threading.get_native_id()}.")
                return

def main(bucket_name, thread_count):
    bucket_name = bucket_name
    thread_count = int(thread_count)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    for _ in range(thread_count):
        thread = threading.Thread(target=upload_blob, args=[bucket, read_write_ratio,])
        thread.start()
    print("all threads start")


if __name__=="__main__":
    thread_count = os.getenv('THREAD_COUNT',5)
    read_write_ratio = os.getenv('READ_WRITE_RATIO',2)
    bucket_name = os.getenv('BUCKET_NAME',None)
    # check if bucket name is null
    if bucket_name is not None:
        main(bucket_name, thread_count)
    else:
        print("Bucket name is null")
        exit(1)

#