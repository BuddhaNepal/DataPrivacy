"""Retrieve the test user info.

Retrieve the test user info by calling the get_test_user_services API.
"""

import destroyer

def main():
    test_user_service = destroyer.get_test_user_services()
    url = destroyer.HOST + test_user_service[0]['url']

    # Get the designated test user
    test_user = destroyer.call_api(destroyer.RequestMethod.get, url)

    destroyer.output(test_user)

if __name__ == "__main__":
