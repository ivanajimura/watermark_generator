FROM ubuntu:22.04
WORKDIR     .
RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean
COPY requirements.txt .
RUN pip install -r ./requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]