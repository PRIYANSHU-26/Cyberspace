import socket
import subprocess
import platform
import re
import psutil

def get_local_ip():
    """Return this machine's local IP address."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unavailable"

def get_active_interface():
    try:
        stats = psutil.net_if_stats()
        for name, stat in stats.items():
            if stat.isup and name.lower() not in ("lo", "loopback"):
                lname = name.lower()
                if "wi" in lname or "wlan" in lname or "wireless" in lname:
                    kind = "Wi-Fi"
                elif "eth" in lname:
                    kind = "Ethernet"
                elif "ppp" in lname or "mobile" in lname or "cell" in lname:
                    kind = "Mobile Data"
                else:
                    kind = "Other"
                return f"{kind} ({name})"
        return "Unknown"
    except Exception:
        return "Unknown"

def ping_host(host="8.8.8.8", count=4):
    system = platform.system().lower()
    if "windows" in system:
        cmd = ["ping", "-n", str(count), host]
    else:
        cmd = ["ping", "-c", str(count), host]

    try:
        output = subprocess.run(cmd, capture_output=True, text=True, timeout=10).stdout
    except Exception:
        return None, None

    # Extract all individual round-trip times (works for both Windows/Linux wording)
    times = [float(t) for t in re.findall(r"time[=<]([\d.]+)", output, re.IGNORECASE)]

    if not times:
        return None, None

    avg_latency = sum(times) / len(times)
    jitter = (max(times) - min(times)) if len(times) > 1 else 0.0
    return round(avg_latency, 2), round(jitter, 2)

def run_speedtest():
    try:
        import speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        download_mbps = round(st.download() / 1_000_000, 2)
        upload_mbps = round(st.upload() / 1_000_000, 2)
        ping_ms = round(st.results.ping, 2)
        return {
            "download_mbps": download_mbps,
            "upload_mbps": upload_mbps,
            "ping_ms": ping_ms,
        }
    except Exception as e:
        print(f"[network_utils] Speedtest failed: {e}")
        return None
