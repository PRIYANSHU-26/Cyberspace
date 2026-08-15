import network_utils
import analyzer

def main():
    print("=" * 55)
    print(" SMART MOBILE NETWORK ANALYZER (CLI)")
    print("=" * 55)

    ip = network_utils.get_local_ip()
    iface = network_utils.get_active_interface()
    print(f"\nLocal IP Address  : {ip}")
    print(f"Connection Type   : {iface}")

    print("\nPinging 8.8.8.8 ...")
    ping_ms, jitter_ms = network_utils.ping_host()
    print(f"Ping              : {ping_ms} ms" if ping_ms else "Ping failed")
    print(f"Jitter            : {jitter_ms} ms" if jitter_ms is not None else "")

    print("\nRunning speed test (this may take 15-30 seconds)...")
    speed = network_utils.run_speedtest()

    if speed:
        download = speed["download_mbps"]
        upload = speed["upload_mbps"]
        if ping_ms is None:
            ping_ms = speed["ping_ms"]
            jitter_ms = 0.0
        print(f"Download Speed    : {download} Mbps")
        print(f"Upload Speed      : {upload} Mbps")
    else:
        download = upload = 0.0
        print("Speed test failed. Check your internet connection.")

    result = analyzer.analyze(ping_ms, jitter_ms or 0.0, download, upload)

    print("\n" + "-" * 55)
    print(f" NETWORK SCORE   : {result['score']} / 100")
    print(f" NETWORK QUALITY : {result['quality']}")
    print("-" * 55)
    print(" Recommendations:")
    for tip in result["tips"]:
        print(f"   • {tip}")
    print("=" * 55)


if __name__ == "__main__":
    main()
