FROM python:3.9.16

WORKDIR /usr/src/application
#copy requirements.txt in container
COPY general_requirements.txt ./
#install requirements in container
RUN pip install --no-cache-dir -r general_requirements.txt
#copy contents entire contents in WORKDIR folder
COPY . . 
#this cmd will be overwritten from docker-compose.yaml file command
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]