
# Scopic Challenge

This repo is an extension of attgan paper implementation that can be found in [attan](https://github.com/taoxugit/AttnGAN) 

# Task1 y Task2

### Table of contents:

- [Scopic Challenge](#scopic-challenge)
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
    - [5.- Tools and frameworks that could simplify the deployment process.](#5--tools-and-frameworks-that-could-simplify-the-deployment-process)


### 1.- Environment setup

We use conda to create our environment

    conda env create -f environment.yml 
    conda activate attngan


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

The paper "AttnGAN: Fine-Grained Text to Image Generation with Attentional Generative Adversarial Networks" introduces a method for generating detailed and realistic images from textual descriptions using a novel attentional generative adversarial network (GAN) framework. The model consists of two main components: a text encoder and an image generator.

The text encoder encodes the input textual description into a semantic vector representation, capturing the salient information. The image generator then uses this vector representation to generate the corresponding image.

One key aspect of AttnGAN is the use of attention mechanisms. The authors introduce a novel Attention Generative Network (AttnGAN) that employs attention at both the global and local levels. The global attention module attends to the entire image, ensuring that the generated image aligns with the overall content of the textual description. The local attention module focuses on specific regions of the image, allowing for the generation of fine-grained details.

To train the model, the authors propose a two-stage process. In the first stage, a conditional GAN is trained to generate images at a coarse level of detail. In the second stage, the model is fine-tuned using a ranking loss that compares the generated images with real images based on their textual descriptions. This ranking loss helps the model capture the nuances and details specified in the textual input.

The experiments conducted by the authors demonstrate that AttnGAN outperforms existing methods in terms of generating visually appealing and detailed images based on textual descriptions. The attention mechanisms employed in AttnGAN enable the model to focus on the most relevant parts of the image, resulting in improved image quality and fine-grained details.

### 2.- Arquitecture

The arquitecture proposed is to run the model on the server side for the following reasons: to manage computational resources such as RAM memory to load the model that in generative models it occupy 
large amount of memory. In this paper the pretrainermodels `text_encoder200.pth` and `image_encoder200.pth` accupy 8.M and 87M respectively, these pretrained models are used for training a general AttnGAN using attention mechanism obtaining a model `bird_AttnGAN2.pth` the use 28M of memory.

### 3.- Scaling 

Ths Scaling of this project can be achieved through various approaches. Here are some strategies for scaling the solution:

- Distributed Training: To handle larger datasets and accelerate training, you can employ distributed training techniques or using technologies such as `Ray`. This involves using multiple machines or GPUs to parallelize the training process. Techniques like data parallelism or model parallelism can be applied to distribute the workload and speed up training.

- Model Optimization: The AttnGAN model can be optimized to make it more efficient and scalable. This could involve reducing the model's complexity, exploring more efficient network architectures, or applying techniques like model pruning, quantization, or knowledge distillation to reduce the model's size and computational requirements.

- Cloud Computing: Leveraging cloud computing services can facilitate scaling the solution. Cloud platforms like Amazon Web Services (AWS), Google Cloud Platform (GCP), or Microsoft Azure provide powerful infrastructure and GPU instances that can handle intensive computations required for training and inference. We can leverage their scalable resources to distribute the workload or deploy multiple instances of the model.

- Batch Processing: Instead of processing images and text descriptions one at a time, We can implement batch processing techniques. This involves grouping multiple inputs together and processing them simultaneously, taking advantage of parallelism and reducing overhead. Batch processing can significantly improve efficiency when handling large volumes of data.

- Caching and Precomputing: If there are computationally expensive or frequently repeated operations in the pipeline, you can cache or precompute the results to avoid redundant calculations. This can save computational resources and speed up the overall process.

- Incremental Learning: Instead of retraining the entire model from scratch when new data becomes available, you can adopt incremental learning techniques. This allows us to update the model using new data while retaining knowledge from the previous training, thus minimizing training time and computational resources.

- Load Balancing and Auto-Scaling: When deploying the model in a server-based architecture, load balancing techniques can be employed to distribute incoming requests evenly across multiple servers or instances. Auto-scaling mechanisms can automatically adjust the number of server instances based on demand, ensuring optimal resource allocation during peak loads.

By implementing these scaling strategies, we can handle larger datasets, improve training and inference efficiency, and accommodate increased user demand or workloads. The specific approach to scaling will depend on the available resources, infrastructure, and requirements of the application.


### 4.- System design on cloud

Some of the  host machine specifications on cloud are the following:

- The use of S3 to store images generated to use later on the app
- The use of services such as ECR (to register docker images repositories )
- The use of EC2 `t2.micro` automaticly by ECS in the `cluster` creation.
- The use of task that 


### 5.- Tools and frameworks that could simplify the deployment process.

- Aws command line 
- Terraform 
- Docker
- Jenkins

