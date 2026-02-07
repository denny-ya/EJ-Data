import certifi
import shutil
import os

# Get standard cert path
cert_path = certifi.where()
print(f"Original Cert Path: {cert_path}")

# Copy to current working directory (safe from special chars in absolute path if we use relative)
dest_path = "cacert.pem"
shutil.copy(cert_path, dest_path)
print(f"Copied to: {os.path.abspath(dest_path)}")
