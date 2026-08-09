from auth import AUTHORIZATION_TOKEN, COOKIE
from utils import get_v5_id

TOP_HOLDING_COMPANIES_LIMIT = 10
X_DEVICE_ID = get_v5_id()
API_TIMEOUT = 15.0

GROWW_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": AUTHORIZATION_TOKEN,
    "cookie": COOKIE,
    "priority": "u=1, i",
    "referer": "https://groww.in/mutual-funds/filter",
    "sec-ch-ua": '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
    "x-app-id": "growwWeb",
    "x-device-id": X_DEVICE_ID,
    "x-device-id-v2": X_DEVICE_ID,
    "x-device-type": "desktop",
    "x-platform": "web",
    "x-primary-target": "td=1,au=1,ld=4",
    "x-secondary-target": "td=2,au=2,ld=3",
    "x-target-version": "0"
}
