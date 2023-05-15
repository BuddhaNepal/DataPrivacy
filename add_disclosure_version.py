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
    main()ubuntu@ip-172-31-4-121:/data/data-consent$ python check_compliance_status.py 
  1 {                                                                                            
  2   "compliance": true                                                                         
  3 }                                                                                            
ubuntu@ip-172-31-4-121:/data/data-consent$ cat add_disclosure_version.py 
"""Add a new consent disclosure versions.

Add a new consent disclosure versions by calling /disclosure-versions API endpoint.
"""

import requests
import output

def main():
    json = {
        "id": 100,
        "disclosure_version": 1.2,
        "disclosure_id": 0,

    }

    url = 'http://localhost:8000/disclosure-versions?disclosure_id=0'
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    response = requests.post(url, headers=headers, json=json)
    if response.ok:
        output.printJson(response.json())
    else:
        print(response.raise_for_status())


if __name__ == "__main__":
