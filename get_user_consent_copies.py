"""Get locale-specific consent copies of a user.

Retrieve the locale-specific consent copies of a users by calling /locale-copies API endpoint.
"""

import requests
import pandas as pd
import output

def get_response(url):
    headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

    response = requests.get(url, headers=headers)
    if response.ok:
        data = response.json()
        return pd.DataFrame.from_records(data)
    else:
        print(response.raise_for_status())
        return pd.DataFrame()


def main():
    locale_copies = pd.DataFrame()
    consents =  get_response('http://localhost:8000/user-consents?user_id=0')
    if (not consents.empty):
        for copy in consents.loc[:, 'locale_copy_id']:
            locale_copy = get_response('http://localhost:8000/locale-copies/' + str(copy))
            locale_copies = locale_copy if locale_copies.empty else locale_copies.append(locale_copy)

    output.printTable(locale_copies)


if __name__ == "__main__":
