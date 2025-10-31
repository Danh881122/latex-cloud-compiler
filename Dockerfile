# Base image có sẵn đầy đủ LaTeX + Python
FROM texlive/texlive:latest

# Cài Python & pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Copy mã nguồn
WORKDIR /app
COPY . .

# Cài Flask
RUN pip install -r requirements.txt

# Chạy server
CMD ["python3", "server.py"]
