from pystyle import Colors, Colorate
import time
import os
import random
import string
import psutil
import requests
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

# ========== UTF-8 ДЛЯ КОРРЕКТНОГО ОТОБРАЖЕНИЯ ==========
if sys.platform == "win32":
    sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)


# ========== STYLE FUNCTIONS ==========
def print_header(title):
    border_top = "╔" + "═" * 48 + "╗"
    border_bottom = "╚" + "═" * 48 + "╝"
    print(Colorate.Horizontal(Colors.blue_to_cyan, border_top, 1))
    print(Colorate.Horizontal(Colors.cyan_to_blue, f"║{title.center(48)}║", 1))
    print(Colorate.Horizontal(Colors.blue_to_cyan, border_bottom, 1))


def print_section(title):
    print(Colorate.Horizontal(Colors.cyan_to_blue, f"\n▰▰▰ {title} ▰▰▰", 1))


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# ========== MAIN BANNER ==========
def show_banner():
    banner = """
╔══════════════════════════════════════════════════════════╗
║                    StarSoft Multi-Tool v2.5              ║
║              ADVANCED HELPER FOR MORE TASKS!             ║
║                    BY: f34ky | NN⁶² TEAM                 ║
╠══════════════════════════════════════════════════════════╣
║  [1] Random Password      [5] Website Headers           ║
║  [2] CPU and RAM Info      [6] IP Info                   ║
║  [3] PING site            [7] Text to ASCII Art          ║
║  [4] Username Search      [8] Password Strength          ║
║  [0] Exit                                                ║
╚══════════════════════════════════════════════════════════╝
"""
    print(Colorate.Horizontal(Colors.blue_to_cyan, banner, 1))


# ========== TOOL 1: RANDOM PASSWORD ==========
def random_password():
    clear_screen()
    print_header("RANDOM PASSWORD GENERATOR")

    try:
        length = int(input("\n└─$ Enter password length (8-32): "))
        if length < 8:
            length = 8
            print("  ⚠ Minimum length set to 8")
        elif length > 32:
            length = 32
            print("  ⚠ Maximum length set to 32")

        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(length))

        print_section("RESULT")
        print(f"  ✓ Generated password: {password}")
        print(f"  📏 Length: {length} characters")

        strength = "High" if length > 12 else "Medium"
        print(f"  🔒 Strength: {strength}")

        save = input("\n└─$ Save password to file? (yes/no): ")
        if save.lower() == "yes":
            with open("passwords.txt", "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {password}\n")
            print("  ✓ Password saved to passwords.txt")

    except ValueError:
        print("  ✗ Error: please enter a number!")

    input("\n└─$ Press Enter to continue...")


# ========== TOOL 2: SYSTEM INFO ==========
def system_info():
    clear_screen()
    print_header("SYSTEM INFORMATION")

    print_section("CPU")
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()

    bar_length = int(cpu_percent / 4)
    print(f"  Usage: [{'█' * bar_length}{'░' * (25 - bar_length)}] {cpu_percent}%")
    print(f"  Cores: {cpu_count}")
    if cpu_freq:
        print(f"  Frequency: {cpu_freq.current:.0f} MHz")

    print_section("RAM")
    ram = psutil.virtual_memory()
    ram_used_gb = ram.used / (1024 ** 3)
    ram_total_gb = ram.total / (1024 ** 3)
    bar_length = int(ram.percent / 4)

    print(f"  Used: {ram_used_gb:.1f} / {ram_total_gb:.1f} GB")
    print(f"  Usage: [{'█' * bar_length}{'░' * (25 - bar_length)}] {ram.percent}%")

    input("\n└─$ Press Enter to continue...")


# ========== TOOL 3: PING SITE ==========
def ping_site():
    clear_screen()
    print_header("WEBSITE PINGER")

    site = input("\n└─$ Enter website URL (e.g., google.com): ").strip()
    if not site.startswith("http"):
        site = "https://" + site

    print_section("CHECKING")

    try:
        start_time = time.time()
        response = requests.get(site, timeout=5)
        response_time = (time.time() - start_time) * 1000

        if response.status_code == 200:
            print(f"  ✓ WEBSITE IS ONLINE!")
            print(f"  ⏱ Response time: {response_time:.0f} ms")
            print(f"  📊 Status: {response.status_code}")
        else:
            print(f"  ⚠ Website responded with status: {response.status_code}")

    except requests.ConnectionError:
        print(f"  ✗ WEBSITE IS OFFLINE! Check URL or internet connection")
    except requests.Timeout:
        print(f"  ✗ Timeout! Website not responding (5 seconds)")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    input("\n└─$ Press Enter to continue...")


# ========== TOOL 4: USERNAME SEARCH (FIXED) ==========

# Только сайты, которые реально работают с проверкой
USERNAME_SITES = {
    "VK": "https://vk.com/{}",
    "GitHub": "https://github.com/{}",
    "Telegram": "https://t.me/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Chess": "https://www.chess.com/member/{}",
    "HackerRank": "https://www.hackerrank.com/{}",
    "LeetCode": "https://leetcode.com/{}/",
    "Replit": "https://replit.com/@{}",
    "PyPI": "https://pypi.org/user/{}",
    "npm": "https://www.npmjs.com/~{}",
    "Codecademy": "https://www.codecademy.com/profiles/{}",
    "Codewars": "https://www.codewars.com/users/{}",
    "BitBucket": "https://bitbucket.org/{}/",
    "GitLab": "https://gitlab.com/{}",
    "Keybase": "https://keybase.io/{}",
    "Patreon": "https://www.patreon.com/{}",
    "Tumblr": "https://{}.tumblr.com/",
    "DeviantArt": "https://www.deviantart.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
}


def check_site(site_name, url_template, username):
    url = url_template.format(username)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    try:
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=False)

        # Если статус 404 — точно нет
        if response.status_code == 404:
            return (site_name, url, False)

        # Если статус 200 — проверяем содержимое
        if response.status_code == 200:
            html_lower = response.text.lower()

            # Ключевые слова "не найден"
            not_found_markers = [
                "not found", "page not found", "doesn't exist", "does not exist",
                "user not found", "profile not found", "account not found",
                "не найден", "страница не найдена", "пользователь не найден",
                "doesn't have an account", "sorry, nobody", "there doesn't seem to be anything here",
                "the specified profile could not be found", "no user found",
                "content not found", "we couldn't find"
            ]

            for marker in not_found_markers:
                if marker in html_lower:
                    return (site_name, url, False)

            # Если маркеров нет — считаем, что аккаунт существует
            return (site_name, url, True)

        # Другие статусы (301, 302, 403, 500 и т.д.) — считаем как "не найден"
        return (site_name, url, False)

    except Exception:
        return (site_name, url, False)


def username_search():
    clear_screen()
    print_header("USERNAME SEARCH")
    print("  Search for accounts on 20+ platforms")
    print("  Supported: VK, GitHub, Telegram, YouTube, TikTok,")
    print("  Chess, HackerRank, LeetCode, Replit, PyPI, and more!")
    print("  ⚠ Instagram, Twitter, Reddit, Twitch, Steam, Spotify removed (false positives)")

    username = input("\n└─$ Enter username to search: ").strip()

    if not username:
        print("  ✗ Username not entered!")
        input("\n└─$ Press Enter to continue...")
        return

    # Очищаем username от пробелов и спецсимволов
    username = username.replace(" ", "").replace("@", "")

    print(Colorate.Horizontal(Colors.cyan_to_blue,
                              f"\n[*] Searching for '{username}' on {len(USERNAME_SITES)} sites...\n", 1))

    found_sites = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = {}
        for site_name, url_template in USERNAME_SITES.items():
            future = executor.submit(check_site, site_name, url_template, username)
            futures[future] = site_name

        for future in as_completed(futures):
            site_name, url, found = future.result()
            if found:
                found_sites.append((site_name, url))
                print(f"  ✓ {site_name}: FOUND -> {url}")

    search_time = time.time() - start_time

    # RESULTS
    print("\n" + "=" * 60)
    print(Colorate.Horizontal(Colors.blue_to_cyan, f"RESULTS FOR: {username}", 1))
    print("=" * 60)

    if found_sites:
        print(Colorate.Horizontal(Colors.green_to_cyan, f"\n[+] FOUND ON {len(found_sites)} SITES:\n", 1))
        for site_name, url in found_sites:
            print(f"  ► {site_name}")
            print(f"    {url}")
            print()
    else:
        print(Colorate.Horizontal(Colors.yellow_to_red, f"\n[-] No accounts found for '{username}'", 1))

    print("=" * 60)
    print(Colorate.Horizontal(Colors.blue_to_cyan,
                              f"Total checked: {len(USERNAME_SITES)} | Found: {len(found_sites)} | Time: {search_time:.2f}s",
                              1))
    print("=" * 60)

    # SAVE TO FILE
    if found_sites:
        filename = f"{username}_results.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Results for {username}\n")
            f.write("=" * 50 + "\n\n")
            for site_name, url in found_sites:
                f.write(f"{site_name}: {url}\n")
        print(Colorate.Horizontal(Colors.green_to_cyan, f"\n[+] Results saved to: {filename}", 1))

    input("\n└─$ Press Enter to continue...")


# ========== TOOL 5: WEBSITE HEADERS ==========
def website_headers():
    clear_screen()
    print_header("WEBSITE HEADERS")

    site = input("\n└─$ Enter website URL: ").strip()
    if not site.startswith("http"):
        site = "https://" + site

    try:
        response = requests.get(site, timeout=5)
        print_section("HEADERS")
        print(f"  Status: {response.status_code}")
        print("\n  Headers:")
        for key, value in response.headers.items():
            short_value = value[:80] + "..." if len(value) > 80 else value
            print(f"    {key}: {short_value}")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    input("\n└─$ Press Enter to continue...")


# ========== TOOL 6: IP INFO ==========
def ip_info():
    clear_screen()
    print_header("IP INFORMATION")

    ip = input("\n└─$ Enter IP address (or leave empty for your IP): ").strip()

    if not ip:
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            ip = response.json()['ip']
            print(f"\n  ℹ Your IP: {ip}")
        except:
            print("  ✗ Could not determine your IP")
            input("\n└─$ Press Enter...")
            return

    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        data = response.json()

        if data['status'] == 'success':
            print_section("IP INFORMATION")
            print(f"  Country: {data.get('country', 'N/A')}")
            print(f"  City: {data.get('city', 'N/A')}")
            print(f"  ISP: {data.get('isp', 'N/A')}")
            print(f"  Region: {data.get('regionName', 'N/A')}")
            print(f"  Zip Code: {data.get('zip', 'N/A')}")
            print(f"  Coordinates: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}")
        else:
            print(f"  ✗ Could not get IP information")
    except Exception as e:
        print(f"  ✗ Error: {e}")

    input("\n└─$ Press Enter to continue...")


# ========== TOOL 7: TEXT TO ASCII ART ==========
def text_to_ascii():
    clear_screen()
    print_header("ASCII ART GENERATOR")

    text_input = input("\n└─$ Enter text: ")

    print_section("BLOCK MODE")
    block_result = ""
    for char in text_input.upper():
        if char.isalpha():
            block_result += f"[{char}]"
        else:
            block_result += f" {char} "
    print(f"  {block_result}")

    input("\n└─$ Press Enter to continue...")


# ========== TOOL 8: PASSWORD STRENGTH ==========
def password_strength():
    clear_screen()
    print_header("PASSWORD STRENGTH CHECKER")

    password = input("\n└─$ Enter password to check: ")

    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Too short (min. 8 characters)")

    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters")

    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add numbers")

    if any(c in "!@#$%^&*" for c in password):
        score += 1
    else:
        feedback.append("Add special characters (!@#$%^&*)")

    print_section("RESULT")

    if score == 5:
        print(f"  Score: {score}/5 - VERY STRONG!")
    elif score >= 3:
        print(f"  Score: {score}/5 - MEDIUM")
    else:
        print(f"  Score: {score}/5 - WEAK")

    if feedback:
        print("\n  Recommendations:")
        for f in feedback:
            print(f"    - {f}")

    input("\n└─$ Press Enter to continue...")


# ========== MAIN MENU ==========
def main():
    while True:
        clear_screen()
        show_banner()

        choice = input("\n└─$ Choose tool (0-8): ").strip()

        if choice == '1':
            random_password()
        elif choice == '2':
            system_info()
        elif choice == '3':
            ping_site()
        elif choice == '4':
            username_search()
        elif choice == '5':
            website_headers()
        elif choice == '6':
            ip_info()
        elif choice == '7':
            text_to_ascii()
        elif choice == '8':
            password_strength()
        elif choice == '0' or choice.lower() == 'exit':
            print(Colorate.Horizontal(Colors.blue_to_cyan, "\n[+] Thanks for using StarSoft! Goodbye!\n", 1))
            sys.exit()
        else:
            print("  ✗ Invalid choice! Enter number 0-8")
            time.sleep(1.5)


# ========== RUN ==========
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Colorate.Horizontal(Colors.blue_to_cyan, "\n\n[+] Program terminated. Goodbye!\n", 1))
    except Exception as e:
        print(f"\n✗ Error: {e}")
        input("Press Enter to exit...")