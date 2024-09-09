# gcs-prewarm
The underlying mechanism followed the official [Documentation](https://cloud.google.com/storage/docs/request-rate?hl=zh-cn) on GCS QPS ramp-up specified the initial IO Limit as: Read 5000/s，Write 1000/s. For any QPS rate expected above the number, a ramp up is needed to avoid errors (429, 408, 5xx) that implied a cooling period for bucket scalability.
The tool developed helps to ramp up, allowing any bucket to be ramped up to desired write and read QPS at any defined read-write ratio.

## Run with Cloud Run Job
- BUCKET_NAME: 需要预热的存储桶名称
- READ_WRITE_RATIO： 读写比例是多少
- region：Cloud Run Job部署的区域，和存储桶所在区域一致
- task-timeout：预热多少秒
- tasks：Job的数量，参考GCS的QPS和task数量对照表
```
export BUCKET_NAME=your_bucket_name
export READ_WRITE_RATIO=1
export REGION=asia-east2
export TASK_NUM=100

gcloud run jobs deploy gcs-prewarm \
--image=hellof20/gcs-prewarm:2024090901 \
--update-env-vars BUCKET_NAME=$BUCKET_NAME,READ_WRITE_RATIO=$READ_WRITE_RATIO \
--tasks $TASK_NUM \
--region $REGION \
--execute-now \
--task-timeout 1800 \
--max-retries=0
```

## Reference
不同task数量和读写比例的情况下可以达到的性能如下

<img width="357" alt="image" src="https://github.com/user-attachments/assets/2fa91d07-15cb-4809-86b3-960345793862">

## Build your own image (Optional)
```
docker build -t hellof20/gcs-prewarm:2024090901 .
```
