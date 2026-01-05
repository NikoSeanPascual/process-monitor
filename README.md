# Niko’s Process Monitor — Mini Task Manager

A **hacker-style Mini Task Manager** built with **CustomTkinter** that displays running system processes in real time, allows searching and filtering, and supports terminating processes directly from the UI.

Designed to look minimal, fast, and terminal-inspired while demonstrating **OS interaction, threading, and real-time UI updates**.

---

## Features

### 🖥 Real-Time Process Monitoring
- Displays currently running processes
- Auto-refreshes every few seconds
- Groups duplicate processes and aggregates memory usage

### 🔍 Live Search & Filtering
- Instantly filter processes by name
- Case-insensitive, real-time updates

### 🧠 Memory Usage Tracking
- Shows memory usage per process (MB)
- Sorted by highest memory usage by default

### 🧵 Background Processing
- Process fetching runs in a background thread
- UI remains responsive at all times

### 🖱 Context Menu Controls
- Right-click any process to terminate it
- Uses native system commands (`taskkill`)
- Immediate effect with no UI freezing

### 🧬 Hacker-Style UI
- Neon green terminal aesthetic
- Custom fonts with fallback handling
- Scrollable process table
- Fixed widget pool for performance

---

## Tech Stack

- **Python**
- **CustomTkinter** (modern UI framework)
- **Tkinter** (standard library)
- **subprocess** (OS command execution)
- **threading**
- **time**

---

## Requirements

Install the required dependency before running:

```bash
pip install customtkinter
