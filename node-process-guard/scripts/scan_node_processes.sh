#!/usr/bin/env bash
set -euo pipefail

# Node Process Guard - Scan Script
# Scans all Node-related processes, detects conflicts, and outputs JSON report
# This script ONLY collects data. Analysis and reporting are done by the LLM.

# System Node processes to exclude (known system apps that use Node)
SYSTEM_PATTERNS=(
    "WeDrive"
    "wemail"
    "CCXProcess"
    "Creative Cloud"
    "Slack"
    "Discord"
    "Cursor"
    "VS Code"
    "Code Helper"
    "Electron"
    "企业微信"
    "腾讯会议"
    "QQ"
    "微信"
    "Microsoft Teams"
    "Notion"
    "Obsidian"
    "Figma"
    "/Applications/Utilities"
    "/System/"
)

is_system_process() {
    local cmd="$1"
    for pattern in "${SYSTEM_PATTERNS[@]}"; do
        if [[ "$cmd" == *"$pattern"* ]]; then
            return 0
        fi
    done
    return 1
}

# Get process info: pid ppid command etime cpu mem
get_process_info() {
    local pid="$1"
    ps -p "$pid" -o pid=,ppid=,etime=,%cpu=,%mem=,command= 2>/dev/null || true
}

# Get working directory
get_cwd() {
    local pid="$1"
    lsof -a -d cwd -p "$pid" -Fn 2>/dev/null | grep '^n' | sed 's/^n//' | head -1 || echo ""
}

# Get listening ports (macOS lsof needs -a for AND logic between -p and -i)
get_ports() {
    local pid="$1"
    lsof -a -iTCP -sTCP:LISTEN -Pn -p "$pid" 2>/dev/null | awk 'NR>1 {print $9}' | sed -E 's/.*]:?([0-9]+).*/\1/' | sort -u | tr '\n' ',' | sed 's/,$//' || echo ""
}

# Build array of PIDs
declare -a ALL_PIDS=()

# Helper to add unique PID
add_pid() {
    local p="$1"
    if [[ -n "$p" && "$p" =~ ^[0-9]+$ ]]; then
        if [[ ${#ALL_PIDS[@]} -gt 0 ]]; then
            for existing in "${ALL_PIDS[@]}"; do
                if [[ "$existing" == "$p" ]]; then return; fi
            done
        fi
        ALL_PIDS+=("$p")
    fi
}

# Find Node-related PIDs from ps
while IFS= read -r line; do
    pid=$(echo "$line" | awk '{print $2}')
    add_pid "$pid"
done < <(ps aux | grep -iE '(node|npm|npx|pnpm|yarn|vite|next|tsx)' | grep -v grep)

# Also from pgrep
while IFS= read -r pid; do
    add_pid "$pid"
done < <(pgrep -f "(node|npm|npx|pnpm|yarn|vite|next|tsx)" 2>/dev/null || true)

if [[ ${#ALL_PIDS[@]} -eq 0 ]]; then
    echo '{"processes": [], "conflicts": [], "totalCount": 0, "scanTime": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"}'
    exit 0
fi

# Build JSON lines for each process
JSON_LINES=""
for pid in "${ALL_PIDS[@]}"; do
    info=$(get_process_info "$pid")
    [[ -z "$info" ]] && continue

    # Parse ps output: pid ppid etime %cpu %mem command...
    # Command may contain spaces, so we reconstruct from field 6 onward
    ppid=$(echo "$info" | awk '{print $2}')
    etime=$(echo "$info" | awk '{print $3}')
    cpu=$(echo "$info" | awk '{print $4}')
    mem=$(echo "$info" | awk '{print $5}')
    cmd=$(echo "$info" | awk '{for(i=6;i<=NF;i++) printf "%s%s", (i>6?" ":""), $i; print ""}')
    # Trim leading spaces
    cmd=$(echo "$cmd" | sed 's/^[[:space:]]*//')

    # Skip system processes and false positives
    if is_system_process "$cmd"; then continue; fi
    if [[ "$cmd" == *"grep"* ]] || [[ "$cmd" == *"ps aux"* ]]; then continue; fi

    cwd=$(get_cwd "$pid")
    ports=$(get_ports "$pid")

    # Identify project name
    project_name=""
    if [[ -n "$cwd" ]]; then
        project_name=$(basename "$cwd")
        if [[ -f "$cwd/package.json" ]]; then
            pkg_name=$(grep -m1 '"name"' "$cwd/package.json" 2>/dev/null | sed -E 's/.*"name"[^"]*"([^"]*)".*/\1/' || true)
            if [[ -n "$pkg_name" && "$pkg_name" != "name" ]]; then
                project_name="$pkg_name"
            fi
        fi
    fi

    # Determine process type
    proc_type="node"
    if [[ "$cmd" == *"npm"* ]]; then proc_type="npm"
    elif [[ "$cmd" == *"pnpm"* ]]; then proc_type="pnpm"
    elif [[ "$cmd" == *"yarn"* ]]; then proc_type="yarn"
    elif [[ "$cmd" == *"vite"* ]]; then proc_type="vite"
    elif [[ "$cmd" == *"next"* ]]; then proc_type="next"
    fi

    # Build one JSON object line via jq
    line=$(jq -n \
        --argjson pid "$pid" \
        --argjson ppid "${ppid:-0}" \
        --arg type "$proc_type" \
        --arg command "$cmd" \
        --arg cwd "$cwd" \
        --arg projectName "$project_name" \
        --arg ports "$ports" \
        --arg etime "$etime" \
        --arg cpu "$cpu" \
        --arg mem "$mem" \
        '{pid: $pid, ppid: $ppid, type: $type, command: $command, cwd: $cwd, projectName: $projectName, ports: $ports, elapsedTime: $etime, cpuPercent: $cpu, memoryPercent: $mem}')

    if [[ -n "$JSON_LINES" ]]; then
        JSON_LINES="$JSON_LINES
$line"
    else
        JSON_LINES="$line"
    fi
done

if [[ -z "$JSON_LINES" ]]; then
    echo '{"processes": [], "conflicts": [], "totalCount": 0, "scanTime": "'"$(date -u +%Y-%m-%dT%H:%M:%SZ)"'"}'
    exit 0
fi

# Assemble full JSON with jq
processes_json=$(echo "$JSON_LINES" | jq -s '.')

# Detect conflicts using jq
# 1. Duplicate ports: different processes listening on same port
dup_port_conflicts=$(echo "$processes_json" | jq -r '
    [
      .[] | select(.ports != "" and .ports != null) |
      . as $proc |
      (.ports | split(","))[] |
      { port: (. | gsub(" ";"")), pid: $proc.pid, projectName: $proc.projectName, command: $proc.command, cwd: $proc.cwd }
    ] | group_by(.port) | map(select(length > 1)) | .[]
')

# 2. Duplicate cwd: same project directory has multiple independent process trees.
# Exclude normal parent-child chains by counting root processes per cwd.
# A root process has no parent (ppid) present in the same cwd group.
dup_cwd_conflicts=$(echo "$processes_json" | jq -r '
    [ .[] | select(.cwd != "" and .cwd != null) ] |
    group_by(.cwd) |
    map(select(length > 1)) |
    map(
      . as $group |
      # collect all pids in this group
      ($group | map(.pid)) as $pids |
      # root processes: ppid is NOT in $pids
      [ .[] | select(.ppid as $ppid | $pids | index($ppid) | not) ] as $roots |
      # only report if more than one independent root exists
      select($roots | length > 1) |
      { cwd: .[0].cwd, projectName: .[0].projectName, items: $roots }
    ) | .[]
')

# Build conflicts array
conflicts_json="[]"
if [[ -n "$dup_port_conflicts" && "$dup_port_conflicts" != "[]" && "$dup_port_conflicts" != "null" ]]; then
    conflicts_json=$(echo "$dup_port_conflicts" | jq -s '. | map({type: "duplicate_port", items: .})')
fi

if [[ -n "$dup_cwd_conflicts" && "$dup_cwd_conflicts" != "[]" && "$dup_cwd_conflicts" != "null" ]]; then
    new_conflicts=$(echo "$dup_cwd_conflicts" | jq -s '. | map({type: "duplicate_cwd", items: .items})')
    if [[ "$conflicts_json" == "[]" ]]; then
        conflicts_json="$new_conflicts"
    else
        conflicts_json=$(echo "$conflicts_json $new_conflicts" | jq -s 'add')
    fi
fi

# Final output — raw JSON only. The LLM will analyze and send the report.
echo "$processes_json" | jq --argjson conflicts "$conflicts_json" '{
    processes: .,
    conflicts: $conflicts,
    totalCount: length,
    scanTime: (now | todateiso8601)
}'
