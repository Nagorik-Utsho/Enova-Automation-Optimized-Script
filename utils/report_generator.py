import csv
from datetime import datetime



def generate_csv_report(report, vpn_name="Enova VPN", protocol=''):

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %I:%M %p")
    filename = f"{vpn_name.replace(' ', '_')}_{protocol}_Report_{now.strftime('%Y%m%d_%I%M%p')}.csv"

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Main header
        writer.writerow([f"VPN Name: {vpn_name}", f"Protocol: {protocol}", f"Test Date & Time: {date_str}"])
        writer.writerow([])  # spacing
        writer.writerow(["Server/Test", "Step", "Status", "Symbol", "Message"])
        writer.writerow([])

        # Write rows for all tests
        for test_name, servers in report.items():
            # Print the test name as a single row before its steps
            writer.writerow([f"Test Name = {test_name}"])
            writer.writerow([])  # optional spacing

            for server_key in servers:
                server = servers[server_key].get("name", server_key)
                for step, res in servers[server_key].items():
                    if step == "name":
                        continue
                    status = res.get("status", "UNKNOWN")
                    message = res.get("message", "")
                    symbol = "✅" if status == "SUCCESS" else "❌"
                    writer.writerow([server, step, status, symbol, message])

            # Add extra spacing after each test
            writer.writerow([])
            writer.writerow([])

    print(f"✅ Combined report generated: {filename}")




