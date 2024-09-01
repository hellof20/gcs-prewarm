# gcs-prewarm

## Build your own image
```
docker build -t hellof20/gcs-prewarm:2024090104 .
```

## Run with Cloud Run Job
- BUCKET_NAME: 需要预热的存储桶名称
- READ_WRITE_RATIO： 读写比例是多少
- region：Cloud Run Job部署的区域，和存储桶所在区域一致
- task-timeout：预热多少秒
- tasks：Job的数量，参考GCS的QPS和task数量对照表
```
gcloud run jobs deploy gcs-prewarm \
--image=hellof20/gcs-prewarm:2024090104 \
--update-env-vars BUCKET_NAME=pwm-gcs-hk,READ_WRITE_RATIO=1 \
--tasks 50 \
--region asia-east2 \
--execute-now \
--task-timeout 1800
```

## Reference
