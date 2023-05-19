"""Check the legal hold status of the test user.

Call E Discovery service to check the legal hold status of the test user.
"""

import destroyer

def main():
    test_user_service = destroyer.get_test_user_services()
    url = destroyer.HOST + test_user_service[0]['url']

    # Get the designated test user
    test_user = destroyer.call_api(destroyer.RequestMethod.get, url)

    user_id = test_user['id']
    url = destroyer.LEGAL_HOLD_API + "?user_id=" + str(user_id)

    # Get the legal hold status of the test user
    can_i_delete = destroyer.call_api(destroyer.RequestMethod.get, url)
    destroyer.output(can_i_delete)

if __name__ == "__main__":
