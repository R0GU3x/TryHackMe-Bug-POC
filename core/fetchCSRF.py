import json
import requests
import core.colors as colors

def get_csrf_token_simple(cookies_file="core/cookies.data"):
    """Simplified function to just get the CSRF token"""
    
    # Load cookies
    with open(cookies_file, 'r') as f:
        cookies_data = json.load(f)
    
    cookies = {c['name']: c['value'] for c in cookies_data}
    
    # Make request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "*/*",
        "Referer": "https://tryhackme.com/room/kothfoodctf"
    }
    
    response = requests.get(
        "https://tryhackme.com/api/v2/auth/csrf",
        headers=headers,
        cookies=cookies
        # verify=False
    )
    
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