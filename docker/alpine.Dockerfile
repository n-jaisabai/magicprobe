FROM alpine:3.19

# 'file' package provides libmagic.so on Alpine / musl
RUN apk add --no-cache \
        python3 \
        py3-pip \
        file

WORKDIR /app
COPY . .

RUN pip3 install --no-cache-dir --break-system-packages -e ".[dev]"

CMD ["python3", "-m", "pytest", "tests/integration/", "-v"]
