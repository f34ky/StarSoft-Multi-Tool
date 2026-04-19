from pystyle import Colors, Colorate
import time
import os
import random
import string
import psutil
import requests
import sys
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

# ========== UTF-8 FOR CORRECT DISPLAY ==========
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


def gradient_print(text, gradient=Colors.blue_to_cyan, delay=0.0001):
    colored_text = Colorate.Horizontal(gradient, text, 1)
    for char in colored_text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def gradient_input(prompt, gradient=Colors.cyan_to_blue, delay=0.0001):
    colored_prompt = Colorate.Horizontal(gradient, prompt, 1)
    for char in colored_prompt:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    return input()


def success_print(text):
    gradient_print(text, Colors.green_to_cyan)


def error_print(text):
    gradient_print(text, Colors.red_to_purple)


def info_print(text):
    gradient_print(text, Colors.blue_to_cyan)


def warning_print(text):
    gradient_print(text, Colors.yellow_to_red)


# ========== MAIN BANNER ==========
def show_banner():
    banner = """
╔══════════════════════════════════════════════════════════╗
║                    StarSoft Multi-Tool v2.6              ║
║              ADVANCED HELPER FOR MORE TASKS!             ║
║                    BY: f34ky | NN⁶² TEAM                 ║
╠══════════════════════════════════════════════════════════╣
║  [1] Random Password      [5] Website Headers            ║
║  [2] CPU and RAM Info     [6] IP Info                    ║
║  [3] PING site            [7] Text to ASCII Art          ║
║  [4] Username Search      [8] Password Strength          ║
║  [9] Link Analyzer        [0] Exit                       ║
╚══════════════════════════════════════════════════════════╝
"""
    print(Colorate.Horizontal(Colors.blue_to_cyan, banner, 1))

    info_print("[✓] New: Link Analyzer module added!\n")


# ========== TOOL 1: RANDOM PASSWORD ==========
def random_password():
    clear_screen()
    print_header("RANDOM PASSWORD GENERATOR")

    try:
        length = int(gradient_input("\n└─$ Enter password length (8-32): "))
        if length < 8:
            length = 8
            warning_print("  ⚠ Minimum length set to 8")
        elif length > 32:
            length = 32
            warning_print("  ⚠ Maximum length set to 32")

        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(length))

        print_section("RESULT")
        success_print(f"  ✓ Generated password: {password}")
        info_print(f"  📏 Length: {length} characters")

        strength = "High" if length > 12 else "Medium"
        if length > 12:
            gradient_print(f"  🔒 Strength: {strength}", Colors.green_to_cyan)
        else:
            gradient_print(f"  🔒 Strength: {strength}", Colors.yellow_to_red)

        save = gradient_input("\n└─$ Save password to file? (yes/no): ")
        if save.lower() == "yes":
            with open("passwords.txt", "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {password}\n")
            success_print("  ✓ Password saved to passwords.txt")

    except ValueError:
        error_print("  ✗ Error: please enter a number!")

    gradient_input("\n└─$ Press Enter to continue...")


# ========== TOOL 2: SYSTEM INFO ==========
def system_info():
    clear_screen()
    print_header("SYSTEM INFORMATION")

    print_section("CPU")
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    cpu_freq = psutil.cpu_freq()

    bar_length = int(cpu_percent / 4)
    info_print(f"  Usage: [{'█' * bar_length}{'░' * (25 - bar_length)}] {cpu_percent}%")
    info_print(f"  Cores: {cpu_count}")
    if cpu_freq:
        info_print(f"  Frequency: {cpu_freq.current:.0f} MHz")

    print_section("RAM")
    ram = psutil.virtual_memory()
    ram_used_gb = ram.used / (1024 ** 3)
    ram_total_gb = ram.total / (1024 ** 3)
    bar_length = int(ram.percent / 4)

    info_print(f"  Used: {ram_used_gb:.1f} / {ram_total_gb:.1f} GB")
    info_print(f"  Usage: [{'█' * bar_length}{'░' * (25 - bar_length)}] {ram.percent}%")

    gradient_input("\n└─$ Press Enter to continue...")


# ========== TOOL 3: PING SITE ==========
def ping_site():
    clear_screen()
    print_header("WEBSITE PINGER")

    site = gradient_input("\n└─$ Enter website URL (e.g., google.com): ").strip()
    if not site.startswith("http"):
        site = "https://" + site

    print_section("CHECKING")
    info_print(f"  Checking {site}...")

    try:
        start_time = time.time()
        response = requests.get(site, timeout=5)
        response_time = (time.time() - start_time) * 1000

        if response.status_code == 200:
            success_print(f"  ✓ WEBSITE IS ONLINE!")
            info_print(f"  ⏱ Response time: {response_time:.0f} ms")
            info_print(f"  📊 Status: {response.status_code}")
        else:
            warning_print(f"  ⚠ Website responded with status: {response.status_code}")

    except requests.ConnectionError:
        error_print(f"  ✗ WEBSITE IS OFFLINE! Check URL or internet connection")
    except requests.Timeout:
        error_print(f"  ✗ Timeout! Website not responding (5 seconds)")
    except Exception as e:
        error_print(f"  ✗ Error: {e}")

    gradient_input("\n└─$ Press Enter to continue...")


# ========== TOOL 4: USERNAME SEARCH (УЛУЧШЕН) ==========

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
    "Pinterest": "https://www.pinterest.com/{}/",
    "Spotify": "https://open.spotify.com/user/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Reddit": "https://www.reddit.com/user/{}",
}


def check_username_site(site_name, url_template, username):
    url = url_template.format(username)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    try:
        response = requests.get(url, headers=headers, timeout=5, allow_redirects=False)

        if response.status_code == 404:
            return (site_name, url, False)

        if response.status_code == 200:
            html_lower = response.text.lower()
            not_found_markers = [
                "not found", "page not found", "doesn't exist", "user not found",
                "profile not found", "account not found", "не найден",
                "страница не найдена", "пользователь не найден", "doesn't have an account",
                "sorry, nobody", "there doesn't seem to be anything here"
            ]
            for marker in not_found_markers:
                if marker in html_lower:
                    return (site_name, url, False)
            return (site_name, url, True)

        return (site_name, url, False)
    except Exception:
        return (site_name, url, False)


def username_search():
    clear_screen()
    print_header("USERNAME SEARCH")
    info_print("  Search for accounts on 25+ platforms")
    info_print("  Supported: VK, GitHub, Telegram, YouTube, TikTok, Twitch, Reddit, and more!")

    username = gradient_input("\n└─$ Enter username to search: ").strip()
    username = username.replace(" ", "").replace("@", "")

    if not username:
        error_print("  ✗ Username not entered!")
        gradient_input("\n└─$ Press Enter to continue...")
        return

    info_print(f"\n[*] Searching for '{username}' on {len(USERNAME_SITES)} sites...\n")

    found_sites = []
    start_time = time.time()

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {}
        for site_name, url_template in USERNAME_SITES.items():
            future = executor.submit(check_username_site, site_name, url_template, username)
            futures[future] = site_name

        for future in as_completed(futures):
            site_name, url, found = future.result()
            if found:
                found_sites.append((site_name, url))
                success_print(f"  ✓ {site_name}: FOUND -> {url}")

    search_time = time.time() - start_time

    print("\n" + "=" * 60)
    print(Colorate.Horizontal(Colors.blue_to_cyan, f"RESULTS FOR: {username}", 1))
    print("=" * 60)

    if found_sites:
        success_print(f"\n[+] FOUND ON {len(found_sites)} SITES:\n")
        for site_name, url in found_sites:
            info_print(f"  ► {site_name}")
            info_print(f"    {url}\n")
    else:
        warning_print(f"\n[-] No accounts found for '{username}'")

    print("=" * 60)
    info_print(f"Total checked: {len(USERNAME_SITES)} | Found: {len(found_sites)} | Time: {search_time:.2f}s")
    print("=" * 60)

    if found_sites:
        filename = f"{username}_results.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Results for {username}\n")
            f.write("=" * 50 + "\n\n")
            for site_name, url in found_sites:
                f.write(f"{site_name}: {url}\n")
        success_print(f"\n[+] Results saved to: {filename}")

    gradient_input("\n└─$ Press Enter to continue...")


# ========== TOOL 5: WEBSITE HEADERS ==========
def website_headers():
    clear_screen()
    print_header("WEBSITE HEADERS")

    site = gradient_input("\n└─$ Enter website URL: ").strip()
    if not site.startswith("http"):
        site = "https://" + site

    try:
        response = requests.get(site, timeout=5)
        print_section("HEADERS")
        info_print(f"  Status: {response.status_code}")
        info_print("\n  Headers:")
        for key, value in response.headers.items():
            short_value = value[:80] + "..." if len(value) > 80 else value
            info_print(f"    {key}: {short_value}")
    except Exception as e:
        error_print(f"  ✗ Error: {e}")

    gradient_input("\n└─$ Press Enter to continue...")


# ========== TOOL 6: IP INFO ==========
def ip_info():
    clear_screen()
    print_header("IP INFORMATION")

    ip = gradient_input("\n└─$ Enter IP address (or leave empty for your IP): ").strip()

    if not ip:
        try:
            response = requests.get('https://api.ipify.org?format=json', timeout=5)
            ip = response.json()['ip']
            info_print(f"\n  ℹ Your IP: {ip}")
        except:
            error_print("  ✗ Could not determine your IP")
            gradient_input("\n└─$ Press Enter...")
            return

    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        data = response.json()

        if data['status'] == 'success':
            print_section("IP INFORMATION")
            info_print(f"  Country: {data.get('country', 'N/A')}")
            info_print(f"  City: {data.get('city', 'N/A')}")
            info_print(f"  ISP: {data.get('isp', 'N/A')}")
            info_print(f"  Region: {data.get('regionName', 'N/A')}")
            info_print(f"  Zip Code: {data.get('zip', 'N/A')}")
            info_print(f"  Coordinates: {data.get('lat', 'N/A')}, {data.get('lon', 'N/A')}")
        else:
            error_print(f"  ✗ Could not get IP information")
    except Exception as e:
        error_print(f"  ✗ Error: {e}")

    gradient_input("\n└─$ Press Enter to continue...")


# ========== TOOL 7: TEXT TO ASCII ART ==========
def text_to_ascii():
    clear_screen()
    print_header("ASCII ART GENERATOR")

    text_input = gradient_input("\n└─$ Enter text: ")

    print_section("BLOCK MODE")
    block_result = ""
    for char in text_input.upper():
        if char.isalpha():
            block_result += f"[{char}]"
        else:
            block_result += f" {char} "
    info_print(f"  {block_result}")

    gradient_input("\n└─$ Press Enter to continue...")


# ========== TOOL 8: PASSWORD STRENGTH ==========
def password_strength():
    clear_screen()
    print_header("PASSWORD STRENGTH CHECKER")

    password = gradient_input("\n└─$ Enter password to check: ")

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
        success_print(f"  Score: {score}/5 - VERY STRONG!")
    elif score >= 3:
        warning_print(f"  Score: {score}/5 - MEDIUM")
    else:
        error_print(f"  Score: {score}/5 - WEAK")

    if feedback:
        info_print("\n  Recommendations:")
        for f in feedback:
            warning_print(f"    - {f}")

    gradient_input("\n└─$ Press Enter to continue...")


# ========== TOOL 9: LINK ANALYZER (НОВИНКА!) ==========

def expand_url(short_url):
    """Раскрывает сокращённую ссылку"""
    try:
        response = requests.head(short_url, allow_redirects=True, timeout=5)
        return response.url
    except:
        return short_url


def check_phishing_domains(url):
    """Проверяет URL по базе фишинговых доменов (локальная эвристика)"""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()

    suspicious_patterns = [
        r'secure-?.*\.(com|ru|org)',
        r'login-?.*\.(com|ru)',
        r'verify-?.*\.(com|ru)',
        r'account-?.*\.(com|ru)',
        r'signin-?.*\.(com|ru)',
        r'auth-?.*\.(com|ru)'
    ]

    for pattern in suspicious_patterns:
        if re.search(pattern, domain):
            return True, f"Подозрительный паттерн в домене: {domain}"

    return False, None


def get_whois_info(domain):
    """Простая WHOIS-подобная проверка (без внешних API)"""
    try:
        response = requests.get(f"https://rdap.org/domain/{domain}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data
    except:
        pass
    return None


def link_analyzer():
    clear_screen()
    print_header("LINK ANALYZER")
    info_print("  Analyze links for safety, redirects, and basic info")
    info_print("  Features: URL expansion, phishing detection, domain info")

    url = gradient_input("\n└─$ Enter URL to analyze: ").strip()

    if not url:
        error_print("  ✗ No URL entered!")
        gradient_input("\n└─$ Press Enter to continue...")
        return

    if not url.startswith("http"):
        url = "https://" + url

    print_section("ANALYSIS")

    # 1. Проверка доступности
    info_print(f"  Checking: {url}")
    try:
        response = requests.get(url, timeout=5, allow_redirects=False)
        info_print(f"  Status code: {response.status_code}")
    except:
        warning_print("  Could not reach the URL")

    # 2. Раскрытие сокращённой ссылки
    if "bit.ly" in url or "tinyurl" in url or "short" in url or "goo.gl" in url or "clck.ru" in url:
        info_print("  Detected short link, expanding...")
        expanded = expand_url(url)
        if expanded != url:
            success_print(f"  Expanded URL: {expanded}")
        else:
            info_print("  Could not expand (might not be a short link)")

    # 3. Парсинг домена
    parsed = urlparse(url)
    domain = parsed.netloc
    info_print(f"  Domain: {domain}")

    # 4. Базовая проверка на фишинг
    is_suspicious, reason = check_phishing_domains(url)
    if is_suspicious:
        warning_print(f"  ⚠ SUSPICIOUS: {reason}")
    else:
        success_print("  No obvious phishing indicators found")

    # 5. Протокол
    protocol = "HTTPS (secure)" if parsed.scheme == "https" else "HTTP (not secure)"
    if parsed.scheme == "https":
        success_print(f"  Protocol: {protocol}")
    else:
        error_print(f"  Protocol: {protocol}")

    # 6. Параметры
    if parsed.query:
        info_print(f"  Query parameters: {parsed.query[:100]}...")
    else:
        info_print("  No query parameters")

    # 7. Путь
    if parsed.path and parsed.path != "/":
        info_print(f"  Path: {parsed.path[:100]}...")

    print("=" * 60)
    info_print("  NOTE: This is a basic check. Always be cautious with unknown links!")
    print("=" * 60)

    gradient_input("\n└─$ Press Enter to continue...")


# ========== MAIN MENU ==========
def main():
    while True:
        clear_screen()
        show_banner()

        choice = gradient_input("\n└─$ Choose tool (0-9): ").strip()

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
        elif choice == '9':
            link_analyzer()
        elif choice == '0' or choice.lower() == 'exit':
            success_print("\n[+] Thanks for using StarSoft! Goodbye!\n")
            sys.exit()
        else:
            error_print("  ✗ Invalid choice! Enter number 0-9")
            time.sleep(1.5)


# ========== RUN ==========
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        success_print("\n\n[+] Program terminated. Goodbye!\n")
    except Exception as e:
        error_print(f"\n✗ Error: {e}")
        gradient_input("Press Enter to exit...")
