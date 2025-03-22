### idapro91-docker

[![Docker Pulls](https://img.shields.io/docker/pulls/stackoverflowexcept1on/idapro)](https://hub.docker.com/r/stackoverflowexcept1on/idapro)
[![Docker Image](https://img.shields.io/badge/docker_image-1.01GB-blue)](https://hub.docker.com/r/stackoverflowexcept1on/idapro)

IDA Pro 9.1 Docker Image that can be used both in batch mode (without GUI) and with X11 forwarding. You can run IDA Pro on a Linux server at night and get `database.i64` the next day.

### Requirements

- `ida-pro_91_x64linux.run` file, which can be downloaded from release page

### Building

```bash
docker build \
    --build-arg MODE=cli \
    --platform linux/amd64 \
    --tag stackoverflowexcept1on/idapro:cli .
```

```bash
docker build \
    --build-arg MODE=x11 \
    --platform linux/amd64 \
    --tag stackoverflowexcept1on/idapro:x11 .
```

### Installing

If you don't want to build anything, pre-built docker image is available:

```bash
docker pull \
    --platform linux/amd64 \
    stackoverflowexcept1on/idapro:cli
```

```bash
docker pull \
    --platform linux/amd64 \
    stackoverflowexcept1on/idapro:x11
```

### Running

```bash
mkdir -p demo && cd demo
cp /bin/cat .
docker run \
    --hostname hostname \
    --interactive \
    --name container \
    --platform linux/amd64 \
    --rm \
    --tty \
    --volume $(pwd):/files \
    stackoverflowexcept1on/idapro:cli \
        -B \
        -P+ \
        /files/cat
ls cat.i64
```

```bash
mkdir -p demo && cd demo
cp /bin/cat .
xhost +local:docker
docker run \
    --hostname hostname \
    --interactive \
    --env DISPLAY=$DISPLAY \
    --name container \
    --platform linux/amd64 \
    --rm \
    --tty \
    --volume $(pwd):/files \
    --volume /tmp/.X11-unix:/tmp/.X11-unix \
    stackoverflowexcept1on/idapro:x11 \
        /files/cat
ls cat.i64
```
