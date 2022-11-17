FROM python:latest

RUN mkdir /dashboard
ADD ./dashboard /dashboard/
RUN pip install -r /dashboard/requirements.txt

EXPOSE 5001
CMD ["python", "/dashboard/app.py"]