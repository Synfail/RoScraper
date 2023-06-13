import asyncio
import aiohttp
from colorama import Fore, Style
import os
import random

async def scrape_user(user_id, session):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    async with session.get(url) as response:
        if response.status == 200:
            data = await response.json()
            name = data.get("name")
            return name

async def scrape_usernames(user_id, num_users):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(num_users):
            task = asyncio.create_task(scrape_user(user_id, session))
            tasks.append(task)
            user_id = str(int(user_id) + 1)

        results = await asyncio.gather(*tasks)
        usernames = [name for name in results if name is not None]

    with open("usernames.txt", "w") as file:
        file.write("\n".join(usernames))

    print(f"Successfully scraped {len(usernames)} usernames. Saved in 'usernames.txt'.")

def main():
    # Clear console
    os.system('cls' if os.name == 'nt' else 'clear')

    # Print ASCII logo in red
    logo = """
    ██████╗  ██████╗ ███████╗ ██████╗██████╗  █████╗ ██████╗ ███████╗██████╗ 
    ██╔══██╗██╔═══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
    ██████╔╝██║   ██║███████╗██║     ██████╔╝███████║██████╔╝█████╗  ██████╔╝
    ██╔══██╗██║   ██║╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔══╝  ██╔══██╗
    ██║  ██║╚██████╔╝███████║╚██████╗██║  ██║██║  ██║██║     ███████╗██║  ██║
    ╚═╝  ╚═╝ ╚═════╝ ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
    v1.02
    """
    print(Fore.RED + logo + Style.RESET_ALL)

    use_random_number = input("Do you want to use a random ID? (y/n): ").lower()

    if use_random_number == "y":
        user_id = str(random.randint(1, 4702708283))
    else:
        user_id = input("Enter the user ID: ")

    num_users = int(input("Enter the number of users to scrape (Max 305): "))
    print(Fore.GREEN + f"\nScraping {num_users} Usernames..." + Style.RESET_ALL)

    asyncio.run(scrape_usernames(user_id, num_users))

if __name__ == "__main__":
    main()
