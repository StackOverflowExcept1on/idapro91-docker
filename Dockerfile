FROM ubuntu:24.04 AS builder
RUN apt update && \
    apt install --no-install-recommends --yes \
        python3 \
        libpython3.12t64 && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /opt/ida-pro-9.1
COPY . /opt/ida-pro-9.1
RUN echo "8ff08022be3a0ef693a9e3ea01010d1356b26cfdcbbe7fdd68d01b3c9700f9e2 ida-pro_91_x64linux.run" | sha256sum -c && \
    chmod +x ida-pro_91_x64linux.run && \
    mkdir -p /root/.local/share/applications && \
    ./ida-pro_91_x64linux.run --mode unattended && \
    rm ida-pro_91_x64linux.run && \
    ./idapyswitch --verbose --auto-apply --ignore-python-config && \
    export PYTHONDONTWRITEBYTECODE=1 && \
    python3 idakeygen.py && \
    python3 idareggen.py && \
    rm idakeygen.py && \
    rm idareggen.py && \
    sed -i '37,46d' idc/analysis.idc

FROM ubuntu:24.04
ARG MODE=cli
ENV MODE=$MODE
RUN apt update && \
    apt install --no-install-recommends --yes \
        python3 \
        libpython3.12t64 && \
    if [ "$MODE" = "x11" ]; then \
        apt install --no-install-recommends --yes \
            libgl1 \
            libglib2.0-0 \
            libfontconfig1 \
            libxcb-icccm4 \
            libxcb-image0 \
            libxcb-keysyms1 \
            libxcb-render-util0 \
            libxcb-shape0 \
            libxcb-xinerama0 \
            libxcb-xkb1 \
            libsm6 \
            libxkbcommon-x11-0 \
            libdbus-1-3; \
    fi && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /opt/ida-pro-9.1
COPY --from=builder /opt/ida-pro-9.1 /opt/ida-pro-9.1
COPY --from=builder /root/.idapro /root/.idapro
ENTRYPOINT ["/opt/ida-pro-9.1/entrypoint.sh"]
