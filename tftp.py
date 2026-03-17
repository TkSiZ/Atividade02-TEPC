import argparse
import logging
import os
import time
import threading

from dotenv import load_dotenv
import questionary
import tftpy


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("tftp.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

SERVER_IP = os.getenv("SERVER_IP")
SERVER_BIND = os.getenv("SERVER_BIND", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", 69))


def tftp_client():
    if not SERVER_IP:
        print("Error: SERVER_IP not found in .env")
        return

    client = tftpy.TftpClient(SERVER_IP, SERVER_PORT)
    logger.info(f"Connected to TFTP Server {SERVER_IP}:{SERVER_PORT}")

    while True:
        choice = questionary.select(
            "What do you want to do?",
            choices=["List files", "Download file", "Upload file", "Exit"],
        ).ask()
        
        if choice == "List files":
            logger.info("Listing remote files via index.txt...")
            temp_index = "temp_index.txt"

            try:
                client.download("index.txt", temp_index)
                print("\n---Available files---")

                with open(temp_index, "r") as f:
                    files = f.read()
                    print(files if files.strip() else "(Server empty)")
                
                print("-----------------\n")

                os.remove(temp_index)
            except Exception as error:
                logger.error(f"Files listing error: {error}")
                print(f"Error {error}")

        elif choice == "Download file":
            remote = questionary.text("Remote filename:").ask()
            local = questionary.text("Local filename:").ask()

            logger.info(f"Download requested: {remote} -> {local}")

            start = time.time()

            try:
                client.download(remote, local)

                elapsed = time.time() - start
                size = os.path.getsize(local)
                speed = size / elapsed / 1024

                logger.info(f"Download finished in {elapsed:.2f}s ({speed:.2f} KB/s)")
                print("Download Success")

            except Exception as error:
                logger.error(f"Download failed: {error}")
                print(f"Error: {error}")

        elif choice == "Upload file":
            remote_filename = questionary.text("Remote filename:").ask()
            local_filename = questionary.text(
                "Enter local filename to upload:"
            ).ask()

            local_path = os.path.abspath(
                local_filename.strip().replace('"', "")
            )

            if not os.path.isfile(local_path):
                logger.warning(f"File not found: {local_path}")
                print(f"File not found {local_path}")
                continue

            logger.info(f"Upload requested: {local_path} -> {remote_filename}")
            
            start = time.time()

            try:
                client.upload(remote_filename, local_path)

                elapsed = time.time() - start
                size = os.path.getsize(local_path)
                speed = size / elapsed / 1024

                logger.info(f"Upload finished in {elapsed:.2f}s ({speed:.2f} KB/s)")
                print("Upload Finished")

            except Exception as error:
                logger.error(f"Upload failed: {error}")
                print(f"Upload failed: {error}\n")

        elif choice == "Exit":
            logger.info("Client closed")
            print("Closing the Client!")
            break


def update_index_file(tftp_root_dir):
    index_path = os.path.join(tftp_root_dir, "index.txt")

    while True:
        try:
            files = os.listdir(tftp_root_dir)

            if "index.txt" in files:
                files.remove("index.txt")
            
            with open(index_path, "w") as f:
                for file_name in files:
                    f.write(f"{file_name}\n")
        except Exception as error:
            logger.error(f"Failed to update index file: {error}")
        
        time.sleep(5)

def tftp_server():
    dir_name = "tftpboot"
    tftp_root_dir = os.path.abspath(dir_name)

    os.makedirs(tftp_root_dir, exist_ok=True)

    logger.info(f"TFTP root directory: {tftp_root_dir}")

    print("TFTP root:", tftp_root_dir)

    index_thread = threading.Thread(target=update_index_file, args=(tftp_root_dir,), daemon=True)
    index_thread.start()

    server = tftpy.TftpServer(tftproot=tftp_root_dir)

    try:
        logger.info(f"Starting TFTP server on {SERVER_BIND}:{SERVER_PORT}")
        server.listen(SERVER_BIND, SERVER_PORT)
    except Exception as error:
        logger.error(f"Server Error: {error}")
        print(f"Server Error: {error}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--client", action="store_true")
    group.add_argument("--server", action="store_true")

    args = parser.parse_args()

    if args.client:
        tftp_client()
    elif args.server:
        tftp_server()