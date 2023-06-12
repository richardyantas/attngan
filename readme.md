
# Task1 y Task2

### Table of contents:

- [Task1 y Task2](#task1-y-task2)
    - [Table of contents:](#table-of-contents)
    - [1.- Environment setup](#1--environment-setup)
    - [2.- Steps to run the training](#2--steps-to-run-the-training)
    - [3.- Sample input/output after your training](#3--sample-inputoutput-after-your-training)
    - [4.- Dataset](#4--dataset)
    - [5.- Testing](#5--testing)
    - [6.- Deploying](#6--deploying)
    - [7.- Results](#7--results)
- [Task3](#task3)
    - [1.- Description paper](#1--description-paper)
    - [2.- Arquitecture](#2--arquitecture)
    - [3.- Scaling](#3--scaling)
    - [4.- System design on cloud](#4--system-design-on-cloud)
    - [5.-](#5-)


### 1.- Environment setup

We use conda to create our environment

    conda env create -f environment.yml 
    conda activate attngan
    pip install -r requirements.txt


### 2.- Steps to run the training

All config files `*.yml` required for the traning is located in `trainer/cfg/`
- Get into trainer directory `cd /trainer`
- Pre-train DAMSM models:

  - For bird dataset: `python pretrain_DAMSM.py --cfg cfg/DAMSM/bird.yml --gpu 0`


- Train AttnGAN models:

  - For bird dataset: `python main.py --cfg cfg/bird_attn2.yml --gpu 0`
  - `*.yml` files are example configuration files for training/evaluation our models.


### 3.- Sample input/output after your training

Input: A caption that describe that image that would be created
Output: An image

### 4.- Dataset

- Download our preprocessed metadata for  [birds](https://drive.google.com/open?id=1O_LtUP9sch09QH3s_EBAgLEctBQ5JBSJ) and save them to data/
- Download the birds image data. Extract them to data/birds/

### 5.- Testing

For that, a dockerfile is create in order to build an image.

There is a three step process running the application and generating bird images.
   ```
    cd /app
   ```
1. Create the container (optionally choose the cpu or gpu dockerfile: 
   ```
   docker build -t "flask-gan-app" -f dockerfile.cpu .
   ``` 
2. Run the container (replace the key's with the appropriate blob storage location as well as App Insights Key): 
    ```
    docker run -it -e BUCKET_NAME=scopicbucket -e ACCESS_KEY_ID=ACCESS_KEY_ID -e ACCESS_SECRET_KEY=ACCESS_SECRET_KEY -p 5678:8080 attngan
    ```
3. Call the API: 
   ```
   curl -H "Content-Type: application/json" -X POST -d '{"caption":"the bird has a yellow crown and a black eyering that is round"}' http://locahost:5678/api/v1.0/bird

### 6.- Deploying

    aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin

    docker tag flask-gan-app:latest public.ecr.aws/c0b5t4d6/flask-gan-app:latest

    docker push public.ecr.aws/c0b5t4d6/flask-gan-app:latest

### 7.- Results

- Complexity of the model
- Model evaluation metric 
- The trained model
- Code files modification
- A screenshot of the output 


# Task3


### 1.- Description paper



### 2.- Arquitecture
### 3.- Scaling 
### 4.- System design on cloud
### 5.- 

