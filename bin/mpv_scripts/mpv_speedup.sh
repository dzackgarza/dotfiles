#!/bin/bash
echo '{command: ["add", "speed", "+0.25"]}' | socat - /tmp/node-mpv.sock
