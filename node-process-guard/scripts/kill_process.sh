#!/usr/bin/env bash
set -uo pipefail

# Node Process Guard - Kill Process Script
# Safely terminates a process by PID with graceful fallback

PID="${1:-}"
FORCE="${2:-false}"

if [[ -z "$PID" || ! "$PID" =~ ^[0-9]+$ ]]; then
    echo '{"success": false, "error": "Invalid or missing PID"}'
    exit 1
fi

if ! kill -0 "$PID" 2>/dev/null; then
    echo "{\"success\": false, \"error\": \"Process $PID does not exist or no permission\"}"
    exit 1
fi

# Get process info before killing
proc_info=$(ps -p "$PID" -o pid=,command= 2>/dev/null | sed 's/^[[:space:]]*//' || true)

if [[ "$FORCE" == "true" ]]; then
    kill -9 "$PID" 2>/dev/null
    sleep 0.5
    if ! kill -0 "$PID" 2>/dev/null; then
        echo "{\"success\": true, \"pid\": $PID, \"command\": \"$proc_info\", \"method\": \"SIGKILL\", \"message\": \"Process killed forcefully\"}"
    else
        echo "{\"success\": false, \"pid\": $PID, \"error\": \"Failed to kill process even with SIGKILL\"}"
    fi
else
    # Try graceful kill first
    kill -15 "$PID" 2>/dev/null
    sleep 1
    if ! kill -0 "$PID" 2>/dev/null; then
        echo "{\"success\": true, \"pid\": $PID, \"command\": \"$proc_info\", \"method\": \"SIGTERM\", \"message\": \"Process terminated gracefully\"}"
    else
        # Fallback to force kill
        kill -9 "$PID" 2>/dev/null
        sleep 0.5
        if ! kill -0 "$PID" 2>/dev/null; then
            echo "{\"success\": true, \"pid\": $PID, \"command\": \"$proc_info\", \"method\": \"SIGKILL (after SIGTERM timeout)\", \"message\": \"Process killed after graceful termination failed\"}"
        else
            echo "{\"success\": false, \"pid\": $PID, \"error\": \"Failed to terminate process\"}"
        fi
    fi
fi
