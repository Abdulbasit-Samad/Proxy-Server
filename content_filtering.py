import os

def block_websites(urls):
    redirect = "127.0.0.1"

    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"  

    with open(hosts_path, 'a') as file:
        for url in urls:
            file.write("\n" + redirect + " " + url)

    os.system("ipconfig /flushdns")

def unblock_websites(urls):
   
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"  # Replace with the path to your hosts file on your operating system

    with open(hosts_path, 'r') as file:
    
        lines = file.readlines()

    with open(hosts_path, 'w') as file:
        for line in lines:
            if not any(url in line for url in urls):
                file.write(line)

    os.system("ipconfig /flushdns")  

