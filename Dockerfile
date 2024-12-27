FROM python:3.11.6-slim-bullseye AS builder

ENV TZ=Europe/Paris
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app
COPY . .

RUN <<EOT
# apt update
# apt install -y build-essential curl apt-utils python3-dev
python3 -m venv venv
export PATH=/app/venv/bin:$PATH
pip install pip -U
pip install --no-cache-dir -r requirements.txt
# apt remove -y build-essential
# apt autoremove
# apt autoclean
# rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
EOT

FROM python:3.11.6-alpine

ARG UID
ARG GID
ARG UNAME

COPY --from=builder /app /app
RUN <<EOT
addgroup -S -g ${GID} ${UNAME}
adduser -S -u ${UID} -g ${GID} ${UNAME}
chown -R ${UID}:${GID} /app
EOT

WORKDIR /app
ENV PATH=/app/venv/bin:$PATH
USER ${UNAME}

CMD [ "gunicorn", "app:app" ]
