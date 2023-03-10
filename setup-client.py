# ------------------------------------------------------------------
# Description:  This script will install the tools necessary for
#               a user to remotely connect from their client to a
#               server using TigerVNC.  Run from the client computer
#               that you plan on using.
#
# Usage:        > python setup-client
#               > vnc-devbox
#
# Requirements: Ssh must already be setup between server and client.
#               Works on MacOSX clients.  Not tested on any other
#               OS.
#
# Author:       Destin V
# Date:         12-14-2021
# ------------------------------------------------------------------

import os

# ------------------------------------------------------------------
# FILL OUT PRIOR TO RUNNING THE SCRIPT!
# ------------------------------------------------------------------
# setup required
SERVER_USER = "ubuntu"  # default user name
SERVER_IP = "xxx.xx.xx.xx"  # the address to the server box
SERVER_LOCAL = "127.0.0.1"  # leave this as default to use localhost
CUSTOM_ALIAS = "vnc-devbox"  # the custom alias you want for connecting

# ------------------------------------------------------------------
# DO NOT MODIFY
# ------------------------------------------------------------------
SERVER_LOGIN = f"{SERVER_USER}@{SERVER_IP}"
HOME_FOLDER = os.path.expanduser("~")
TIGERVNC_VER = "1.12.0"
TIGERVNC_PORT = "5901"


def validate():
    if SERVER_IP == "xxx.xx.xx.xx":
        raise ValueError("Invalid server ip address!")


def update_file(file: str, custom_line: str) -> None:
    """Updates the specified file by adding the custom line.

    Args:
        file (str): the file to edit
        custom_line (str): The custom line to add to the file
    """

    assert file.endswith("rc"), "Error! This is not an *rc file!"

    # create the file if it does not already exist
    if ~os.path.exists(file):
        print(f"Generating a new file:\n", f"{file}")
        open(file, "a").close()

    # print notification
    print(f"Adding line to your shell config:\n", f"{custom_line}")

    # add an alias to the file
    new_line_added = False

    with open(file, "r") as f:
        lines = f.readlines()
        if custom_line not in lines:
            out = open(file, "a")
            out.write(custom_line)
            out.close()

            new_line_added = True

    if new_line_added is True:
        print(f"New line: {alias_vnc_devbox} was added to {file}")
    else:
        print(f"No changes made to {file}")


def print_intro():
    os.system("clear")
    print(
        f" ---------------------------------------------\n",
        f"\n",
        f"This script will install a Virtual Network  \n",
        f"Client (VCN) on your computer for connecting \n",
        f"           with remote servers.  \n",
        f"\n",
        f"First install the TigerVNC client from here: \n",
        f"https://github.com/TigerVNC/tigervnc/releases \n",
        f"Place the app in ~/Applications/ \n",
        f"\n",
        f"You will be asked for authorization to change\n",
        f"             system settings!",
        f"\n",
        f"---------------------------------------------\n",
    )

    print(
        f" ---------------------------------------------\n",
        f"USER SETTINGS: \n",
        f"SERVER USER: {SERVER_USER} \n",
        f"SERVER IP: {SERVER_IP} \n",
        f"SERVER LOCAL: {SERVER_LOCAL} \n",
        f"CUSTOM ALIAS: {CUSTOM_ALIAS} \n",
        f"---------------------------------------------\n",
    )


def print_summary():
    # print notification
    print(f"---------------------------------------------\n")
    print(
        f"Run the command: \n",
        f">>> {CUSTOM_ALIAS} \n",
        f"This will bring up the TigerVNC viewer client...",
        f"Enter Address: localhost:5901",
    ),
    print(f"---------------------------------------------\n")


if __name__ == "__main__":

    validate()
    print_intro()

    # await user input
    user_input = input("Enter version of TigerVNC installed [Default==1.12.0] \n")

    if len(user_input) > 0:
        TIGERVNC_VER = user_input

    # installing ttab (need to approve accessibility settings)
    # ttab allows automation via terminal tabs: https://www.npmjs.com/package/ttab
    # the -g option installs the package globally by adding it to your path
    os.system("brew update")
    os.system("brew install node")
    os.system("npm install ttab -g")
    os.system("ttab")

    # create an alias that will be added to the shell
    alias_vnc_viewer = (
        f"alias vnc_viewer='~/Applications/TigerVNC\ Viewer\ {TIGERVNC_VER}.app'"
    )
    alias_vnc_devbox = f"alias {CUSTOM_ALIAS}='ttab ssh -L {TIGERVNC_PORT}:{SERVER_LOCAL}:{TIGERVNC_PORT} {SERVER_LOGIN}; alias_vnc_viewer'"

    # define the path to the shell configurations
    bashrc = os.path.abspath("%s/.bashrc" % HOME_FOLDER)
    zshrc = os.path.abspath("%s/.zshrc" % HOME_FOLDER)

    # update the files with custom alias
    update_file(file=bashrc, custom_line=alias_vnc_viewer)
    update_file(file=zshrc, custom_line=alias_vnc_viewer)
    update_file(file=bashrc, custom_line=alias_vnc_devbox)
    update_file(file=zshrc, custom_line=alias_vnc_devbox)

    print_summary()

