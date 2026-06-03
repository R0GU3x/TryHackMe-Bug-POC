import json
import requests
import core.colors as colors
import time

def get_csrf_token_simple(cookies_file="core/cookies.data"):
    """Simplified function to just get the CSRF token"""
    
    # Load cookies
    with open(cookies_file, 'r') as f:
        cookies_data = json.load(f)
    
    try:
        cookies = {c['name']: c['value'] for c in cookies_data}
    except (KeyError, TypeError) as e:
        print(f"{colors.BRIGHT_RED}{colors.BOLD}[✗]{colors.RESET} Error parsing cookies: {e}")
        return None

    # Make request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "*/*",
        "Referer": "https://tryhackme.com/room/kothfoodctf"
    }
    while True:
        try:
            response = requests.get(
                "https://tryhackme.com/api/v2/auth/csrf",
                headers=headers,
                cookies=cookies
                # verify=False
            )
            break
        except requests.exceptions.ConnectionError:
            print(f"{colors.RED}{colors.BOLD}✗ No Internet Connection. Retrying... {colors.RESET}", end='\r')
            time.sleep(1)

    if response.status_code == 200:
        data = response.json()
        if data.get('status') == 'success':
            token = data.get('data', {}).get('token')
            print(f"{colors.BRIGHT_GREEN}{colors.BOLD}[✓]{colors.RESET} CSRF Token Grabbed: {colors.BRIGHT_MAGENTA}{token}{colors.RESET}")
            return token
    
    return None

if __name__ == "__main__":
    token = get_csrf_token_simple()
    if token:
        print(f"Token: {token}")
    else:
        print("Failed to get token")