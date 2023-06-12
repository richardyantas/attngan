FROM python:3.9.16-buster

RUN pip install --upgrade pip
RUN pip install torch==1.9.0+cpu torchvision==0.10.0+cpu -f https://download.pytorch.org/whl/torch_stable.html

# RUN pip install --upgrade pip

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY prod.in /usr/src/app/
RUN pip install --no-cache-dir -r prod.in
COPY . /usr/src/app

ENV GPU False
ENV EXPORT_MODEL True

# EXPOSE 8080
EXPOSE 5000

CMD ["python", "main.py"]