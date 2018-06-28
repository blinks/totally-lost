FROM python:2
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["lost.py"]
EXPOSE 5000
