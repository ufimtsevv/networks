import csv
import argparse

from pythonping import ping

def read_domains(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file if line.strip()]

def get_rtts(domains):
    rtts = []
    for domain in domains:
        try:
            response = ping(domain, count=4)
            rtts.append(response.rtt_avg_ms)
        except Exception as e:
            print(f"error pinging domain {domain}: {e}")
            rtts.append(None)
    return rtts

def save_results(domains, rtts, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["domain", "RTT (ms)"])
        for domain, rtt in zip(domains, rtts):
            writer.writerow([domain, rtt if rtt is not None else "N/A"])

def main():
    parser = argparse.ArgumentParser(description="use: main.py <domains.txt> <result.csv>")
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()

    domains = read_domains(args.input)

    rtts = get_rtts(domains)

    save_results(domains, rtts, args.output)
    print(f"results saved to: {args.output}")

if __name__ == "__main__":
    main()