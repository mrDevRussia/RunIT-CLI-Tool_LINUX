#!/usr/bin/env bash
set -euo pipefail

echo "[RunIT-Linux] Installing dependencies"

detect_pm() {
  if command -v apt >/dev/null 2>&1; then echo apt; return; fi
  if command -v dnf >/dev/null 2>&1; then echo dnf; return; fi
  if command -v pacman >/dev/null 2>&1; then echo pacman; return; fi
  echo none
}

PM=$(detect_pm)
case "$PM" in
  apt)
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv build-essential
    ;;
  dnf)
    sudo dnf install -y python3 python3-pip python3-virtualenv gcc python3-devel
    ;;
  pacman)
    sudo pacman -Sy --needed python python-pip
    ;;
  none)
    echo "No supported package manager detected. Ensure Python3 and pip are installed."
    ;;
esac

pip3 install --upgrade pip
pip3 install requests cryptography psutil

chmod +x "$(dirname "$0")/run.sh"
echo "[RunIT-Linux] Installation complete"