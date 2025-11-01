FROM debian:bookworm-slim

# Cài LaTeX + Python
RUN apt-get update \
 && apt-get install -y texlive-full python3 python3-pip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# PEP 668: cần --break-system-packages trong container Debian
RUN pip install --break-system-packages -r requirements.txt

CMD ["python3", "server.py"]
