"""Check if the test user is deleted.

Call eDiscovery serice the check the legal hold status of the test user.
"""

import argparse
import destroyer

def main():

    parser = argparse.ArgumentParser(
        prog="check_user_deleted.py", description="Check if a user is deleted"
    )

    parser.add_argument(
        "user_id",
        type=int,
        nargs="?",
        help="user id to be checked",
        default=40001,      # default test user id if none is provided
    )

    user_id = parser.parse_args().user_id
    is_deleted_service = destroyer.get_is_deleted_services()
    url = destroyer.HOST + is_deleted_service[0]['url'] + "?user_id=" + str(user_id)

    # Check if the test user is deleted
    is_deleted = destroyer.call_api(destroyer.RequestMethod.get, url)
    destroyer.output(is_deleted)

if __name__ == "__main__":
    main()ubuntu@ip-172-31-3-4:/data/data-deletion$ cat delete_test_user.py 
"""Delete the test user.

Delete the test user by calling the User services API.
"""

import destroyer

def main():
    test_user_service = destroyer.get_test_user_services()
    url = destroyer.HOST + test_user_service[0]['url']

    # Get the designated test user
    test_user = destroyer.call_api(destroyer.RequestMethod.get, url)

    # Get owning deletion service
    url = destroyer.DELETION_SERVICES_BY_ID + \
        str(test_user_service[0]['deletion_service_id'])
    parent_service = destroyer.call_api(destroyer.RequestMethod.get, url)

    delete_api = next((api for api in parent_service['apis']
                    if api['api_type'] == destroyer.models.APIType.delete), None)

    delete_url = destroyer.HOST + \
        delete_api['url'] + "?" + delete_api['api_field'] + \
        "=" + str(test_user['id'])

    delete_response = destroyer.call_api(destroyer.RequestMethod.delete, delete_url)
    destroyer.output(delete_response)


if __name__ == "__main__":
