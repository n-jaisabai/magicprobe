FROM fedora:40

RUN dnf install -y \
        python3 \
        python3-pip \
        file-libs \
    && dnf clean all

WORKDIR /app
COPY . .

RUN pip3 install --no-cache-dir -e ".[dev]"

CMD ["python3", "-m", "pytest", "tests/integration/", "-v"]
