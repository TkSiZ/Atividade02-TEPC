import argparse
import os
from dotenv import load_dotenv
import tftpy
import questionary
import logging

load_dotenv()

logging.basicConfig(level=logging.DEBUG)

SERVER_IP = os.getenv("SERVER_IP")
SERVER_BIND = os.getenv("SERVER_BIND", "0.0.0.0")

def tftp_client():
    if not SERVER_IP:
        print("Error: SERVER_IP not found in .env")
        return
    client = tftpy.TftpClient(SERVER_IP, 69)
    while True:
        choice = questionary.select("What do you want to do?", choices=['Download file', 'Upload file', 'Exit']).ask()
        if choice == 'Download file':
            remote = questionary.text("Remote filename:").ask()
            local = questionary.text("Local filename:").ask()
            try:
                client.download(remote, local)
                print("Download Success")
            except Exception as e:
                print(f"Error: {e}")
        elif choice == 'Upload file':
            remote_filename = questionary.text("Remote filename:").ask()
            local_filename = questionary.text("Enter local filename to upload: ").ask()
            local_path = os.path.abspath(local_filename.strip().replace('"', ''))

            if not os.path.isfile(local_path):
                print(f"File not found {local_path}")
                continue
            try:
                with open(local_path,'rb') as f:
                    client.upload(remote_filename, f)
                print("Upload Finished")
            except Exception as e:
                print(f"Upload failed: {e}\n")
        elif choice == 'Exit':
            print("Closing the Client!")
            break
            

def tftp_server():
    dir_name = "tftpboot"
    tftproot_dir = os.path.abspath(dir_name)
    os.makedirs(tftproot_dir, exist_ok=True)
    print("TFTP root:", tftproot_dir)
    server = tftpy.TftpServer(tftproot=tftproot_dir)
    
    try:
        server.listen(SERVER_BIND, 69)
    except Exception as e:
        print(f"Server Error: {e}")
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