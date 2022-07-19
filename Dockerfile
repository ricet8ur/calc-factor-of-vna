FROM python:3.8-slim-buster
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8501
COPY . /app
ENTRYPOINT ["streamlit", "run"]
CMD ["./source/main.py", "--browser.serverAddress=0.0.0.0", "--browser.gatherUsageStats=false", "--server.maxUploadSize = 20"]
# docker build -t calc-q-factor:latest .
# docker run -p 8501:8501 calc-q-factor:latest
