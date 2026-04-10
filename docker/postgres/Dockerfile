FROM postgres:16

RUN apt-get update && apt-get install -y locales \
    && sed -i '/pt_BR.UTF-8/s/^# //' /etc/locale.gen \
    && locale-gen \
    && rm -rf /var/lib/apt/lists/*
