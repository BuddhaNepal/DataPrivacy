"""Reset database back to the initial state.

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
    main()ubuntu@ip-172-31-4-121:/data/data-consent$ cat get_features.py 
"""Get consent features.

Retrieve the consent features by calling /features API endpoint.
"""

import requests
import output

def main():
    url = 'http://localhost:8000/features'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    response = requests.get(url, headers=headers)
    if response.ok:
        output.printTable(response.json())
    else:
        print(response.raise_for_status())


if __name__ == "__main__":
