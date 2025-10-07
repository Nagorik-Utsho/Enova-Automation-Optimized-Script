import csv
from datetime import datetime
import os


def generate_csv_report(report, vpn_name='', protocol='', test_name=''):
    """
    Generates or appends to a CSV automation report.

    Args:
        report (dict): Dictionary containing server/test results.
        vpn_name (str): Optional VPN name (default blank).
        protocol (str): Optional protocol name (default blank).
        test_name (str): Optional test name (default blank).
    """
    # Current date and time
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d %I:%M %p")  # Full date & 12-hour time

    # CSV filename (one file per protocol, append if exists)
    filename = f"{vpn_name.replace(' ', '_')}_{protocol}_Report.csv" if vpn_name or protocol else "Automation_Report.csv"

    # Check if file exists to determine mode
    file_exists = os.path.isfile(filename)
    mode = "a" if file_exists else "w"

    with open(filename, mode, newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Add 3-4 empty lines before new section
        if file_exists:
            writer.writerow([])
            writer.writerow([])
            writer.writerow([])

        # Header row for this test type
        writer.writerow([f"VPN Name: {vpn_name}", f"Test Name: {test_name}", f"Protocol: {protocol}",
                         f"Report Generated: {date_str}"])
        writer.writerow([])  # Empty row for spacing

        # Table header for validation test cases
        writer.writerow(["Server", "Step", "Status", "Symbol", "Message"])

        # Table rows
        for server_key in report:
            server = report[server_key].get("name", "")
            for step, res in report[server_key].items():
                if step == "name":
                    continue
                status = res.get("status", "UNKNOWN")
                message = res.get("message", "")
                symbol = "✅" if status in ["Passed", "SUCCESS"] else "❌"
                writer.writerow([server, step, status, symbol, message])

    print(f"✅ Report generated/updated: {filename}")
