FROM python:latest

RUN mkdir /dashboard
WORKDIR /dashboard
ADD ./dashboard /dashboard/
RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["python", "/dashboard/app.py"]