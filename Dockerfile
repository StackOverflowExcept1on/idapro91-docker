FROM ubuntu:24.04 AS builder
RUN apt update && apt install -y python3 python3-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/ida-pro-9.1
COPY . /opt/ida-pro-9.1
RUN echo "8ff08022be3a0ef693a9e3ea01010d1356b26cfdcbbe7fdd68d01b3c9700f9e2 ida-pro_91_x64linux.run" | sha256sum -c && \
    chmod +x ida-pro_91_x64linux.run && \
    mkdir -p /root/.local/share/applications && \
    ./ida-pro_91_x64linux.run --mode unattended && \
    rm ida-pro_91_x64linux.run && \
    ./idapyswitch --auto-apply && \
    python3 idakeygen.py && \
    rm idakeygen.py && \
    mv analysis.idc idc && \
    mv ida.reg /root/.idapro

FROM ubuntu:24.04
RUN apt update && apt install -y python3 python3-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/ida-pro-9.1
COPY --from=builder /opt/ida-pro-9.1 /opt/ida-pro-9.1
COPY --from=builder /root/.idapro /root/.idapro

ENTRYPOINT ["/opt/ida-pro-9.1/idat"]
