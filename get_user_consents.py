"""Get consents of a user.

Retrieve the consents of a users by calling /user-consents API endpoint.
"""

import requests
import output

def main():
    url = 'http://localhost:8000/user-consents?user_id=0'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    response = requests.get(url, headers=headers)
    if response.ok:
        output.printTable(response.json())
    else:
        print(response.raise_for_status())


if __name__ == "__main__":
