from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from pe_delete import crud, models, schemas, database
import uvicorn

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


# Dependency
def get_db():
    db = database.SessionLocal()
    db.execute("PRAGMA foreign_keys = ON")
    try:
        yield db
    finally:
        db.close()


@app.post("/reset-db/", status_code=status.HTTP_200_OK)
def reset_db(db: Session = Depends(get_db)):
    crud.reset_db(db=db)
    return {"reset-db": True}


@app.get("/e-discovery/legal-hold", status_code=status.HTTP_200_OK)
def e_discovery_legal_hold(user_id: int, db: Session = Depends(get_db)):
    e_discovery = crud.get_legal_hold(db, user_id=user_id)
    if (e_discovery == None):
        raise HTTPException(
            status_code=404, detail="User not found: " + str(user_id))

    return {"user_id": user_id,
            "legal_hold": e_discovery.legal_hold}


@app.get("/user-account/get-test-user", response_model=schemas.User, status_code=status.HTTP_200_OK)
def user_account_get_test_user(db: Session = Depends(get_db)):
    db_user = crud.get_user_by_name(db, name=models.TEST_USER_NAME)
    if db_user:
        return db_user
    else:
        return crud.create_test_user(db=db)


@app.get("/user-account/is-deleted", status_code=status.HTTP_200_OK)
def user_account_get_is_deleted(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    return {"is_deleted " + str(user_id): db_user == None}


@app.delete("/user-account/delete", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user_id = crud.delete_user(db, user_id=user_id)
    if (db_user_id == 0):
        raise HTTPException(
            status_code=404, detail="User not found: " + str(user_id))
    return {"delete user_id " + str(user_id): "success"}


@app.post("/deletion-services/", response_model=schemas.DeletionService, status_code=status.HTTP_201_CREATED)
def create_deletion_service(deletion_service: schemas.DeletionServiceCreate, db: Session = Depends(get_db)):
    return crud.create_deletion_service(db=db, deletion_service=deletion_service)


@app.get("/deletion-services/", response_model=List[schemas.DeletionService])
def read_deletion_services(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    deletion_services = crud.get_deletion_services(db, skip=skip, limit=limit)
    return deletion_services


@app.get("/deletion-services/{deletion_service_id}", response_model=schemas.DeletionService)
def read_deletion_service(deletion_service_id: int, db: Session = Depends(get_db)):
    db_deletion_service = crud.get_deletion_service(
        db, deletion_service_id=deletion_service_id)
    if db_deletion_service is None:
        raise HTTPException(
            status_code=404, detail="Deletion Service not found")
    return db_deletion_service


@app.delete("/deletion-services/{deletion_service_id}", status_code=status.HTTP_200_OK)
def delete_deletion_service(deletion_service_id: int, db: Session = Depends(get_db)):
    db_deletion_service_id = crud.delete_deletion_service(
        db, deletion_service_id=deletion_service_id)
    if (db_deletion_service_id == 0):
        raise HTTPException(
            status_code=404, detail="Deletion Service not found")
    return

####


@app.post("/deletion-service-apis/{deletion_service_id}", response_model=schemas.DeletionAPI, status_code=status.HTTP_201_CREATED)
def create_deletion_service_api(deletion_service_id: int, deletion_api: schemas.DeletionAPICreate, db: Session = Depends(get_db)):
    return crud.create_deletion_service_api(db=db, deletion_API=deletion_api, deletion_service_id=deletion_service_id)


@app.get("/deletion-service-apis/", response_model=List[schemas.DeletionAPI])
def read_deletion_service_apis(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    deletion_service_apis = crud.get_deletion_apis(
        db, skip=skip, limit=limit)
    return deletion_service_apis


@app.get("/deletion-service-apis-by-type", response_model=List[schemas.DeletionAPI])
def read_deletion_service_apis_by_type(api_type: models.APIType, api_field: models.APIFieldType, db: Session = Depends(get_db)):
    return (crud.get_deletion_apis_by_type(db, api_type=api_type, api_field=api_field))


@app.delete("/deletion-service-apis/{deletion_api_id}", status_code=status.HTTP_200_OK)
def delete_deletion_service(deletion_api_id: int, db: Session = Depends(get_db)):
    db_deletion_api_id = crud.delete_deletion_service(
        db, deletion_api_id=deletion_api_id)
    if (db_deletion_api_id == 0):
        raise HTTPException(
            status_code=404, detail="Deletion Service not found")
    return


@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users_by_ssn", response_model=List[schemas.User])
def users_by_ssn(ssn: str, db: Session = Depends(get_db)):
    return (crud.get_user_by_ssn(db, ssn=ssn))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
