"""
main.py
-------
Smart Mobile Network Analyzer - Tkinter GUI
"""

import csv
import os
import threading
import datetime
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import network_utils
import analyzer

LOG_FILE = os.path.join(os.path.dirname(__file__), "history.csv")

QUALITY_COLORS = {
    "Excellent": "#2e7d32",
    "Good": "#558b2f",
    "Fair": "#f9a825",
    "Poor": "#c62828",
    "Unknown": "#616161",
}

class NetworkAnalyzerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart Mobile Network Analyzer")
        self.geometry("620x600")
        self.resizable(False, False)
        self.configure(bg="#f4f6f8")

        self._build_widgets()
        self._ensure_log_file()
        self._load_history_into_graph()

# -------- UI SETUP --------
    def _build_widgets(self):
        title = tk.Label(
            self, text="📊 Smart Mobile Network Analyzer",
            font=("Segoe UI", 18, "bold"), bg="#f4f6f8", fg="#1a1a1a"
        )
        title.pack(pady=(15, 5))

        self.info_label = tk.Label(
            self, text="Click below to measure your current network quality.",
            font=("Segoe UI", 10), bg="#f4f6f8", fg="#555"
        )
        self.info_label.pack(pady=(0, 10))

        self.analyze_btn = tk.Button(
            self, text="Analyze Network", font=("Segoe UI", 11, "bold"),
            bg="#1565c0", fg="white", padx=20, pady=8,
            command=self.start_analysis
        )
        self.analyze_btn.pack(pady=5)

        self.progress = ttk.Progressbar(self, mode="indeterminate", length=300)
        self.progress.pack(pady=5)

        # Results frame
        results_frame = tk.Frame(self, bg="white", bd=1, relief="solid")
        results_frame.pack(pady=10, padx=20, fill="x")

        self.result_vars = {
            "ip": tk.StringVar(value="IP Address: -"),
            "iface": tk.StringVar(value="Connection Type: -"),
            "ping": tk.StringVar(value="Ping: -"),
            "jitter": tk.StringVar(value="Jitter: -"),
            "download": tk.StringVar(value="Download: -"),
            "upload": tk.StringVar(value="Upload: -"),
        }
        
        for key in ["ip", "iface", "ping", "jitter", "download", "upload"]:
            tk.Label(results_frame, textvariable=self.result_vars[key],
                     font=("Segoe UI", 10), bg="white", anchor="w"
                     ).pack(fill="x", padx=15, pady=3)

        # Quality badge
        self.quality_label = tk.Label(
            self, text="Quality: -", font=("Segoe UI", 14, "bold"),
            bg="#f4f6f8", fg="#333"
        )
        self.quality_label.pack(pady=(10, 5))

        # Tips box
        self.tips_box = tk.Text(self, height=5, width=68, font=("Segoe UI", 9),
                                wrap="word", bg="#fffde7", relief="flat")
        self.tips_box.pack(pady=5, padx=20)
        self.tips_box.insert("1.0", "Recommendations will appear here.")
        self.tips_box.config(state="disabled")
        
        # Graph
        self.fig = Figure(figsize=(5.8, 2.2), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Score History", fontsize=9)
        self.ax.set_ylim(0, 100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(pady=10)

# --------
    def _ensure_log_file(self):
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "ping_ms", "jitter_ms",
                                 "download_mbps", "upload_mbps", "score", "quality"])

    def _log_result(self, ping, jitter, download, upload, score, quality):
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.datetime.now().isoformat(timespec="seconds"),
                ping, jitter, download, upload, score, quality
            ])

    def _load_history_into_graph(self):
        scores = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        scores.append(float(row["score"]))
                    except (ValueError, KeyError):
                        pass
        self._plot_scores(scores)

    def _plot_scores(self, scores):
        self.ax.clear()
        self.ax.set_ylim(0, 100)
        self.ax.set_title("Score History", fontsize=9)
        if scores:
            self.ax.plot(scores[-20:], marker="o", color="#1565c0")
        self.canvas.draw()

# -------- ANALYSIS --------
    def start_analysis(self):
        self.analyze_btn.config(state="disabled")
        self.progress.start(10)
        self.info_label.config(text="Measuring network... this can take ~15-30 seconds.")
        threading.Thread(target=self._run_analysis, daemon=True).start()

    def _run_analysis(self):
        ip = network_utils.get_local_ip()
        iface = network_utils.get_active_interface()
        ping_ms, jitter_ms = network_utils.ping_host()
        speed = network_utils.run_speedtest()

        download = speed["download_mbps"] if speed else 0.0
        upload = speed["upload_mbps"] if speed else 0.0
        
        # Prefer speedtest's own ping if the manual ping failed
        if ping_ms is None and speed:
            ping_ms = speed["ping_ms"]
            jitter_ms = 0.0
            
        result = analyzer.analyze(ping_ms, jitter_ms or 0.0, download, upload)

        self.after(0, self._display_results, ip, iface, ping_ms, jitter_ms,
                   download, upload, result)

    def _display_results(self, ip, iface, ping_ms, jitter_ms, download, upload, result):
        self.progress.stop()
        self.analyze_btn.config(state="normal")
        self.info_label.config(text="Click below to measure your current network quality.")

        self.result_vars["ip"].set(f"IP Address: {ip}")
        self.result_vars["iface"].set(f"Connection Type: {iface}")
        self.result_vars["ping"].set(f"Ping: {ping_ms if ping_ms is not None else 'N/A'} ms")
        self.result_vars["jitter"].set(f"Jitter: {jitter_ms if jitter_ms is not None else 'N/A'} ms")
        self.result_vars["download"].set(f"Download: {download} Mbps")
        self.result_vars["upload"].set(f"Upload: {upload} Mbps")

        quality = result["quality"]
        color = QUALITY_COLORS.get(quality, "#333")
        self.quality_label.config(
            text=f"Quality: {quality} (Score: {result['score']}/100)", fg=color
        )

        self.tips_box.config(state="normal")
        self.tips_box.delete("1.0", "end")
        self.tips_box.insert("1.0", "\n".join(f"• {t}" for t in result["tips"]))
        self.tips_box.config(state="disabled")

        if quality != "Unknown":
            self._log_result(ping_ms, jitter_ms, download, upload,
                             result["score"], quality)
            self._load_history_into_graph()
        else:
            messagebox.showwarning("Network Analyzer",
                                   "Could not complete the test. Check your internet connection.")

if __name__ == "__main__":
    app = NetworkAnalyzerApp()
    app.mainloop()
