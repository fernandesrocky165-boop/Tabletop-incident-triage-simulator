#!/usr/bin/env python3
"""
Root entrypoint for running the Web Dashboard GUI.
Usage: python run_web.py [--port 5000] [--host 127.0.0.1]
"""

import sys
import os
import argparse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from web.app import run_server

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Start SOC Operations Tabletop Simulator Web GUI")
    parser.add_argument("--port", type=int, default=5000, help="Port to listen on (default 5000)")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host interface (default 127.0.0.1)")
    args = parser.parse_args()

    print(f"\n=======================================================")
    print(f" SOC Operations Tabletop Incident Triage Web Dashboard")
    print(f" Aligned with NIST SP 800-61r2 & MITRE ATT&CK")
    print(f" Running at: http://{args.host}:{args.port}")
    print(f"=======================================================\n")

    run_server(host=args.host, port=args.port, debug=False)
