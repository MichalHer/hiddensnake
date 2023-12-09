from hiddensnake.encryption_algorithms import DESEncryptorCBC
from hiddensnake.carrier_files import WavFile, PngFile
from hiddensnake.hiding_algorithms import LSBHider
from hiddensnake import HiddenSnake
from hiddensnake.base import BaseEncrypter, BaseHider, BaseFile
import os.path as pth
from getpass import getpass
import pickle

CARRIER_CLASSES = {
    ".png":PngFile,
    ".wav":WavFile
}

LOGO = (
    " _  _ _    _    _          ___           _       \n"
    "| || (_)__| |__| |___ _ _ / __|_ _  __ _| |_____ \n"
    "| __ | / _` / _` / -_) ' \\\\__ \ ' \/ _` | / / -_)\n"
    "|_||_|_\__,_\__,_\___|_||_|___/_||_\__,_|_\_\___|\n"
)


def show_wrong_choice():
    print("- didn't expect that ¯\_( ͡° ͜ʖ ͡°)_/¯")
    
def show_logo():
    print(LOGO)
    
def show_exception_occured():
    print("- SOMETHING WENT WRONG! (ノಠ益ಠ)ノ彡┻━┻")

def get_command():
    return input("- ")

def get_password():
    return getpass("- ")

class MainMenu:

    def __init__(self):
        self.hs = HiddenSnake()
        self.steg = LSBHider()
        self.enc = DESEncryptorCBC()


    def __str__(self):
        return (
            f"0. set password\n"
            f"1. configure stego algorithm {'(unloaded)' if self.steg == None else ''}\n"
            f"2. configure crypto algorithm {'(unloaded)' if self.enc == None else ''}\n"
            "3. register carrier file\n"
            "4. register hidden file\n"
            "5. register hidden message\n"
            "6. hide\n"
            "7. reveal\n"
            "\n"
            "? - print menu again\n"
            "\"e\" or \"exit\" for exit\n"
            "\n"
        )
    
    def ask(self):
        self.enter_choice(input("- choose an option: "))
    
    def enter_choice(self, choice: str):
        if choice == "0":
            try:
                print('- enter the password')
                passwd = get_password()
                self.enc.set_password(passwd)
                if len(passwd) < 7: print("- Soooo weeeeak... (－‸ლ)")
                else: print("- OK (̿▀̿ ̿Ĺ̯̿̿▀̿ ̿)̄")
            except Exception as e:
                print(e)
                show_exception_occured()

        elif choice == "?":
            print(self)

        elif choice == "2":
            try:
                print("- enter a .pkl crypto class file path")
                path = get_command()
                with open(path, 'rb') as file:
                    self.enc = pickle.load(file)
                self.enc = self.enc()
                print("- Crypto class registered ( ͡° ͜ʖ ͡°)")
            except Exception:
                show_exception_occured()

        elif choice == "3":
            try:
                print("- enter a carrier file path")
                path = get_command()
                filename = str(pth.basename(path))
                extension = filename[filename.find("."):]
                try:
                    fp = CARRIER_CLASSES[extension]()
                except:
                    print("- Unknown carrier file ◕_◕")
                    fp = None
                fp.from_file(path)
                fp.set_filename(filename)
                self.hs.register_carrier_file(fp)
                print("- Carrier file registered ( ͡° ͜ʖ ͡°)")
            except Exception as e:
                print(e)
                show_exception_occured()

        elif choice == "4":
            try:
                print("- enter a secret file path")
                path = get_command()
                with open(path, 'rb') as file:
                    file_bytes = bytearray(file.read())
                dot_idx = path.find(".", 1)
                if dot_idx != -1 : file_extension = path[dot_idx:]
                self.hs.register_hidden_bytes(file_bytes, file_extension)
                print("- OK! (☞ﾟヮﾟ)☞")
            except Exception:
                show_exception_occured()
            
        elif choice == "5":
            try:
                print('- enter a secret message')
                message = get_command()
                self.hs.register_hidden_bytes(bytearray(message, encoding='utf-8'))
                print("- OK! (☞ﾟヮﾟ)☞")
            except Exception:
                show_exception_occured()
                
        elif choice == "6":
            try:
                self.steg.register_encrypter(self.enc)
                self.hs.register_hider(self.steg)
                print("- Wait a minute... (͡ ° ͜ʖ ͡ °)")
                if self.hs.can_hide():
                    files = self.hs.hide()
                    for i, f in enumerate(files):
                        filename = f'file_with_hidden_message_{i+1}.unknown'
                        if f.filename != None: filename = f"{i+1}_stego_{f.filename}"
                        f.save_file(filename)
                    print("Let's rock! ୧༼ಠ益ಠ༽︻╦╤─")
                else:
                    print('- carrier files capacity is too low. ( ͡° ʖ̯ ͡°)')
            except Exception as e:
                print(e)
                show_exception_occured()
            
        elif choice == "7":
            try:
                print("- Wait a minute... (͡ ° ͜ʖ ͡ °)")
                self.steg.register_encrypter(self.enc)
                self.hs.register_hider(self.steg)
                reveal_result = self.hs.reval()
                revaled_bytes = reveal_result[0]
                file_ext = reveal_result[1]
                if file_ext[0] == ".":
                    with open(f"secret_file{file_ext}", 'wb') as file:
                        file.write(revaled_bytes)
                    print("- Done. (̿▀̿‿ ̿▀̿ ̿)")
                else:
                    print("- Listen ◕_◕...")
                    print("\t...", revaled_bytes.decode())
                
            except Exception:
                show_exception_occured()
            
        elif choice in ["e", "exit", "end", "q", "quit"]:
            exit()
            
        else:
            show_wrong_choice()


def main():
    show_logo()
    menu = MainMenu()
    print(menu)
    while 1:
        menu.ask()
    
if __name__ == "__main__":
    main()