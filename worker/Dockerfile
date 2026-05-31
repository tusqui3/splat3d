FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# INTEGRATION POINT: Install COLMAP + nerfstudio/3DGS here
# RUN apt-get install -y colmap
# RUN pip install nerfstudio

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "worker.py"]
