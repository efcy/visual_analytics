FROM ubuntu:22.04

# show the stdout and stderr streams right in the command line instead of getting buffered.
ENV PYTHONUNBUFFERED=1

RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(. /etc/os-release && echo $UBUNTU_CODENAME)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg

RUN apt-get update && apt-get -y --no-install-recommends install \
    wget \
    git \
    python3 \
    python3-pip \
    nano \
    python-is-python3 \
    python3-dev \
    postgresql-client-16

RUN mkdir /django
WORKDIR /django
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]