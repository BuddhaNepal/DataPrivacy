import requests
import json
import enum
from pe_delete import models

from rich.console import Console
from rich.syntax import Syntax


def output(value_to_ouput):
    syntax = Syntax(json.dumps(value_to_ouput, indent=2), "python",
                    theme="monokai", line_numbers=True)
    console = Console()
    console.print(syntax)


headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}

HOST = "http://localhost:8000"
LEGAL_HOLD_API = HOST + "/e-discovery/legal-hold"
DELETION_SERVICES_BY_TYPE_API = HOST + "/deletion-service-apis-by-type"
DELETION_SERVICES_BY_ID = HOST + "/deletion-services/"


class RequestMethod(enum.Enum):
    get = "get"
    delete = "delete"
    post = "post"


def call_api(request_method, url):

    try:
        if (request_method == RequestMethod.get):
            response = requests.get(url, headers=headers)
        elif (request_method == RequestMethod.delete):
            response = requests.delete(url, headers=headers)
        elif (request_method == RequestMethod.post):
            response = requests.post(url, headers=headers)

        if response.ok:
            data = response.json()
        else:
            print(response.raise_for_status())

    except requests.exceptions.RequestException as e:
        print(e)
        data = response.json()

    return data


def get_user_delete_services():
    field_type = models.APIFieldType.user_id
    api_type = models.APIType.delete
    url = DELETION_SERVICES_BY_TYPE_API + "?api_type=" + \
        api_type.value + "&api_field=" + field_type.value
    delete_user_services = call_api(RequestMethod.get, url)
    return delete_user_services


def get_test_user_services():
    field_type = models.APIFieldType.user_id
    api_type = models.APIType.get_test_user
    url = DELETION_SERVICES_BY_TYPE_API + "?api_type=" + \
        api_type.value + "&api_field=" + field_type.value
    test_user_services = call_api(RequestMethod.get, url)
    return test_user_services


def get_is_deleted_services():
    field_type = models.APIFieldType.user_id
    api_type = models.APIType.is_deleted
    url = DELETION_SERVICES_BY_TYPE_API + "?api_type=" + \
        api_type.value + "&api_field=" + field_type.value
    is_deleted_user_services = call_api(RequestMethod.get, url)
    return is_deleted_user_services


def main():
    test_user_services = get_test_user_services()
    output(test_user_services)

    user_delete_services = get_user_delete_services()
    output(user_delete_services)

    is_deleted_user_services = get_is_deleted_services()
    output(is_deleted_user_services)

    # audit test users
    for test_user_service in test_user_services:
        url = HOST + test_user_service['url']
        test_user = call_api(RequestMethod.get, url)
        output(test_user)

        user_id = test_user['id']

        url = LEGAL_HOLD_API + "?user_id=" + str(user_id)
        can_i_delete = call_api(RequestMethod.get, url)
        output(can_i_delete)

        # Get owning deletion service
        url = DELETION_SERVICES_BY_ID + \
            str(test_user_service['deletion_service_id'])
        parent_service = call_api(RequestMethod.get, url)
        output(parent_service)

        delete_api = next((api for api in parent_service['apis']
                        if api['api_type'] == models.APIType.delete), None)

        output(parent_service)

        delete_url = HOST + \
            delete_api['url'] + "?" + delete_api['api_field'] + \
            "=" + str(test_user['id'])
        delete_response = call_api(RequestMethod.delete, delete_url)
        output(delete_response)

        output(test_user)

        url = LEGAL_HOLD_API + "?user_id=10"
        can_i_delete = call_api(RequestMethod.get, url)
        output(can_i_delete)


if __name__ == "__main__":
