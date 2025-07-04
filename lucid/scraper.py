import requests
import os
import time
import glob
import re

# Base URL for the PDFs from Lucid Motors' investor relations site
BASE_URL = "https://ir.lucidmotors.com/node/{}/pdf"

# Directory where the downloaded PDFs will be saved
OUTPUT_DIR = "lucid_pdfs"

# Range of node numbers to iterate through
START_NODE = 5200
END_NODE = 9999

def download_lucid_pdfs():
    """
    Iterates through a range of node IDs to find and download PDF files
    from the Lucid Motors investor relations website. The script can be
    restarted and will resume from where it left off.
    """
    # Create the output directory if it doesn't already exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"PDFs will be saved in '{OUTPUT_DIR}' directory.")

    # Scan for existing downloads to determine where to resume
    print("Scanning for existing PDFs to determine resume point...")
    existing_files = glob.glob(os.path.join(OUTPUT_DIR, "lucid_node_*.pdf"))
    successful_nodes = set()
    for f in existing_files:
        match = re.search(r'lucid_node_(\d+)\.pdf$', f)
        if match:
            successful_nodes.add(int(match.group(1)))

    if successful_nodes:
        last_downloaded = max(successful_nodes)
        start_from = max(START_NODE, last_downloaded + 1)
        print(f"Found {len(successful_nodes)} existing PDFs. Resuming scan from node {start_from}.")
    else:
        start_from = START_NODE
        print("No existing PDFs found. Starting PDF scan from the beginning.")

    if start_from > END_NODE:
        print(f"All nodes up to {END_NODE} have been checked. Process will now complete.")

    # Use a session for connection pooling
    with requests.Session() as session:
        for node_id in range(start_from, END_NODE + 1):
            url = BASE_URL.format(node_id)
            file_path = os.path.join(OUTPUT_DIR, f"lucid_node_{node_id}.pdf")

            # This check is a safeguard; the loop should start after existing files.
            if os.path.exists(file_path):
                print(f"Node {node_id}: PDF already exists. Adding to list and skipping.")
                successful_nodes.add(node_id)
                continue

            try:
                print(f"Requesting {url}...")
                response = session.get(url, timeout=15, stream=True)

                if response.status_code == 200 and 'application/pdf' in response.headers.get('Content-Type', ''):
                    successful_nodes.add(node_id)
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Successfully downloaded and saved: {file_path}")
                else:
                    print(f"Node {node_id} did not return a PDF. Status: {response.status_code}")

            except requests.exceptions.RequestException as e:
                print(f"An error occurred for node {node_id}: {e}")

            # A short delay to be respectful to the server
            time.sleep(0.1)

    print("\nDownload process has completed.")

    if successful_nodes:
        sorted_nodes = sorted(list(successful_nodes))
        print(f"\nFound {len(sorted_nodes)} PDF files in total.")
        print(f"Successful node IDs: {sorted_nodes}")

        nodes_file_path = os.path.join(OUTPUT_DIR, "successful_nodes.txt")
        with open(nodes_file_path, 'w') as f:
            for node in sorted_nodes:
                f.write(f"{node}\n")
        print(f"List of successful node IDs saved to '{nodes_file_path}'")
    else:
        print("\nNo PDF files were found in the specified node range.")

if __name__ == "__main__":
    download_lucid_pdfs()