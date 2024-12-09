# Elasticsearch Backup & Restore Tool

This repository provides a simple Dockerized Python tool to create and restore Elasticsearch snapshots. It can be used with a local Elasticsearch instance, a Dockerized Elasticsearch, or any reachable Elasticsearch service. The script does not rely on any proprietary or product-specific configurations, making it generally usable in diverse environments.

## Features

- **Backup Elasticsearch indices** to a file system repository.
- **Restore Elasticsearch indices** from a snapshot repository.
- **Dockerized**: No need to install Python, `requests`, or other dependencies on your machine.
- **Configurable**: Control Elasticsearch endpoint, repository name, snapshot name, indices, and snapshot directory via command-line flags.

## Requirements

- Docker installed on your system.
- Access to an Elasticsearch instance (local, remote, or dockerized) that is reachable from inside the Docker container.
- A directory on the host machine to store snapshots, mounted into the container at `/var/tmp`.

## Building the Docker Image

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

2. Build the Docker image:
   ```bash
   docker build -t es-backup-restore:latest .

## Usage

Run the container with the desired arguments. The script supports various parameters. Run `--help` to see all options:

```bash
docker run --rm es-backup-restore:latest --help

# Common Flags

This guide provides details on the common flags available for configuring and managing Elasticsearch backups and restores.

## Flags

### `--mode [local|docker]`
Defines the operation mode for the script.

- **`local`**: Use for a local Elasticsearch instance running outside of containers on `localhost` (or any given IP).
- **`docker`**: Use for a Dockerized Elasticsearch instance, or if you prefer a neutral mode.

---

### `--es_ip <IP>`
Specifies the Elasticsearch IP or hostname.

- **Default**: `localhost`

---

### `--repo_name <repo_name>`
The name of the snapshot repository.

- **Default**: `my_test_repo`

---

### `--snapshot_name <snapshot_name>`
The name of the snapshot.

- **Default**: `test_snapshot`

---

### `--snapshot_dir <path>`
Directory for storing snapshots.

- **Default**: `/var/tmp`

---

### `--backup`
Enables the steps to perform a backup.

---

### `--restore`
Enables the steps to perform a restore.

---

### `--indices <indices>`
Specifies the indices to backup or restore.

- **Default**: `*` (all indices)

---

### `--include_global_state`
Includes the global state in the snapshot or restore process.

- **Default**: `false`

---

### `--verify_repo`
Verifies the snapshot repository after creation or before performing a restore.

---

### `--skip_verify`
Skips verification steps for snapshots.

---

# Backup Example

This example demonstrates how to perform a backup with Elasticsearch.

## Assumptions

- You have a running Elasticsearch instance accessible at `localhost:9200`.
- You want to save the snapshot to `/host/local/snapshot` on your machine.

## Command

```bash
docker run --rm \
  -v /host/local/snapshot:/var/tmp \
  es-backup-restore:latest \
  --mode local \
  --es_ip localhost \
  --repo_name my_snapshot_repo \
  --snapshot_name my_snapshot \
  --backup


# Restore Example

This example demonstrates how to restore a snapshot with Elasticsearch.

## Assumptions

- The snapshot files have been transferred to `/host/local/snapshot` on your new machine.
- Elasticsearch is running at `localhost:9200` on the restore machine.
- Permissions are correctly set for `/host/local/snapshot`.

## Command

```bash
docker run --rm \
  -v /host/local/snapshot:/var/tmp \
  es-backup-restore:latest \
  --mode local \
  --es_ip localhost \
  --repo_name my_snapshot_repo \
  --snapshot_name my_snapshot \
  --restore

