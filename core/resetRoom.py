import json
import requests
from urllib.parse import urlencode
import core.colors as colors
import subprocess

def load_cookies_from_file(filename="core/cookies.data"):
    """Load cookies from JSON file and convert to requests cookie format"""
    with open(filename, 'r') as f:
        cookies_data = json.load(f)
    
    cookies = {}
    for cookie in cookies_data:
        # Only add cookies that are valid (not expired)
        # Skip session cookies without expiration if you want
        cookies[cookie['name']] = cookie['value']
    
    return cookies

def open_cookies_file(filename="core/cookies.data"):
    with open(filename, 'w') as f:
        json.dump({
            "name": "Fetch the new cookies from you browser and paste them here.",
            "value": "Eating expired cookies leads to constipation"
        }, f)
    try:
        proc = subprocess.Popen(['notepad.exe', filename])
        proc.wait()
    except Exception as e:
        print(f"{colors.BRIGHT_RED}{colors.BOLD}[✗]{colors.RESET} Failed to open {filename}: {e}")

def main(token:str):
    """Send POST request to reset room progress"""
    
    # Load cookies from file
    try:
        cookies = load_cookies_from_file("core/cookies.data")
    except FileNotFoundError:
        print(f"{colors.BRIGHT_RED}{colors.BOLD}[✗]{colors.RESET} Error: cookies.data file not found in current directory")
        return False
    except json.JSONDecodeError as e:
        print(f"{colors.BRIGHT_RED}{colors.BOLD}[✗]{colors.RESET} Error parsing cookies.data: {e}")
        return False
    
    # Request details
    url = "https://tryhackme.com/api/v2/rooms/reset-progress"
    
    # Headers (excluding Cookie header as we'll use cookies parameter)
    headers = {
        "Host": "tryhackme.com",
        "Connection": "keep-alive",
        "sec-ch-ua-full-version-list": '"Chromium";v="148.0.0.0", "Brave";v="148.0.0.0", "Not/A)Brand";v="99.0.0.0"',
        "sec-ch-ua-platform": '"Windows"',
        "sec-ch-ua": '"Chromium";v="148", "Brave";v="148", "Not/A)Brand";v="99"',
        "sec-ch-ua-bitness": '"64"',
        "csrf-token": token,
        "sec-ch-ua-mobile": "?0",
        "baggage": "sentry-environment=production,sentry-release=next-production-9b7ce0bc26,sentry-public_key=175180b5f191796714d2f9138c06c76a,sentry-trace_id=4056f949fa6d41089a778a0c6fc67744,sentry-org_id=4507096022450176,sentry-transaction=%2Froom%2F%3AroomCode,sentry-sampled=false,sentry-sample_rand=0.28631364669556547,sentry-sample_rate=0.05",
        "sentry-trace": "4056f949fa6d41089a778a0c6fc67744-99b07d82de7eea94-0",
        "sec-ch-ua-model": '""',
        "sec-ch-ua-arch": '"x86"',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "accept": "application/json",
        "content-type": "application/json",
        "sec-ch-ua-platform-version": '"19.0.0"',
        "Sec-GPC": "1",
        "Accept-Language": "en-US,en;q=0.7",
        "Origin": "https://tryhackme.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://tryhackme.com/room/kothfoodctf",
        "Accept-Encoding": "gzip, deflate, br, zstd"
    }
    
    # Request body
    data = {"roomCode": "kothfoodctf"}

    while True:
    
        try:
            # Send POST request
            print(colors.BRIGHT_YELLOW, end='')
            response = requests.post(
                url,
                headers=headers,
                cookies=cookies,
                json=data  # This automatically sets content-type to application/json
                # verify=False  # Equivalent to curl's -k flag (skip SSL verification)
            )
            print(colors.RESET)
            
            # print(f"Response Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print(f"{colors.BRIGHT_GREEN}{colors.BOLD}[✓]{colors.RESET} Room Reset: 200 OK")
                # try:
                #     print(f"Response Body: {response.json()}")
                # except:
                #     print(f"Response Body: {response.text}")
                return True
            else:
                print(f"{colors.BRIGHT_RED}{colors.BOLD}[✗]{colors.RESET} Request failed with status code: {response.status_code}")
                print(f"Response: {colors.RED}{response.text}{colors.RESET}")
                print(f"\n{colors.BRIGHT_BLUE}[!]{colors.RESET} Try updating the {colors.BRIGHT_CYAN}{colors.BOLD}cookies.data{colors.RESET_BOLD}{colors.RESET} file")
                print(f'\n', "=" * 60, '\n')
                # return False
                open_cookies_file() # for manual updation
                return False
            
        except requests.exceptions.RequestException as e:
            print(f"{colors.BRIGHT_RED}{colors.BOLD}[✗]{colors.RESET} Error making request: {e}")
            return False

if __name__ == "__main__":
    success = main()