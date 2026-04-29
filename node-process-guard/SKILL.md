---
name: node-process-guard
description: Scan and manage local background Node.js processes, detect port conflicts and duplicate project instances, generate reports, and optionally fix issues by terminating redundant processes. Use when the user mentions checking background processes, Node processes, port conflicts, duplicate dev servers, forgotten npm run dev, killing background services, cleaning up Node processes, or any scenario involving managing local development servers for Node/frontend/backend projects. Trigger words include "检查后台进程", "端口冲突", "node进程", "重复启动", "关闭后台服务", "清理node进程", "npm run dev", "vite", "next".
---

# Node Process Guard

Scan, report, and optionally clean up background Node.js processes on macOS/Linux.

## What This Skill Does

1. **Scan** all Node-related processes (`node`, `npm`, `pnpm`, `yarn`, `npx`, `vite`, `next`, `tsx`)
2. **Detect conflicts**: duplicate ports, duplicate independent process trees in same project directory
3. **Generate a report** with process list, ports, CPU/memory usage, and conflict summary
4. **Optionally fix** by terminating redundant or conflicting processes (with user confirmation)

## Workflow (End-to-End, No User Intervention)

### Step 1: Scan

Run the scan script to collect raw data:

```bash
bash scripts/scan_node_processes.sh
```

Output is a JSON object with:
- `processes[]` — all detected Node processes (pid, ppid, type, command, cwd, projectName, ports, elapsedTime, cpuPercent, memoryPercent)
- `conflicts[]` — detected conflicts:
  - `duplicate_port`: two+ processes listening on the same TCP port
  - `duplicate_cwd`: two+ independent root processes in the same project directory (excludes normal parent-child chains)
- `totalCount` — number of processes found
- `scanTime` — ISO timestamp

### Step 2: LLM Analysis & Report

**You (Claude) analyze the JSON data and write a natural-language report.** Do NOT use hardcoded templates. Think through the actual data and explain it in plain language that a medium-skilled developer can understand.

**Analysis guidelines:**

1. **Group by project** — tell the user which projects are running
2. **Explain what's normal** — a typical `npm run dev` produces a chain like shell → npm → vite → esbuild. Multiple processes under one project with parent-child relationships (ppid present in the same cwd group) is **normal and expected**. Only flag truly independent roots as problematic.
3. **Explain conflicts clearly**:
   - **Duplicate port**: "Port X is occupied by multiple processes. This means if you try to start another service on the same port, it will fail."
   - **Duplicate cwd**: "Project Y has been started independently more than once (not via parent-child fork). This usually happens when you ran `npm run dev` in different terminals at different times."
4. **Give actionable advice** — for each conflict, suggest which PID(s) to keep and which to terminate (typically keep the newer one, kill the older/forgotten one)
5. **Be honest** — if there's nothing wrong, say so clearly

### Step 3: Send Report to Lark

Send the natural-language analysis via `lark-cli` to the fixed chat:

```bash
lark-cli im +messages-send --chat-id oc_578717a43c0e5011765d9cada71d8218 --text "$analysis"
```

> **Fixed target chat**: `oc_578717a43c0e5011765d9cada71d8218`
> If `lark-cli` is not configured, run `lark-cli auth login` first (see `lark-shared` skill).

### Keeping Claude Code Running for Scheduled Tasks

The daily scan is scheduled via Claude Code's built-in scheduler (`CronCreate`). For it to fire reliably, Claude Code must remain running in the background.

Use the helper script (system-wide, not inside this skill):

```bash
# Start daemon
start-claude

# Check status
start-claude --status

# Attach to interact
start-claude --attach

# Stop daemon
start-claude --kill
```

> Script location: `~/.claude/scripts/start-claude.sh`
> Symlink: `~/.local/bin/start-claude` (already in your PATH)

### Step 4: Ask Before Fixing (If Conflicts Exist)

**Never kill processes without explicit user approval.**

For each conflict, ask the user which PID(s) to terminate. For example:

> "Project `etfgauge-frontend` has 2 independent dev servers running:
> - PID 4601 (vite on port 5173, started 2 days ago)
> - PID 8100 (vite on port 5173, started 10 minutes ago)
>
> Which one should I terminate?"

### Step 5: Terminate (If Approved)

Use the kill script for safe termination:

```bash
bash scripts/kill_process.sh <PID> [force]
```

Behavior:
- Default: `SIGTERM` → wait 1s → `SIGKILL` if still alive
- `force=true`: `SIGKILL` immediately

Always report the result (success/failure, method used).

## System Process Exclusions

The scan automatically excludes known system apps that embed Node:

- WeDrive / wemail / 企业微信 / 腾讯会议 / 微信 / QQ
- Slack / Discord / Microsoft Teams / Notion / Obsidian / Figma
- VS Code / Cursor / Code Helper / Electron
- Adobe Creative Cloud / CCXProcess
- `/Applications/Utilities` and `/System/` paths

If a legitimate dev process is misclassified, review its `command` field and adjust the `SYSTEM_PATTERNS` array in `scripts/scan_node_processes.sh`.

## Conflict Detection Details

### Duplicate Port
Triggered when two or more processes (from different PIDs) listen on the same TCP port.

### Duplicate Project Root
Triggered when a project directory (`cwd`) contains **more than one independent root process**. A root process is defined as a process whose parent (`ppid`) is NOT also in the same project directory.

This correctly ignores normal parent-child chains (e.g., shell wrapper → npm → vite → esbuild) and only flags truly duplicate instances.

## Important Notes

- **macOS `lsof` uses `-a` for AND logic** between `-p` (PID) and `-i` (network). The script already handles this.
- **Port extraction**: handles both IPv4 (`*:5173`) and IPv6 (`[::1]:5173`) formats.
- **Project name**: reads `name` from `package.json` in the process's working directory; falls back to directory basename.
- **Zombie/child processes**: the scan includes child processes (esbuild, tsx, etc.) so the user sees the full picture. When killing, usually terminate the root wrapper (shell/npm) rather than individual children.
