# Imports
import os, paramiko, time, pystyle, dhooks, json, glob, shutil
from pystyle import Colors, Colorate, Center
from dhooks import Webhook

# Variables
scriptDir = os.getcwd() # Getting the script directory
clear = lambda: os.system("cls" if os.name in ("nt", "dos") else "clear") # Don't touch this
count = 0 # Don't touch this
clear()

# List of your vps, you can add and remove lines with the same format, watch out that last line doesn't have a (,) at the end.
vps_list = [
    {"ip": "", "username": "", "password": ""},
    {"ip": "", "username": "", "password": ""},
    {"ip": "", "username": "", "password": ""},
    {"ip": "", "username": "", "password": ""}
]

# Logo
logo = """
██╗███╗░░██╗██╗░░░██╗██╗████████╗███████╗  ██████╗░░█████╗░░█████╗░██╗░░██╗██╗░░░██╗██████╗░██████╗░
██║████╗░██║██║░░░██║██║╚══██╔══╝██╔════╝  ██╔══██╗██╔══██╗██╔══██╗██║░██╔╝██║░░░██║██╔══██╗██╔══██╗
██║██╔██╗██║╚██╗░██╔╝██║░░░██║░░░█████╗░░  ██████╦╝███████║██║░░╚═╝█████═╝░██║░░░██║██████╔╝██████╔╝
██║██║╚████║░╚████╔╝░██║░░░██║░░░██╔══╝░░  ██╔══██╗██╔══██║██║░░██╗██╔═██╗░██║░░░██║██╔═══╝░██╔══██╗
██║██║░╚███║░░╚██╔╝░░██║░░░██║░░░███████╗  ██████╦╝██║░░██║╚█████╔╝██║░╚██╗╚██████╔╝██║░░░░░██║░░██║
╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚═╝░░░╚═╝░░░╚══════╝  ╚═════╝░╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░╚═════╝░╚═╝░░░░░╚═╝░░╚═╝"""

# Prints the logo
def printLogo():
        print(Center.XCenter(Colorate.Horizontal(Colors.white_to_blue, logo, 1)))
        
# Download the invites
def downloadInvs():
    global count
    
    for vps in vps_list:
        count += 1
        ip = vps["ip"]
        username = vps["username"]
        password = vps["password"]
        # Checks if folder/files exist
        try:
            if not os.path.exists("invites"):
                print(Center.XCenter(Colorate.Horizontal(Colors.white_to_red, f"\nInvites text file {count} doesn't exist! Creating one.", 1)))
                os.mkdir("invites")
            else:
                print(Center.XCenter(Colorate.Horizontal(Colors.white_to_green, f"\nInvites folder exists!", 1)))
            if not os.path.exists(f"invites/invites{count}.txt"):
                print(Center.XCenter(Colorate.Horizontal(Colors.white_to_red, f"\nInvites text file {count} doesn't exist! Creating one.", 1)))
                with open(f"{scriptDir}/invites/invites{count}.txt", "w") as f:
                    f.write("")
            else:
                print(Center.XCenter(Colorate.Horizontal(Colors.white_to_green, f"\nInvites text file {count} exists!", 1)))
            time.sleep(1)
            # Get the invites to local
            print(Center.XCenter(Colorate.Horizontal(Colors.white_to_blue, f"\nStarting download of vps {count} invites...", 1)))
            vps = paramiko.SSHClient()
            vps.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            vpsTransport = paramiko.Transport((ip, 22))
            vpsTransport.connect(username=username, password=password)
            vpsSFTP = paramiko.SFTPClient.from_transport(vpsTransport)
            vpsSFTP.get('/root/invites.txt', f'{scriptDir}/invites/invites{count}.txt')
            # Makes a new file on each vps so you don't need to
            print(Center.XCenter(Colorate.Horizontal(Colors.white_to_blue, f"\nResetting invites.txt of vps {count}...", 1)))
            file = vpsSFTP.open("/root/invites.txt", "w", bufsize = -1)
            file.write(" ")
            file.close()
            print(Center.XCenter(Colorate.Horizontal(Colors.white_to_green, f"\nResetting invites.txt of vps {count} done!", 1)))
            vpsSFTP.close()
            vpsTransport.close()
            print(Center.XCenter(Colorate.Horizontal(Colors.white_to_green, f"Download of vps {count} invites completed!\n", 1)))
        except Exception as e:
            print(Center.XCenter(Colorate.Horizontal(Colors.white_to_red, "\nFailed! Error: " + str(e) + "\n", 1)))
            input(Center.XCenter(Colorate.Horizontal(Colors.white_to_blue, "\nPress any key to continue.\n", 1)))
            pass

# Start the tool
printLogo()
print(Center.XCenter(Colorate.Horizontal(Colors.white_to_green, "\nStarting download of all vps invites...", 1)))
downloadInvs()
print(Center.XCenter(Colorate.Horizontal(Colors.white_to_green, "\nDownload of all vps invites completed! Concatenating...\n", 1)))
time.sleep(1)
# Concatenate all the invites in only one txt
try:
    os.chdir(f"{scriptDir}/invites")
    outfilename = "invites.txt"

    filenames = glob.glob('*.txt')

    with open(outfilename, 'wb') as outfile:
        for filename in glob.glob('*.txt'):
            if filename == outfilename:
                continue
            with open(filename, 'rb') as readfile:
                shutil.copyfileobj(readfile, outfile)
except Exception as e:
            print(Center.XCenter(Colorate.Horizontal(Colors.white_to_red, "\nFailed! Error: " + str(e) + "\n", 1)))
            input(Center.XCenter(Colorate.Horizontal(Colors.white_to_blue, "\nPress any key to continue.\n", 1)))
            pass
print(Center.XCenter(Colorate.Horizontal(Colors.white_to_green, "\nDone concatenating!...\n", 1)))
time.sleep(1)
print(Center.XCenter(Colorate.Horizontal(Colors.white_to_green, "\nFinished! Exiting...\n", 1)))
time.sleep(1)
exit()