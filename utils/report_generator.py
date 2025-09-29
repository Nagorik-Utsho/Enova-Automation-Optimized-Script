import csv
from datetime import datetime

def generate_csv_report(report, vpn_name="Enova VPN", protocol):
    # Current date and time
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %I:%M %p")  # Full date & 12-hour time

    filename = f"{vpn_name.replace(' ', '_')}_{protocol}_Report_{now.strftime('%Y%m%d_%I%M%p')}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Header row
        writer.writerow([f"VPN Name: {vpn_name}", f"Protocol: {protocol}", f"Test Date & Time: {date_str}"])
        writer.writerow([])  # Empty row for spacing

        # Table header
        writer.writerow(["Server", "Step", "Status", "Symbol", "Message"])

        # Table rows
        for server_key in report:
            server = report[server_key]["name"]
            for step, res in report[server_key].items():
                if step == "name":
                    continue
                status = res.get("status", "UNKNOWN")
                message = res.get("message", "")
                symbol = "✅" if status == "SUCCESS" else "❌"
                writer.writerow([server, step, status, symbol, message])

    print(f"✅ Report generated: {filename}")
