# 📶 Smart Mobile Network Analyzer

A Python-based application that analyzes your current network connection, measures speed and latency, and provides a comprehensive quality score along with actionable recommendations. 

This project features both a graphical user interface (GUI) built with Tkinter and a Command Line Interface (CLI) for flexible usage.

---

## 🎯 Project Objective
**Project:** SMART MOBILE NETWORK ANALYZER, 2025-26  
**Objective:** Develop a GUI-based smart mobile network analyzer to understand current network conditions and performance metrics.

---

## ✨ Features
*   **Comprehensive Metrics:** Measures local IP Address, Connection Type (Wi-Fi, Ethernet, Mobile Data), Ping (ms), Jitter (ms), Download speed (Mbps), and Upload speed (Mbps).
*   **Intelligent Scoring:** Calculates a weighted network score (out of 100) based on download (40%), upload (20%), ping (25%), and jitter (15%).
*   **Quality Classification:** Categorizes the network as "Excellent" (80+), "Good" (60-79), "Fair" (35-59), or "Poor" (<35).
*   **Actionable Recommendations:** Provides tailored tips based on the analysis (e.g., suitable for 4K streaming, warnings about high latency for gaming, etc.).
*   **History Logging & Visualization:** Automatically logs test results to a `history.csv` file and plots a historical graph of network scores using Matplotlib.
*   **Dual Interfaces:** Includes both a user-friendly Tkinter GUI and a lightweight CLI.

---

## 📁 Project Structure
*   `main.py` - The main entry point for the Tkinter GUI application. Handles UI setup, progress bars, and historical score graphing.
*   `CLI.py` - The command-line interface version of the analyzer for terminal-based testing.
*   `analyzer.py` - Contains the core logic for scoring the network, classifying the quality band, and generating recommendations.
*   `network_utils.py` - Handles system-level operations including retrieving local IP, detecting active network interfaces (`psutil`), measuring ping/jitter, and running speed tests (`speedtest`).
*   `history.csv` - *(Generated automatically)* Stores timestamped logs of all network tests.

---

## 🛠️ Prerequisites & Installation

Before running the application, ensure you have Python installed (Python 3.x recommended) along with the required external libraries.

1. **Clone the repository:**
   ```bash

   Install required dependencies:

Bash
pip install matplotlib psutil speedtest-cli
(Note: Standard libraries like tkinter, socket, subprocess, threading, csv, re, and platform are included with Python by default).

🚀 Usage
To launch the Graphical User Interface (GUI):

Bash
python main.py
Click the "Analyze Network" button to begin the test. The measurement process typically takes 15-30 seconds.

To run the Command Line Interface (CLI):

Bash
python CLI.py



   👨‍💻 Credits
Student Name: Priyanshu Baunthiyal

SAP ID: 1000017309

Institution: DIT University
   git clone [https://github.com/yourusername/smart-mobile-network-analyzer.git](https://github.com/yourusername/smart-mobile-network-analyzer.git)
   cd smart-mobile-network-analyzer
