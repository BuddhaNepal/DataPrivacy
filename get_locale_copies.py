"""Get consent disclosure locale copies.

Retrieve the consent disclosure locale copies by calling /locale-copies API endpoint.
"""

import requests
import output

def main():
    url = 'http://localhost:8000/locale-copies?disclosure_version_id=1'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    response = requests.get(url, headers=headers)
    if response.ok:
        output.printTable(response.json())
    else:
        print(response.raise_for_status())


if __name__ == "__main__":
