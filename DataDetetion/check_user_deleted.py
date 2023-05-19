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
