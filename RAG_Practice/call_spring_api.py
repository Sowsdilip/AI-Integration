import requests
import re

BASE_URL = "http://localhost:8080/api/lc/"


def get_lc_status(lc_number: str):
    lc_number = lc_number.strip().upper()
    check = re.fullmatch(r"[A-Z0-9-]{3,16}",lc_number)     
    if not check:
        return "invalid LC number format",True
    url = BASE_URL + f"{lc_number}"
    print(f"url  {url}")
    try:
        resp = requests.get(url, timeout=5)
    except requests.RequestException as e:
        print(f"excetion details {e}")
        return f"LC service unavailable: try later", True
    print(resp)
    print(resp.status_code)
    if resp.ok:
        return resp.text, False
    elif resp.status_code == 404:
        return resp.json().get("detail","LC not found"), True
    else:
        print(f"exception details code = {resp.status_code} message = {resp.text[:200]}")
        return f"Exception with status code {resp.status_code} while processing request", True


if __name__ == "__main__":
    lc_number = "L@C-11"
    print(lc_number)
    response = get_lc_status(lc_number)
    print(response)
