FROM python:3.11

WORKDIR /app/

COPY requirements.txt /app/

# Make sure to create a .env file whenever this is ran
COPY lib/* /app/

# Leave this here until I have the build completed
RUN ls /app

RUN pip install wheel

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "dockerops.py"]
