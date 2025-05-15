from telethon.sync import TelegramClient
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.types import Channel, Chat
from telethon.errors import RPCError
import os
from colorama import Fore, Style, init

init(autoreset=True)

banner = f"""{Fore.RED}████████╗ █████╗  ██████╗ ██████╗
╚══██╔══╝██╔══██╗██╔════╝██╔════╝
   ██║   ███████║██║     ██║    By - @Naresh
   ██║   ██╔══██║██║     ██║    IG - @errorexplot
   ██║   ██║  ██║╚██████╗╚██████╗
   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝
                                 {Style.RESET_ALL}"""


def disclaimer():
    print(f"""{Fore.RED}
==================================================
⚠️  DISCLAIMER ⚠️

1. This tool DOES NOT delete personal chats.
2. This is NOT a hacking script.
3️. This tool is trustworthy and DOES NOT store your personal information.

==================================================
{Style.RESET_ALL}""")
client = None
print(banner)

def login():
    global client
    print(f"{Fore.RED}🔐 Login - Enter your details{Style.RESET_ALL}")

    api_id = int(input("🔢 Enter your Telegram API ID: "))
    api_hash = input("🔐 Enter your Telegram API Hash: ")
    phone = input("📱 Enter your phone number with country code (e.g. +91XXXXXXXXXX): ")
    session_name = input("📁 Enter a session name (e.g. abcd1234): ")

    session_file = f"{session_name}.session"

    client = TelegramClient(session_file, api_id, api_hash)
    client.connect()

    if not client.is_user_authorized():
        print("📨 Sending OTP to your Telegram...")
        client.send_code_request(phone)
        code = input("✅ Enter the OTP you received: ")
        client.sign_in(phone, code)
    else:
        print("✅ Session loaded. You're already logged in!")

    print("✅ Logged in successfully!")

def leave_all_channels():
    global client
    if not client:
        print(f"{Fore.RED}❌ You need to login first!{Style.RESET_ALL}")
        return

    dialogs = client.get_dialogs()
    left_count = 0

    for dialog in dialogs:
        entity = dialog.entity
        if isinstance(entity, Channel) and dialog.is_channel and not dialog.is_group:
            try:
                print(f"🚪 Leaving channel: {dialog.name}")
                client(LeaveChannelRequest(entity))
                left_count += 1
            except Exception as e:
                print(f"❌ Error leaving {dialog.name}: {e}")

    print(f"\n✅ Done. Left {left_count} channel(s).")

def leave_dead_channels_groups_bots():
    global client
    if not client:
        print(f"{Fore.RED}❌ You need to login first!{Style.RESET_ALL}")
        return

    dialogs = client.get_dialogs()
    left_count = 0

    for dialog in dialogs:
        entity = dialog.entity

        try:
            if isinstance(entity, Channel) or isinstance(entity, Chat):
                name = dialog.name or ""
                if "Deleted" in name or name.strip() == "":
                    print(f"🚪 Leaving dead channel/group/bot: {name if name else 'Unknown'}")
                    client(LeaveChannelRequest(entity))
                    left_count += 1
        except RPCError as e:
            print(f"❌ RPC Error leaving {dialog.name}: {e}")
        except Exception as e:
            print(f"⚠️ Skipped (error): {e}")

    print(f"\n✅ Done. Left {left_count} dead channels/groups/bots.")

def about_me():
    print(f"""{Fore.RED}
===============================================================================
= 👋 Hy Dear User ,                                                           
= 🙋‍♂️ My Name Is Naresh And I Am An Ethical Hacker.                            
= 🛠️ I Have Developed This Channel Leave Tool For You.                        
= 📱 I Know You Join Too Many Channels And Want To Leave Them At Once.        
= 🤖 So I Created This Tool To Help You Out.                                  
= 🙏 If You Like My Work, Please Follow Me On Instagram: @errorexploit        
= 💻 Also Follow My GitHub To Stay Updated With New Projects.                 
===============================================================================
{Style.RESET_ALL}""")

def main():
    global client
    disclaimer()  # डिस्क्लेमर शो करो

    while True:
        print(f"""{Fore.RED}
📲 Telegram Channel Leave Tool
1️⃣ Login
2️⃣ Leave All Channels
3️⃣ Leave Dead Channels, Groups & Bots
4️⃣ About Me
5️⃣ Exit
{Style.RESET_ALL}""")
        choice = input(f"{Fore.RED}👉 Choose an option (1-5): {Style.RESET_ALL}")

        if choice == "1":
            login()
        elif choice == "2":
            leave_all_channels()
        elif choice == "3":
            leave_dead_channels_groups_bots()
        elif choice == "4":
            about_me()
        elif choice == "5":
            print(f"{Fore.RED}👋 Exiting... Bye My Dear User ❤️ !{Style.RESET_ALL}")
            if client:
                client.disconnect()
            break
        else:
            print(f"{Fore.RED}❌ Invalid choice! Try again.{Style.RESET_ALL}")

if __name__ == "__main__":
    main()