import argparse 
import os
from dotenv import load_dotenv
import tftpy
import questionary

load_dotenv()
SERVER_IP = os.getenv("SERVER_IP")
SERVER_BIND = os.getenv("SERVER_BIND")

def tftp_client():
    client = tftpy.TftpClient(SERVER_IP, 69)

    while True:
        choice = questionary.select(
            "What do you want to do?",
            choices=[
                'Download file',
                'Upload file',
                'Exit'
            ]
        ).ask()

        if choice == 'Download file':
            remote_filename = questionary.text("Enter filename to download: ").ask()
            local_filename = questionary.text("Enter local filename to save: ").ask()

            try:
                client.download(remote_filename, local_filename)
                print("Download completed!\n")
                print("-=-"*30)
            except Exception as e:
                print(f"Download failed: {e}\n")
                print("-=-"*30)

        elif choice == 'Upload file':
            remote_filename = questionary.text("Enter remote filename: ").ask()
            local_filename = questionary.text("Enter local filename to upload: ").ask()

            try:
                client.upload(remote_filename, local_filename)
                print("Upload completed!\n")
                print("-=-"*30)
            except Exception as e:
                print(f"Upload failed: {e}\n")

        elif choice == 'Exit':
            print("Closing the Client!")
            break


def tftp_server():
    dir_name = "tftpboot"
    tftproot_dir = os.path.join(os.getcwd(), dir_name)
    os.makedirs(tftproot_dir, exist_ok=True)

    server = tftpy.TftpServer(tftproot=tftproot_dir)
    print('Servidor inicializado!')
    server.listen(SERVER_BIND, 69)
    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--client", help= "Initializing TFTP Client", action="store_true")
    group.add_argument("--server", help= "Initializing TFTP Server", action="store_true")

    args = parser.parse_args()
    
    if args.client:
        print("Instanciando um TFTP Client")
        tftp_client()
    
    elif args.server:
        print("Instanciando um TFTP Server")
        tftp_server()
    
    else: 
        print("Please choose to instantiate a TFTP server or client.")
