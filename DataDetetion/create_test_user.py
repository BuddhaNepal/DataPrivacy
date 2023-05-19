"""Create a test user.

Create a test user by calling the User services API.
"""

import destroyer

def main():
    test_user_service = destroyer.get_test_user_services()
    url = destroyer.HOST + test_user_service[0]['url']

    # Get the designated test user - service will create one if not exists
    test_user = destroyer.call_api(destroyer.RequestMethod.get, url)
    print("Created test user: " + test_user['email'])

if __name__ == "__main__":
