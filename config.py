import socket
import os

def get_local_ip():
    """
    Finds the local IP address of the machine.
    """
    s = None
    try:
        # Create a temporary socket to an external IP (doesn't send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
    except socket.error:
        local_ip = None
    finally:
        if s:
            s.close()
    return local_ip

def create_files(ip_adress):
    specs = "SERVER_IP=" + ip_address + "\n" + "SERVER_BIND=0.0.0.0"
    with open(".env", "w") as obj_file:
        obj_file.write(specs)
    
    try:
        os.mkdir("tftpboot")
    except:
        pass


# Example usage:
ip_address = get_local_ip()
print(f"Your Local IP Address is: {ip_address}")
create_files(ip_address)

