# main.py
import argparse
import json
import logging
from network_inventory_collector.config import MAX_WORKERS
from concurrent.futures import ThreadPoolExecutor, as_completed
from network_inventory_collector.collector import collect_from_host
from network_inventory_collector.utils import load_hosts, load_credentials, setup_logger

def main():
    parser = argparse.ArgumentParser(description="Remote Network Inventory Collector")
    parser.add_argument("--hosts", required=True, help="Path to hosts.txt")
    parser.add_argument("--credentials", required=True, help="Path to credentials.txt")
    parser.add_argument("--output", help="Optional output file (JSON)")
    parser.add_argument("--interface-filter", help="Optional filter for interface names (comma-separated, e.g. eth,ens)")
    args = parser.parse_args()

    setup_logger()
    hosts = load_hosts(args.hosts)
    credentials = load_credentials(args.credentials)
    interface_filters = args.interface_filter.split(",") if args.interface_filter else None

    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(collect_from_host, host, credentials, interface_filters): host for host in hosts}
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)

    print(json.dumps(results, indent=2))
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
