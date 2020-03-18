FROM python:3.7.7-slim-buster
COPY . /

# ## install dependencies
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends gcc netcat-openbsd


# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app


ENTRYPOINT [ "python" ]

CMD [ "main.py" ]