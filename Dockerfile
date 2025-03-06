FROM ubuntu:24.04 AS builder
RUN apt update && apt install -y python3 python3-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/idapro-9.0
COPY . /opt/idapro-9.0
RUN echo "0b12a798f0e2ab7c5b7a795eb275136af7fce88356fddefd7f7776c6aa588372 idapro_90_x64linux.run" | sha256sum -c && \
    chmod +x idapro_90_x64linux.run && \
    ./idapro_90_x64linux.run --mode unattended && \
    rm idapro_90_x64linux.run && \
    ./idapyswitch --auto-apply && \
    python3 idakeygen.py && \
    rm idakeygen.py && \
    mv libida.so.patched libida.so && \
    mv libida64.so.patched libida64.so && \
    mv analysis.idc idc && \
    mv ida.reg /root/.idapro

FROM ubuntu:24.04
RUN apt update && apt install -y python3 python3-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/idapro-9.0
COPY --from=builder /opt/idapro-9.0 /opt/idapro-9.0
COPY --from=builder /root/.idapro /root/.idapro

ENTRYPOINT ["/opt/idapro-9.0/idat64"]
