## ML Workflow For Scones Unlimited On Amazon SageMaker


#### Project overview
This repository contains an end-to-end machine learning pipeline that trains, deploys, and serves an image classification model which distinguishes bicycles from motorcycles. The solution demonstrates model training with SageMaker, serverless inference using AWS Lambda, and orchestration using AWS Step Functions. The pipeline includes data capture, inference monitoring, and post-processing.
 

#### Architecture

* S3 — Storage for training data, artifacts, and captured inference data.

* SageMaker — Model training and hosted inference endpoint (with Data Capture enabled).

* Lambda (3 functions)

   Preprocess Image: Download image from S3, encode to base64 and return payload.

   Invoke Model: Decode base64, call SageMaker endpoint, return inference result.

   Postprocess Results: Parse returned inferences, check threshold, return final decision.

* Step Functions — Orchestrates Lambda invocations: Preprocess Image → Invoke Model → Postprocess Results.


#### What I built

* A image classification model in SageMaker.

* Deployment of the model to a SageMaker endpoint.

* A serverless inference pipeline with three Lambda functions and an orchestrating Step Function.

* Data capture from SageMaker endpoints into S3 for offline analysis and model monitoring.

* Scripts and notebooks to download and parse captured data and to analyze inference outputs.


#### Key concepts & data notes

* Gzip / .tar.gz: The project includes handling gzipped dataset archives (lossless compression). Use rb mode and pickle to read bytes from extracted files.

* Pickle: Serialization used to store dataset metadata. Use pickle.load(..., encoding='bytes') if necessary.

* CIFAR-like format (example): A single row represents a 32 x 32 x 3 image (3072 integers) plus a label integer (total 3073 entries).

* SageMaker Data Capture: When enabled, SageMaker writes request/response logs to an S3 path under data_capture/. Download them for analysis and monitoring.

#### Project structure
SconesUnlimited/
│
├── data/

│   ├── cifar-100-python/        

│
├── notebooks/

│   ├── training_and_endpoint.ipynb

├── lambdas/

│   ├── preprocess_image/

│   │   └── lambda_function.py

│   ├── invoke_model/

│   │   └── lambda_function.py

│   └── postprocess_results/

│       └── lambda_function.py

│

├── step_function/

│   └── state_machine.json       
│

├── captured_data/               

├── src/


│   ├── model.py                  

│   ├── train.py                 

│   ├── predict.py               

│   └── data.py                  
│
├── tests/                       

├── README.md

└── requirements.txt



