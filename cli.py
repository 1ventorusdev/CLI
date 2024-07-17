import os
import datetime
import socket
import platform

class DataBase:
    def __init__(self):
        self.version = "beta 0.10.5"
        self.output = ""
        self.CommandHelp = {
            "shutdown": "bla bla bla",
            "cd": "bla bla bla",
            "dir": "bla bla bla",
            "ls": "bla bla bla",
            "quit": "bla bla bla",
        }

        self.filetype = {
            "python file": [".py", ".pyc"],
            "c file": [".c", ".cpp", ".c#", ".h"],  # Ajout de .cpp et .h
            "JS file": [".js"],
            "HTML file": [".html", ".htm"],
            "CSS file": [".css"],
            "temp file": [".tmp", ".temp"],
            "config file": [".conf", ".config", ".cfg"],
            "log file": [".log"],
            "version file": [".ver"],
            "SQL file":[".sql"],
            "text file": ["txt"],
            "game data file": [".gdta"],
            "vodka file": [".vod"],
            "error file": [".err", ".error"],
            "assembly file": [".asm"]
            }
        
    data = {
        "$d": str(datetime.date.today()),
        "$t": str(datetime.datetime.now().time()),
        "$p": os.getcwd(),
        "$username": os.getlogin(),
        "$hostname": socket.gethostname(),
        "$v": platform.system() + " " + platform.version(),
        "$ip": "0.0.0.0", # replace by method for obtain ip
        "$mac": "ffff.ffff.ffff.ffff" # replace by method for obtain mac address
        }

    tmp = {}

    shutdownCommand = ["shutdown", "stop"]

    system = platform.system()
    if system == "Windows":
        clear = "cls"
        shutdown = "shutdown -p"
        disc = ["a:", "b:", "c:", "d:", "e:", "f:", "g:", "h:", "i:", "j:", "k:", "l:", "m:", "n:", "o:", "p:", "q:", "r:", "s:", "t:", "u:", "v:", "w:", "x:", "y:", "z:"]
    elif system == "Linux":
        clear = "clear"
        shutdown = "shutdown -h"
        disc = []
        for file in os.listdir(f"/media/{os.getlogin()}"):
            d = os.path.join(f"/media/{os.getlogin()}", file)
            if os.path.isdir(d):
                disc.append(file)

    def entry(self):
        cd = os.getcwd()
        if platform.system() == "Linux":
            if cd.startswith(f"/home/{os.getlogin()}"):
                cd = cd.replace(f"/home/{os.getlogin()}", "~")
            endcommand = "\033[33m$"
        elif platform.system() == "Windows":
            endcommand = "\033[36m>"
        else:
            endcommand = "\033[33m$\033[36m>>>"
        cd = cd.replace("\\", "/")
        cd = cd.replace("//", "/")
        return (
            f"\033[1m\033[36m┌─[\033[34mCLI {self.version}\033[36m]─[\033[31m{cd}\033[36m]\n"
            f"\033[1m\033[36m└───(\033[32m{os.getlogin()}\033[34m\033[31m@\033[31m{socket.gethostname()}\033[36m){endcommand}\033[0m "
        )
    
    # set the data to print after
    def setOutput(self, output):
        self.output = output

    def addOutput(self, output):
        self.output += output

    # print data saved
    def printOutput(self):
        print(self.output)


    # for return the help of command
    def commandhelp(self, command):
        return self.CommandHelp[command]
    
    def isExecutable(self, filename, ext):
        if ext == ".exe":
            return "app file"

        if platform.system() == "Linux":
            if os.access(filename, os.X_OK):
                return "app file"
        return None

    def whatfiletype(self, filename):
        _, ext = os.path.splitext(filename)
        executable = self.isExecutable(filename, ext)
        if executable:
            return executable

        for filetype, exts in self.filetype.items():
            if ext in exts:
                return filetype
            
        typefile = ext.upper() + " file"
        typefile = typefile.replace(".", "")
        return typefile
    
database = DataBase()

class Commands:
    class Var:
        def replace(command:str):
            if "$" in command:
                if command.startswith("?") or "=" in command:
                    pass
                else:
                    for key in database.tmp:
                        if key in command:
                            command = command.replace(key, database.tmp[key])

                    for key in database.data:
                        if key in command:
                            command = command.replace(key, database.data[key])
            return command

        def create(command:str, method):
            if method == "$":
                value, data_name = command.split("=")
                value = value.strip()  # Supprimer les espaces autour de value
                data_name = data_name.strip()
                data_name = "$" + data_name
                data_name = data_name.replace(" ", "")

                if value.lower() in database.data:
                    if data_name in database.tmp:
                        del database.tmp[data_name]
                    database.tmp[data_name] = database.data[value]
                    database.addOutput(f"Donnée '{data_name}' enregistrée avec la valeur '{database.data[value]}'.")
                else:
                    database.addOutput("Donnée $ inconnue")

            elif method == "!":
                value, data_name = command.split("=")
                data_name = "$" + data_name
                data_name = data_name.replace(" ", "")
                value = value.strip()  # Supprimer les espaces autour de value
                data_name = data_name.strip()  # Supprimer les espaces autour de data_name
                if data_name in database.tmp:
                    del database.tmp[data_name]
                database.tmp[data_name] = value
                database.addOutput(f"Donnée '{data_name}' enregistrée avec la valeur '{value}'.")

        def print(command:str):
            if "? " in command:
                variable = command.replace("? ", "")
            else:
                variable = command.replace("?", "")
            if variable.lower() in database.data:
                database.addOutput(database.data[variable.lower()])
            else:
                if not "$" in variable:
                    variable = "$" + variable
                if variable in database.tmp:
                    database.addOutput(database.tmp[variable])
                elif variable.startswith("$!"):
                    variable = variable.replace("$!", "")
                    database.addOutput(variable)
                else:
                    database.addOutput("valeur nom sauvegardé")

    class Dirs:
        def cdlast():
            try:
                parent_directory = os.path.normpath(os.path.join(os.getcwd(), ".."))
                os.chdir(parent_directory)
            except Exception as e:
                database.addOutput(f"Erreur lors du changement de répertoire : {e}")
        
        def cdroot():
            try:
                # Obtient la racine du disque
                root_directory = os.path.abspath(os.sep)
                os.chdir(root_directory)
            except Exception as e:
                database.addOutput(f"Erreur lors du changement de répertoire : {e}")

        def cdtopath(path):
            _, path = path.split(" ", 1)
            path = path.strip()
            try:
                files =  os.listdir()
                if path.startswith("/") and os.path.exists(path.replace("/", "", 1)):
                    path = path.replace("/", "", 1)
                os.chdir(path)
            except FileNotFoundError:
                database.addOutput(f"Le répertoire '{path}' n'existe pas.")
            except Exception as e:
                database.addOutput(f"Erreur lors du changement de répertoire : {e}")

        def cddrive(path):
            if database.system == "Windows":
                os.chdir(path)
            elif database.system == "Linux":
                os.chdir(f"/media/{database.data["$username"]}/{path}")

        def cdUserfile():
            if database.system == "Windows":
                os.chdir(f"c:Users/{database.data["$username"]}")
            elif database.system == "Linux":
                os.chdir(f"/home/{database.data["$username"]}")

        def printcd():
            database.addOutput(os.getcwd())
        
        def printdir(cd):
            files = os.listdir(cd)
            database.addOutput("{:<60} {:<9}\n".format("filename", "type"))
            database.addOutput("-"*75 + "\n")
            for file in files:
                if cd:
                    path = os.path.join(cd, file)
                if file in database.disc:
                    typefile = "[drive]"
                    filename = f"/{file}"
                elif os.path.isdir(path):
                    typefile = "<directory>"
                    filename = f" /{file}"
                elif os.path.isfile(path):
                    typefile = database.whatfiletype(file)
                    filename = f"./{file}"
                else:
                    typefile = "unckown"
                    filename = f"{file}"
                database.addOutput(" {:<60}{:<7}\n".format(filename, typefile))

        def ls(cd):
            output = ""
            files = os.listdir(cd)
            for file in files:
                output += f"{file}  "

            database.addOutput(output)

    # add other class for catergory of command
    # add command in class
    # add command general (not add in under class)

    class System:
        def shutdown(command:str):
            command = command.split()
            if len(command) < 2:
                database.addOutput("please enter parameter of shutdown")
                return
            if command[1] == "-n":
                # method for shutdown system now
                os.system("shutdown /s /t 0")
            elif command[1] == "-t":
                timesleep = int(command[2])
                os.system(f"shutdown /s /t {timesleep}")
                # method to shutdown system in end of timesleep second
            elif command[1] == "/?":
                database.addOutput(database.commandhelp("shutdown"))
        
        # add command system


    class Admin:
        # command only admin user
        pass

    class User:
        # command alternative of admin command
        pass

def main():
    while True:
        command = input(database.entry())
        database.setOutput("")

        command = Commands.Var.replace(command)

        if command == "close":
            quit()
        
        if command.startswith("$"):
            Commands.Var.create(command, "$")
        elif command.startswith("!"):
            command = command.replace("!", "", 1)
            Commands.Var.create(command, "!")
        elif command.startswith("?"):
            Commands.Var.print(command)
        
        elif command.startswith("cd"):
            if command == "cd":
                Commands.Dirs.printcd()
            elif command == "cd..":
                Commands.Dirs.cdlast()
            elif command == "cd/":
                Commands.Dirs.cdroot()
            else:
                if command.endswith("~") or command.endswith(database.data["$username"]):
                    Commands.Dirs.cdUserfile()
                else:
                    Commands.Dirs.cdtopath(command)

        elif command in database.disc:
            Commands.Dirs.cddrive(command)

        elif command.startswith("dir"):
            command = command.split(" ")
            path = os.getcwd()
            if len(command) > 1:
                path = ' '.join(command[1:])
            Commands.Dirs.printdir(path)

        elif command.startswith("ls"):
            command = command.split(" ")
            path = os.getcwd()
            if len(command) > 1:
                path = ' '.join(command[1:])
            Commands.Dirs.ls(path)

        # add traitment of command 


        else:
            database.setOutput("unckown command")

        database.printOutput()

main()

# add try and except for the manage error