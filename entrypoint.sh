#!/usr/bin/env sh
if [ "$MODE" = "cli" ]; then
    exec /opt/ida-pro-9.1/idat "$@"
elif [ "$MODE" = "x11" ]; then
    exec /opt/ida-pro-9.1/ida "$@"
else
    exit 1
fi
