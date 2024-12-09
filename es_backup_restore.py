import argparse
import sys
import time
import requests
from requests.exceptions import RequestException

def create_snapshot_repo(es_ip, repo_name, snapshot_dir):
    url = f"http://{es_ip}:9200/_snapshot/{repo_name}"
    payload = {
        "type": "fs",
        "settings": {
            "location": snapshot_dir,
            "compress": True
        }
    }
    resp = requests.put(url, json=payload)
    if resp.status_code not in [200, 201]:
        print("Failed to create snapshot repository:", resp.text)
        sys.exit(1)
    print("Snapshot repository created:", repo_name)

def verify_repo(es_ip, repo_name):
    url = f"http://{es_ip}:9200/_snapshot/{repo_name}/_all?pretty"
    resp = requests.get(url)
    if resp.status_code == 200:
        print("Repository verification:\n", resp.text)
    else:
        print("Failed to verify repository:", resp.text)

def create_snapshot(es_ip, repo_name, snapshot_name, indices="*", include_global_state=False):
    url = f"http://{es_ip}:9200/_snapshot/{repo_name}/{snapshot_name}"
    payload = {
        "indices": indices,
        "ignore_unavailable": True,
        "include_global_state": include_global_state
    }
    resp = requests.put(url, json=payload)
    if resp.status_code not in [200, 201]:
        print("Failed to create snapshot:", resp.text)
        sys.exit(1)
    print("Snapshot created:", snapshot_name)

def verify_snapshot(es_ip, repo_name, snapshot_name):
    url = f"http://{es_ip}:9200/_snapshot/{repo_name}/{snapshot_name}?pretty"
    resp = requests.get(url)
    if resp.status_code == 200:
        print("Snapshot verification:\n", resp.text)
    else:
        print("Failed to verify snapshot:", resp.text)

def restore_snapshot(es_ip, repo_name, snapshot_name, indices="*", include_global_state=True):
    url = f"http://{es_ip}:9200/_snapshot/{repo_name}/{snapshot_name}/_restore"
    payload = {
        "indices": indices,
        "ignore_unavailable": True,
        "include_global_state": include_global_state
    }
    resp = requests.post(url, json=payload)
    if resp.status_code not in [200, 201, 202]:
        print("Failed to restore snapshot:", resp.text)
        sys.exit(1)
    print("Restore started:", snapshot_name)

def monitor_restore(es_ip):
    url = f"http://{es_ip}:9200/_cat/recovery?v"
    resp = requests.get(url)
    if resp.status_code == 200:
        print("Restore progress:\n", resp.text)
    else:
        print("Failed to monitor restore:", resp.text)

def verify_indices(es_ip):
    url = f"http://{es_ip}:9200/_cat/indices?v"
    resp = requests.get(url)
    if resp.status_code == 200:
        print("Indices:\n", resp.text)
    else:
        print("Failed to list indices:", resp.text)

def check_cluster_health(es_ip):
    url = f"http://{es_ip}:9200/_cluster/health?pretty"
    resp = requests.get(url)
    if resp.status_code == 200:
        print("Cluster health:\n", resp.text)
    else:
        print("Failed to check cluster health:", resp.text)

def main():
    parser = argparse.ArgumentParser(description="Elasticsearch Backup & Restore Script")
    parser.add_argument('--mode', choices=['local','docker'], required=True, 
                        help="Mode of operation: local or docker")
    parser.add_argument('--es_ip', default='localhost', help="Elasticsearch IP or hostname. Defaults to localhost.")
    parser.add_argument('--repo_name', default='my_test_repo', help="Snapshot repository name")
    parser.add_argument('--snapshot_name', default='test_snapshot', help="Snapshot name")
    parser.add_argument('--snapshot_dir', default='/var/tmp', help="Directory where snapshots are stored")
    parser.add_argument('--backup', action='store_true', help="Perform backup steps")
    parser.add_argument('--restore', action='store_true', help="Perform restore steps")
    parser.add_argument('--indices', default='*', help="Indices to backup/restore")
    parser.add_argument('--include_global_state', action='store_true', default=False, 
                        help="Include global state in snapshot/restore")
    parser.add_argument('--verify_repo', action='store_true', help="Verify repository after creation or before restore")
    parser.add_argument('--skip_verify', action='store_true', help="Skip verification steps for snapshots")

    args = parser.parse_args()

    es_ip = args.es_ip

    if args.backup:
        print("=== BACKUP PHASE ===")
        create_snapshot_repo(es_ip, args.repo_name, args.snapshot_dir)
        if args.verify_repo:
            verify_repo(es_ip, args.repo_name)

        create_snapshot(es_ip, args.repo_name, args.snapshot_name, indices=args.indices, include_global_state=args.include_global_state)
        
        if not args.skip_verify:
            verify_snapshot(es_ip, args.repo_name, args.snapshot_name)
        
        print("Backup completed. You can now tar and transfer the snapshot data if needed.")

    if args.restore:
        print("=== RESTORE PHASE ===")
        # Ensure snapshot_dir has the snapshot data and correct permissions before running this.
        create_snapshot_repo(es_ip, args.repo_name, args.snapshot_dir)
        if args.verify_repo:
            verify_repo(es_ip, args.repo_name)

        restore_snapshot(es_ip, args.repo_name, args.snapshot_name, indices=args.indices, include_global_state=True)

        # Give some time for restore to start
        time.sleep(5)
        monitor_restore(es_ip)
        verify_indices(es_ip)
        check_cluster_health(es_ip)

        print("Restore completed.")

if __name__ == '__main__':
    main()

