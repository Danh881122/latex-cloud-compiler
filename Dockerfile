FROM texlive/texlive:latest

# Cài Python & pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Thư mục làm việc
WORKDIR /app

# Copy mã nguồn
COPY . .

# Cài Flask (cho phép ghi đè hệ thống)
RUN pip install --break-system-packages -r requirements.txt

# Chạy Flask server
CMD ["python3", "server.py"]
