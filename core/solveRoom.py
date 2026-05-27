import requests
import json
import core.colors as colors

def parse_cookies_from_json(cookie_json):
    """
    Convert cookie JSON array to dictionary format for requests library.
    
    Args:
        cookie_json: List of cookie objects from browser export
    
    Returns:
        Dictionary with cookie names as keys and values as values
    """
    cookies_dict = {}
    
    for cookie in cookie_json:
        name = cookie.get('name')
        value = cookie.get('value', '')
        if name:  # Only add if name exists
            cookies_dict[name] = value
    
    return cookies_dict

def send_tryhackme_request(cookies_dict, token:str):
    
    answer=""
    question_no=1
    room_code="kothfoodctf"
    task_id="5ea8b5ddfcb6902dd202bcc6"

    # Headers
    headers = {
        'Host': 'tryhackme.com',
        'Connection': 'keep-alive',
        'sec-ch-ua-full-version-list': '"Chromium";v="148.0.0.0", "Brave";v="148.0.0.0", "Not/A)Brand";v="99.0.0.0"',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua': '"Chromium";v="148", "Brave";v="148", "Not/A)Brand";v="99"',
        'sec-ch-ua-bitness': '"64"',
        # 'csrf-token': cookies_dict.get('_csrf', ''),  # Use CSRF token from cookies
        'csrf-token': token,
        'sec-ch-ua-mobile': '?0',
        'baggage': 'sentry-environment=production,sentry-release=next-production-9b7ce0bc26,sentry-public_key=175180b5f191796714d2f9138c06c76a,sentry-trace_id=ecfbf111a41d46e8bc8836e183d9720a,sentry-org_id=4507096022450176,sentry-transaction=%2Froom%2F%3AroomCode,sentry-sampled=false,sentry-sample_rand=0.6679653990159166,sentry-sample_rate=0.05',
        'sentry-trace': 'ecfbf111a41d46e8bc8836e183d9720a-a0625aab7507229d-0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-arch': '"x86"',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'Sec-GPC': '1',
        'Accept-Language': 'en-US,en;q=0.7',
        'Origin': 'https://tryhackme.com',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': f'https://tryhackme.com/room/{room_code}',
        'Accept-Encoding': 'gzip, deflate, br, zstd'
    }
    
    # POST data
    data = {
        "answer": answer,
        "questionNo": question_no,
        "roomCode": room_code,
        "taskId": task_id
    }
    
    # Send POST request
    try:
        print(colors.BRIGHT_YELLOW, end='')
        response = requests.post(
            'https://tryhackme.com/api/v2/rooms/answer',
            headers=headers,
            cookies=cookies_dict,
            json=data
            # verify=False  # Equivalent to curl's -k flag
        )
        print(colors.RESET)
        
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"{colors.BG_RED}Error making request: {colors.RED}{e}{colors.RESET}")
        return None

def main(token:str):
    try:
        # Read cookie data from cookies.data file
        with open("core/cookies.data", 'r', encoding='utf-8') as file:
            cookie_json = json.load(file)
        
        # print(f"Successfully loaded cookie data from cookies.data")
        # print(f"Found {len(cookie_json)} cookie entries")
        # print("-" * 50)
        
        # Parse the cookie JSON to dictionary
        cookies_dict = parse_cookies_from_json(cookie_json)
        
        # print(f"Parsed {len(cookies_dict)} cookies for the request")
        # print("-" * 50)
        
        # Optional: Print cookie names (uncomment for debugging)
        # print("Cookie names loaded:")
        # for name in cookies_dict.keys():
        #     print(f"  - {name}")
        # print("-" * 50)
        
        # Send the request
        response = send_tryhackme_request(cookies_dict, token)
        
        if response:
            # print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                # print("✓ Success! Got 200 OK response")
                try:
                    response_json = response.json()
                    # print(f"Response: {json.dumps(response_json, indent=2)}")
                    streak = response_json["data"]["currentStreak"]
                    # print(f"{colors.BRIGHT_GREEN}Room Solved: {colors.BOLD}200 OK{colors.RESET}")
                    print(f"{colors.BRIGHT_GREEN}{colors.BOLD}[✓]{colors.RESET} Room Solved: 200 OK")
                    print(f"{colors.BRIGHT_CYAN}{colors.BOLD}[i]{colors.RESET} Current Streak: {colors.BRIGHT_YELLOW}{streak}{colors.RESET}")
                except:
                    print(f"Response Text: {colors.BG_BRIGHT_RED}{response.text}{colors.RESET}")
            else:
                print(f"{colors.BRIGHT_RED}{colors.BOLD}✗{colors.RESET} Expected {colors.BRIGHT_GREEN}200{colors.RESET} but got {colors.BRIGHT_RED}{response.status_code}{colors.RESET}")
                print(f"Response: {colors.BG_RED}{response.text}{colors.RESET}")
        else:
            print(f"{colors.RED}Request failed{colors.RESET}")
            
    except FileNotFoundError:
        print(f"{colors.BG_RED}Error: cookies.data file not found in the current directory!{colors.RESET}")
        print(f"{colors.BG_RED}Please create a cookies.data file with the cookie JSON data.{colors.RESET}")
    except json.JSONDecodeError as e:
        print(f"{colors.BG_RED}Error parsing cookies.data: Invalid JSON format{colors.RESET}")
        print(f"{colors.BG_RED}Details: {e}{colors.RESET}")
    except Exception as e:
        print(f"{colors.BG_RED}Unexpected error: {e}{colors.RESET}")

if __name__ == "__main__":
    main()