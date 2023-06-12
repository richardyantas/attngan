# sudo apt update && apt upgrade -y
# sudo apt install python3-pip

# https://stackoverflow.com/questions/63093034/permission-denied-while-starting-a-flask-app-at-port-80-in-aws-ec2-instance
# port 80  for http -> aws 
# use gunicorn and ngnix

# create ECR -> obs: is important to have installed aws-cli

aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/c0b5t4d6
docker build -t flask-app -f dockerfile.test .
docker tag flask-app:latest public.ecr.aws/c0b5t4d6/flask-app:latest
docker push public.ecr.aws/c0b5t4d6/flask-app:latest

# errors
# when create task definition
# User: arn:aws:iam::887811865515:user/rick is not authorized to perform: iam:CreateRole on resource: arn:aws:iam::887811865515:role/ecsTaskExecutionRole because no identity-based policy allows the iam:CreateRole action

aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/c0b5t4d6
docker build -t flask-gan-app .
docker tag flask-gan-app:latest public.ecr.aws/c0b5t4d6/flask-gan-app:latest
docker push public.ecr.aws/c0b5t4d6/flask-gan-app:latest


# docker tag flask-gan-app:latest public.ecr.aws/c0b5t4d6/flask-gan-app:latest
# docker push public.ecr.aws/c0b5t4d6/flask-gan-app:latest

# docker run -rm -v 5000:5000 flask-gan-app