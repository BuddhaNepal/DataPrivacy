"""Check user consent compliance status.

Check the consent compliance status of a user by calling /compliance API endpoint.
"""

import requests
import output

def main():
    url = 'http://localhost:8000/compliance?user_id=0&feature_id=0'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    response = requests.get(url, headers=headers)
    if response.ok:
        output.printJson(response.json())
    else:
        print(response.raise_for_status())


if __name__ == "__main__":
