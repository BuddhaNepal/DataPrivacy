""Reset database back to the initial state.

Reset the database by calling /reset-db API endpoint.
"""

import requests
import output

def main():
    url = 'http://localhost:8000/reset-db'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    response = requests.get(url, headers=headers)
    if response.ok:
        output.printJson(response.json())
    else:
        print(response.raise_for_status())


if __name__ == "__main__":
