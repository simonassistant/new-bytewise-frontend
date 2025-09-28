#!/bin/bash

echo "=== Aliyun Server Git Setup Script ==="
echo "Step 1: Identifying Linux Distribution..."

# Check the distribution
echo "--- OS Release Info ---"
cat /etc/os-release 2>/dev/null || echo "os-release not found"

echo -e "\n--- LSB Release Info ---"
lsb_release -a 2>/dev/null || echo "lsb_release not available"

echo -e "\n--- Issue Info ---"
cat /etc/issue 2>/dev/null || echo "issue file not found"

echo -e "\n--- System Info ---"
uname -a

echo -e "\n--- Available Package Managers ---"
which apt-get 2>/dev/null && echo "apt-get available" || echo "apt-get not found"
which yum 2>/dev/null && echo "yum available" || echo "yum not found"
which dnf 2>/dev/null && echo "dnf available" || echo "dnf not found"
which apk 2>/dev/null && echo "apk available" || echo "apk not found"
which zypper 2>/dev/null && echo "zypper available" || echo "zypper not found"
which pacman 2>/dev/null && echo "pacman available" || echo "pacman not found"

echo -e "\n--- Checking if Git is already installed ---"
which git 2>/dev/null && git --version || echo "Git not found"

echo -e "\n=== Installation Commands Based on System ==="
echo "Based on the above information, use one of these commands:"
echo ""
echo "For Ubuntu/Debian: apt update && apt install -y git"
echo "For CentOS/RHEL: yum install -y git"
echo "For Fedora: dnf install -y git"
echo "For Alpine: apk update && apk add git"
echo "For OpenSUSE: zypper install git"
echo "For Arch: pacman -S git"
echo ""
echo "After installation, run:"
echo "git --version"
echo "which git-receive-pack"
echo "mkdir -p /var/git && cd /var/git && git init --bare new-bytewise-frontend.git"
