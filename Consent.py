from fastapi import FastAPI, HTTPException


from fastapi.responses import JSONResponse
import sqlite3
from sqlite3 import Error
import uvicorn
from pydantic import BaseModel

import create_db

description = """
This is the API documentation supporting the live lab section of the Data Consent module.
"""

tags_metadata = [
    {
        "name": "db",
        "description": "Helper API to reset status to the original database state",
    },
    {
        "name": "compliance",
        "description": "Check compliance status of user with a feature.",
    },
    {
        "name": "users",
        "description": "Operations with users.",
    },
    {
        "name": "features",
        "description": "Operations with features.",
    },
    {
        "name": "disclosures",
        "description": "Operations with disclosures.",
    },
    {
        "name": "disclosure_versions",
        "description": "Operations with disclosure versions.",
    },
    {
        "name": "locale_copies",
        "description": "Operations with locale copies.",
    },
    {
        "name": "user_consents",
        "description": "Operations with user_consents.",
    },
]

DB_FILE = "data/consent.db"


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # conn.row_factory = sqlite3.Row
        return conn
    except Error as e:
        print(e)

    return conn


conn = create_connection(DB_FILE)

if conn is None:
    print("Cannot connect to DB")
    exit()


api = FastAPI(
    title="Data Protocol Privacy Engineering Consent Live Lab",
    description=description,
    version="1.0.0",
    contact={
        "name": "Data Protocol",
        "url": "https://dataprotocol.com/contact",
        "email": "info@dataprotocol.com",
    },
    license_info={
        "name": "MIT LICENSE",
        "url": "https://github.com/Data-Protocol/data-consent/blob/main/LICENSE",
    },
    openapi_tags=tags_metadata,
)


def calculate_compliance(user_id, feature_id):
    print("user_id= ", user_id)
    print("feature_id= ", feature_id)

    cur = conn.cursor()

    cur.execute("SELECT name, locale FROM user WHERE id=?", (user_id,))
    user = cur.fetchone()
    if user is None:
        raise HTTPException(status_code=400, detail="User not valid")

    cur.execute("SELECT disclosure_id FROM feature WHERE id=?", (feature_id,))
    disclosure = cur.fetchone()
    if disclosure is None:
        raise HTTPException(status_code=400, detail="Feature not valid")
    else:
        disclosure_id = disclosure[0]

    print("disclosure_id= ", disclosure_id)

    cur.execute("""SELECT id FROM disclosure_version
                   WHERE disclosure_id=? ORDER BY disclosure_version DESC""", (disclosure_id,))
    latest_disclosure_version = cur.fetchone()
    if latest_disclosure_version is None:
        # if there is no disclosure version for a disclosure, a user cannot be compliant
        return False
    else:
        latest_disclosure_version_id = latest_disclosure_version[0]

    print("latest_disclosure_version_id= ", latest_disclosure_version_id)

    cur.execute("""SELECT locale_copy_id FROM user_consent
                   WHERE disclosure_id=? AND user_id=? ORDER BY time DESC""", (disclosure_id, user_id,))
    locale_copy = cur.fetchone()
    if locale_copy is None:
        # if there is no user consent for a disclosure, a user cannot be compliant
        return False
    else:
        locale_copy_id = locale_copy[0]

    print("locale_copy_id= ", locale_copy_id)

    cur.execute("""SELECT disclosure_version_id FROM locale_copy
                   WHERE id=?""", (locale_copy_id,))
    user_disclosure_version = cur.fetchone()
    if user_disclosure_version is None:
        # if there is no user consent for a disclosure, a user cannot be compliant
        raise HTTPException(status_code=500, detail="Invalid locale_copy_id")
    else:
        user_disclosure_version_id = user_disclosure_version[0]

    print("user_disclosure_version_id= ", user_disclosure_version_id)

    return user_disclosure_version_id == latest_disclosure_version_id


# start crud apis
delete_table_sql = {
    "delete_user": "DELETE FROM user WHERE id = ",
    "delete_feature": "DELETE FROM feature WHERE id = ",
    "delete_disclosure": "DELETE FROM disclosure WHERE id = ",
    "delete_disclosure_version": "DELETE FROM disclosure_version WHERE id = ",
    "delete_locale_copy": "DELETE FROM locale_copy WHERE id = ",
    "delete_user_consent": "DELETE FROM user_consent WHERE id = "
}


def delete_db(con, key, id):
    cur = con.cursor()

    try:
        query = delete_table_sql[key] + str(id)
        print(query)

        result = cur.execute(query)
        if (result.rowcount == 0):
            raise HTTPException(status_code=404, detail="Resource not found")
        con.commit()
        return {"deleted": "True"}

    except sqlite3.Error as err:
        print(err)
        # detail = "args not valid: " + ''.join(args.dict().values)
        raise HTTPException(
            status_code=400, detail=str(err))


add_table_sql = {
    "add_user": "INSERT INTO user",
    "add_feature": "INSERT INTO feature",
    "add_disclosure": "INSERT INTO disclosure",
    "add_disclosure_version": "INSERT OR REPLACE INTO disclosure_version",
    "add_locale_copy": "INSERT INTO locale_copy",
    "add_user_consent": "INSERT INTO user_consent"
}


def add_db(con, key, args):
    cur = con.cursor()

    try:
        arg_dict = args.dict()
        columns = ', '.join(arg_dict.keys())
        placeholders = ':'+', :'.join(arg_dict.keys())
        query = add_table_sql[key] + \
            ' (%s) VALUES (%s)' % (columns, placeholders)
        print(query)

        cur.execute(query, arg_dict)
        con.commit()
        args.id = cur.lastrowid
        return args

    except sqlite3.Error as err:
        print(err)
        # detail = "args not valid: " + ''.join(args.dict().values)
        raise HTTPException(
            status_code=400, detail=str(err))


get_table_sql = {
    "user_consent_by_id": "SELECT * FROM user_consent WHERE id=? ORDER BY id DESC",
    "user_consent_by_user_id": "SELECT * FROM user_consent WHERE user_id=? ORDER BY id DESC",
    "user_consent_all": "SELECT * FROM user_consent ORDER BY id DESC",

    "locale_copy_by_id": "SELECT * FROM locale_copy WHERE id=? ORDER BY time DESC",
    "locale_copy_by_disclosure_version_id": "SELECT * FROM locale_copy WHERE disclosure_version_id=? ORDER BY time DESC",
    "locale_copy_all": "SELECT * FROM locale_copy ORDER BY time DESC",

    "user_by_id": "SELECT * FROM user WHERE id=? ORDER BY id ASC",
    "user_all": "SELECT * FROM user ORDER BY id ASC",

    "disclosure_version_by_id": "SELECT * FROM disclosure_version WHERE id=? ORDER BY id DESC",
    "disclosure_version_by_disclosure_id": "SELECT * FROM disclosure_version WHERE disclosure_id=? ORDER BY id DESC",
    "disclosure_version_all": "SELECT * FROM disclosure_version ORDER BY id DESC",

    "disclosure_by_id": "SELECT * FROM disclosure WHERE id=? ORDER BY id DESC",
    "disclosure_all": "SELECT * FROM disclosure ORDER BY id DESC",

    "feature_by_id": "SELECT * FROM feature WHERE id=? ORDER BY id DESC",
    "feature_all": "SELECT * FROM feature ORDER BY id DESC"
}


def get_db(con, key, args):
    cur = con.cursor()
    if (args == None):
        cur.execute(get_table_sql[key])
    else:
        cur.execute(get_table_sql[key], (args,))

    db_result = cur.fetchall()

    if (db_result is None) or (len(db_result) == 0):
        detail = "args not valid: " + str(args)
        raise HTTPException(
            status_code=400, detail=detail)

    response = []
    columns = [desc[0] for desc in cur.description]
    for row in db_result:
        summary = dict(zip(columns, row))
        response.append(summary)

    return JSONResponse(content=response)


# API interface

@api.get("/reset-db", tags=["db"], description="This resets the database to the original state")
async def reset_db():

    global conn

    conn.close()
    create_db.main()
    conn = create_connection(DB_FILE)

    if conn is None:
        print("Cannot connect to DB")
        raise HTTPException(
            status_code=500, detail="Cannot reset database - fatal error")
    else:
        response = {"success":  True}
        return response


@api.get("/compliance", tags=["compliance"], description="This checks if a user is compliant")
async def get_compliance(user_id: int, feature_id: int):

    compliance = calculate_compliance(user_id, feature_id)
    response = {"compliance":  compliance}
    # json_compatible_item_data = jsonable_encoder(dict)
    return JSONResponse(content=response)


# User

class User(BaseModel):
    id: int
    name: str
    locale: str


@api.post("/users", tags=["users"], description="Add a new user")
async def add_user(user: User):
    return add_db(conn, "add_user", user)


@api.delete("/users/{user_id}", tags=["users"], description="Delete a user")
async def delete_user(user_id: int):
    return delete_db(conn, "delete_user", user_id)


@api.get("/users/{user_id}", tags=["users"], description="Get individual user")
async def get_users_by_id(user_id: int):
    return get_db(conn, "user_by_id", user_id)


@api.get("/users", tags=["users"], description="Get all users")
async def get_users():
    return get_db(conn, "user_all", None)


# User Consents

class UserConsent(BaseModel):
    id: int
    disclosure_id: int
    locale_copy_id: int


@api.post("/user-consents", tags=["user_consents"], description="Add a new user consent")
async def add_user_consent(user_consent: UserConsent):
    return add_db(conn, "add_user_consent", user_consent)


@api.delete("/user_consents/{user_consent_id}", tags=["user_consents"], description="Delete a user consent")
async def delete_user_consent(user_consent_id: int):
    return delete_db(conn, "delete_user_consent", user_consent_id)


@api.get("/user-consents", tags=["user_consents"], description="Get individual user consent or get all if no id specified")
async def get_user_consent_by_user_id(user_id: int = None):
    if (user_id == None):
        return get_db(conn, "user_consent_all", None)
    else:
        return get_db(conn, "user_consent_by_user_id", user_id)


@api.get("/user-consents/{user_consent_id}", tags=["user_consents"])
async def get_user_consent_by_id(user_consent_id: int):
    return get_db(conn, "user_consent_by_id", user_consent_id)


class LocaleCopy(BaseModel):
    id: int
    disclosure_version_id: int
    locale: str


@api.post("/locale-copies", tags=["locale_copies"], description="Add a new locale copy")
async def add_locale_copy(locale_copy: LocaleCopy):
    return add_db(conn, "add_locale_copy", locale_copy)


@api.delete("/locale-copies/{locale_copy_id}", tags=["locale_copies"], description="Delete a locale copy")
async def delete_locale_copy(locale_copy_id: int):
    return delete_db(conn, "delete_locale_copy", locale_copy_id)


@api.get("/locale-copies", tags=["locale_copies"], description="Get all local copies for a disclosure_version_id or get all")
async def get_locale_copy_by_disclosure_version(disclosure_version_id: int):
    if (disclosure_version_id == None):
        return get_db(conn, "locale_copy_all", None)
    else:
        return get_db(conn, "locale_copy_by_disclosure_version_id", disclosure_version_id)


@api.get("/locale-copies/{locale_copy_id}", tags=["locale_copies"], description="Get individual local copy")
async def get_locale_copy_by_id(locale_copy_id: int):
    return get_db(conn, "locale_copy_by_id", locale_copy_id)


class Feature(BaseModel):
    id: int
    disclosure_id: int
    name: str


@api.post("/features", tags=["features"], description="Add a new feature")
async def add_feature(feature: Feature):
    return add_db(conn, "add_feature", feature)


@api.delete("/features/{feature_id}", tags=["features"], description="Delete a feature")
async def delete_feature(feature_id: int):
    return delete_db(conn, "delete_feature", feature_id)


@api.get("/features/{feature_id}", tags=["features"], description="Get individual feature")
async def get_feature(feature_id: int):
    return get_db(conn, "feature_by_id", feature_id)


@api.get("/features", tags=["features"], description="Get all features")
async def get_feature():
    return get_db(conn, "feature_all", None)


class Disclosure(BaseModel):
    id: int
    name: str


@api.post("/disclosures", tags=["disclosures"], description="Add a new disclosure")
async def add_disclosure(disclosure: Disclosure):
    return add_db(conn, "add_disclosure", disclosure)


@api.delete("/disclosures/{disclosure_id}", tags=["disclosures"], description="Delete a disclosure")
async def delete_disclosure(disclosure_id: int):
    return delete_db(conn, "delete_disclosure", disclosure_id)


@api.get("/disclosures/{disclosure_id}", tags=["disclosures"], description="Get individual disclosure")
async def get_disclosure_by_id(disclosure_id: int):
    return get_db(conn, "disclosure_by_id", disclosure_id)


@api.get("/disclosures", tags=["disclosures"], description="Get all disclosures")
async def get_disclosures():
    return get_db(conn, "disclosure_all", None)


class DisclosureVersion(BaseModel):
    id: int
    disclosure_version: float
    disclosure_id: int


@api.post("/disclosure-versions", tags=["disclosure_versions"], description="Add a new disclosure version")
async def add_disclosure_version(disclosure_version: DisclosureVersion):
    return add_db(conn, "add_disclosure_version", disclosure_version)


@api.delete("/disclosure-versions/{disclosure_version_id}", tags=["disclosure_versions"], description="Delete a disclosure version")
async def delete_disclosure_version(disclosure_version_id: int):
    return delete_db(conn, "delete_disclosure_version", disclosure_version_id)


@api.get("/disclosure-versions", tags=["disclosure_versions"], description="Get individual disclosure versions related to disclosure_id")
async def get_disclosure_versions_by_disclosure_id(disclosure_id: int):
    return get_db(conn, "disclosure_version_by_disclosure_id", disclosure_id)


@api.get("/disclosure-versions/{disclosure_version_id}", tags=["disclosure_versions"], description="Get individual disclosure version or get all if no id specified")
async def get_disclosure_version_by_id(disclosure_version_id: int):
    if(disclosure_version_id == None):
        return get_db(conn, "disclosure_version_all", None)
    else:
        return get_db(conn, "disclosure_version_by_id", disclosure_version_id)


if __name__ == "__main__":
    uvicorn.run(api, host="127.0.0.1", port=8000)
