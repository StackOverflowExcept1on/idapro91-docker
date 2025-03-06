### idapro90-docker

[![Docker Pulls](https://img.shields.io/docker/pulls/stackoverflowexcept1on/idapro)](https://hub.docker.com/r/stackoverflowexcept1on/idapro)
[![Docker Image](https://img.shields.io/badge/docker_image-995MB-blue)](https://hub.docker.com/r/stackoverflowexcept1on/idapro)

IDA Pro 9.0 Docker Image that can be used in batch mode (without GUI). You can run IDA Pro on a Linux server at night and get `database.i64` the next day.

### Requirements

- `ida-pro_90_x64linux.run` file, which can be downloaded from release page

### Building

```bash
docker build --tag stackoverflowexcept1on/idapro .
```

### Installing

If you don't want to build anything, pre-built docker image is available:

```bash
docker pull stackoverflowexcept1on/idapro
```

### Running

```bash
mkdir -p demo && cd demo
cp /bin/cat .
docker run --rm -it -v $(pwd):/files stackoverflowexcept1on/idapro -P+ -B /files/cat
ls cat.i64
```
