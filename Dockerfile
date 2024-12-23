FROM python:3.11.6-slim-bullseye as builder

ENV TZ=Europe/Paris
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY . .

RUN <<EOT
apt update
apt install -y build-essential curl apt-utils python3-dev
python3 -m venv venv
export PATH=/app/venv/bin:$PATH
pip install pip -U
pip install --no-cache-dir -r requirements.txt
apt remove -y build-essential
apt autoremove
apt autoclean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
EOT

FROM python:3.11.6-alpine
COPY --from=builder /app /app
WORKDIR /app
ENV PATH=/app/venv/bin:$PATH

CMD [ "gunicorn", "app:app" ]