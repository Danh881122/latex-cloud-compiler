FROM texlive/texlive:latest
RUN apt-get update && apt-get install -y python3 python3-pip
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python3", "server.py"]
