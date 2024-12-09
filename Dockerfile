FROM python:3.11-slim

# Install Python dependencies
RUN pip install requests

# Copy the script into the container
COPY es_backup_restore.py /usr/local/bin/es_backup_restore.py
RUN chmod +x /usr/local/bin/es_backup_restore.py

WORKDIR /var/tmp
ENTRYPOINT ["python", "/usr/local/bin/es_backup_restore.py"]

