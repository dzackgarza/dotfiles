#!/usr/bin/env bash

MAXFILE="$HOME/.config/waybar/max_upload.txt"
TMPFILE="/tmp/waybar_maxtest.txt"

while true; do
  # Use curl to upload /dev/zero for 10 seconds, get peak rate
  BYTES=$(dd if=/dev/zero bs=1M count=10 2>/dev/null | \
    curl -s -o /dev/null --max-time 10 -T - https://transfer.sh/test 2>&1 | \
    grep -oE '[0-9.]+ [kMG]B/s' | tail -1)

  # Parse to bytes/sec
  RATE_BPS=$(awk -v rate="$BYTES" '
    BEGIN {
      split(rate, parts, " ");
      n = parts[1];
      unit = parts[2];
      mult = (unit == "kB/s") ? 1024 :
             (unit == "MB/s") ? 1048576 :
             (unit == "GB/s") ? 1073741824 : 1;
      print n * mult
    }')

  # Convert to Mbps and save
  if [[ "$RATE_BPS" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    RATE_MBPS=$(awk -v bps="$RATE_BPS" 'BEGIN { printf "%.2f", bps / 125000 }')
    echo "$RATE_MBPS" > "$MAXFILE"
  fi

  sleep 60
done

