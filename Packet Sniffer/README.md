# 🚀 Network Packet Sniffer & Analyzer

A real-time network packet sniffer and analyzer built with Python. Captures network traffic, analyzes protocols, monitors bandwidth, and detects suspicious activity.

## ✨ Features

- **Real-time Packet Capture** - Raw socket networking for all interface traffic
- **Protocol Analysis** - TCP, UDP, ICMP, IPv4/IPv6 parsing
- **Traffic Visualization** - Live dashboard and Matplotlib charts
- **Security Monitoring** - Alert system for suspicious activity
- **Bandwidth Analysis** - Real-time throughput monitoring
- **Connection Tracking** - Network conversation analysis
- **Comprehensive Reporting** - JSON export with full analysis

## 🛠️ Installation

### Prerequisites
- Python 3.6+
- Linux/macOS (Windows requires additional setup)
- Root/Administrator privileges for packet capture

### Install Dependencies
```bash
pip install matplotlib numpy

sudo python sniffer.py

sudo python sniffer.py -i eth0 --no-display

sudo python sniffer.py -m 5000

sudo python sniffer.py -i eth0 -m 10000 --no-display