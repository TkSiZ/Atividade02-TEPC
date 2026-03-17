import argparse
import logging
import os
import time

from dotenv import load_dotenv
import questionary
import tftpy
from tqdm import tqdm


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

class ProgressBar:
    def __init__(self):
        self.pbar = None

    def hook(self, pkt):
        if self.pbar is None:
            self.pbar = tqdm(
                total=pkt.totalsize,
                unit="B",
                unit_scale=True,
                desc="Transfer"
            )

        self.pbar.update(len(pkt.data))

        if pkt.blocknumber * 512 >= pkt.totalsize:
            self.pbar.close()

def tftp_client():
    if not SERVER_IP:
        print("Error: SERVER_IP not found in .env")
        return

    client = tftpy.TftpClient(SERVER_IP, SERVER_PORT)
    logger.info(f"Connected to TFTP Server {SERVER_IP}:{SERVER_PORT}")

    while True:
        choice = questionary.select(
            "What do you want to do?",
            choices=["Download file", "Upload file", "Exit"],
        ).ask()

        if choice == "Download file":
            remote = questionary.text("Remote filename:").ask()
            local = questionary.text("Local filename:").ask()

            logger.info(f"Download requested: {remote} -> {local}")

            progress = ProgressBar()
            start = time.time()

            try:
                client.download(remote, local, packethook=progress.hook)

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
            progress = ProgressBar()
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


def tftp_server():
    dir_name = "tftpboot"
    tftp_root_dir = os.path.abspath(dir_name)

    os.makedirs(tftp_root_dir, exist_ok=True)

    logger.info(f"TFTP root directory: {tftp_root_dir}")

    print("TFTP root:", tftp_root_dir)

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