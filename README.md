## ML Workflow For Scones Unlimited On Amazon SageMaker


### Project overview
This repository contains an end-to-end machine learning pipeline that trains, deploys, and serves an image classification model which distinguishes bicycles from motorcycles. The solution demonstrates model training with SageMaker, serverless inference using AWS Lambda, and orchestration using AWS Step Functions. The pipeline includes data capture, inference monitoring, and post-processing.
 

### Architecture

* S3 — Storage for training data, artifacts, and captured inference data.

* SageMaker — Model training and hosted inference endpoint (with Data Capture enabled).

* Lambda (3 functions)

   Preprocess Image: Download image from S3, encode to base64 and return payload.

   Invoke Model: Decode base64, call SageMaker endpoint, return inference result.

   Postprocess Results: Parse returned inferences, check threshold, return final decision.

* Step Functions — Orchestrates Lambda invocations: Preprocess Image → Invoke Model → Postprocess Results.

<img width="1366" height="596" alt="Screenshot 2025-10-03 222824" src="https://github.com/user-attachments/assets/a68c97fa-111e-4f7b-a4a1-1b2edc678a4c" />

### What I built

* A image classification model in SageMaker.

* Deployment of the model to a SageMaker endpoint.

* A serverless inference pipeline with three Lambda functions and an orchestrating Step Function.

* Data capture from SageMaker endpoints into S3 for offline analysis and model monitoring.

* Scripts and notebooks to download and parse captured data and to analyze inference outputs.


### Key concepts & data notes

* Gzip / .tar.gz: The project includes handling gzipped dataset archives (lossless compression). Use rb mode and pickle to read bytes from extracted files.

* Pickle: Serialization used to store dataset metadata. Use pickle.load(..., encoding='bytes') if necessary.

* CIFAR-like format (example): A single row represents a 32 x 32 x 3 image (3072 integers) plus a label integer (total 3073 entries).

* SageMaker Data Capture: When enabled, SageMaker writes request/response logs to an S3 path under data_capture/. Download them for analysis and monitoring.


### Troubleshooting & common errors

#### *  KeyError: 'image_data'

* Cause: mismatch in the JSON shape passed between Lambdas / Step Function.

* Fix: standardize outputs and use Payload.$ + ResultPath/OutputPath carefully in your state machine; in Lambda handlers, accept both direct and nested inputs (e.g., handle event["body"] and event["image_data"]).

#### * TypeError: string indices must be integers

* Cause: JSON strings not parsed into Python dicts.

* Fix: json.loads(...) where necessary; read .jsonl line by line using jsonlines.

####* SageMaker ModuleNotFoundError on endpoint/unpickle errors

* Cause: model pickled/saved with different library versions than endpoint environment.

* Fix: ensure SageMaker container versions match the training environment or re-export using torch.jit or save model weights instead and rebuild model class.

#### * Lambda “module import” errors (sagemaker not found)

* Ensure any non-standard library used by Lambda is included in a Lambda Layer or package the dependencies into the deployment package. For SageMaker SDK inside Lambda, prefer calling boto3 (sagemaker-runtime) or include SageMaker in a layer.


