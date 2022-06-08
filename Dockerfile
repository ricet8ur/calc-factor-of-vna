FROM python:latest
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8501
COPY . /app
ENTRYPOINT ["streamlit", "run"]
CMD ["./source/main.py"]
# docker build -t calc-q-factor:latest .
# docker run -p 8501:8501 calc-q-factor:latest