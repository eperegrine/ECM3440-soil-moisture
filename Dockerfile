FROM python:latest

RUN mkdir /dashboard
WORKDIR /dashboard
ADD ./dashboard /dashboard/
RUN pip install -r requirements.txt

EXPOSE 5001
CMD ["python", "/dashboard/app.py"]