#!/usr/bin/env bash
# lean-polish 시각 확인용 로컬 서버(앱 안 브라우저는 file:// 주소를 캡처할 수 없다).
# 사용: serve.sh start <폴더> [포트=8765]   |   serve.sh stop
# 127.0.0.1에만 열고, 끝나면 반드시 stop 한다.
set -u
PID_FILE="${TMPDIR:-/tmp}/lean-polish-serve.pid"

case "${1:-}" in
  start)
    dir="${2:-}"; port="${3:-8765}"
    [ -d "$dir" ] || { echo "폴더가 없습니다: $dir"; exit 2; }
    if [ -f "$PID_FILE" ] && kill -0 "$(cut -d' ' -f1 "$PID_FILE")" 2>/dev/null; then
      echo "이미 실행 중입니다: $(cat "$PID_FILE") (먼저 stop 하세요)"; exit 0
    fi
    cd "$dir" || exit 2
    nohup python3 -m http.server "$port" --bind 127.0.0.1 >/dev/null 2>&1 &
    pid=$!
    echo "$pid $port" > "$PID_FILE"
    sleep 1
    if kill -0 "$pid" 2>/dev/null; then
      echo "시작: http://127.0.0.1:$port/  (폴더: $dir)"
    else
      echo "시작 실패(포트가 이미 쓰이는 중일 수 있습니다)"; rm -f "$PID_FILE"; exit 1
    fi
    ;;
  stop)
    [ -f "$PID_FILE" ] || { echo "실행 중인 서버가 없습니다"; exit 0; }
    pid=$(cut -d' ' -f1 "$PID_FILE")
    if kill "$pid" 2>/dev/null; then echo "종료: $pid"; else echo "이미 종료되어 있습니다"; fi
    rm -f "$PID_FILE"
    ;;
  *)
    echo "사용: serve.sh start <폴더> [포트] | serve.sh stop"; exit 2
    ;;
esac
