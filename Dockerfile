FROM ubuntu:24.04 AS builder
RUN apt update && apt install -y python3 python3-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/ida-pro-9.0
COPY . /opt/ida-pro-9.0
RUN echo "c0e2d5f410f8a4a3745bb219d821d690ce1768a5ce0a25e86e0c30c1fe599c71 ida-pro_90_x64linux.run" | sha256sum -c && \
    chmod +x ida-pro_90_x64linux.run && \
    mkdir -p /root/.local/share/applications && \
    ./ida-pro_90_x64linux.run --mode unattended && \
    rm ida-pro_90_x64linux.run && \
    ./idapyswitch --auto-apply && \
    python3 idakeygen.py && \
    rm idakeygen.py && \
    mv analysis.idc idc && \
    mv ida.reg /root/.idapro

FROM ubuntu:24.04
RUN apt update && apt install -y python3 python3-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/ida-pro-9.0
COPY --from=builder /opt/ida-pro-9.0 /opt/ida-pro-9.0
COPY --from=builder /root/.idapro /root/.idapro

ENTRYPOINT ["/opt/ida-pro-9.0/idat"]
