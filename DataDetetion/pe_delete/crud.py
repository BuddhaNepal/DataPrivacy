from sqlalchemy.orm import Session
from pe_delete import database, models, schemas
from faker import Faker
from shutil import copyfile

fake = Faker()
Faker.seed(4321)


def reset_db(db: Session):
    copyfile(database.MASTER_DB_FILE, database.WORKING_DB_FILE)
    return


def get_legal_hold(db: Session, user_id: int):
    return db.query(models.EDiscovery).filter(models.EDiscovery.id == user_id).first()


def get_deletion_service(db: Session, deletion_service_id: int):
    return db.query(models.DeletionService).filter(models.DeletionService.id == deletion_service_id).first()


def get_deletion_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DeletionService).offset(skip).limit(limit).all()


def create_deletion_service(db: Session, deletion_service: schemas.DeletionServiceCreate):
    db_deletion_service = models.DeletionService(
        **deletion_service.dict())
    db.add(db_deletion_service)
    db.commit()
    db.refresh(db_deletion_service)
    return db_deletion_service


def delete_deletion_service(db: Session, deletion_service_id: int):

    db_result = db.query(models.DeletionService).filter(
        models.DeletionService.id == deletion_service_id).delete()
    db.commit()
    return db_result


def get_deletion_apis(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DeletionAPI).offset(skip).limit(limit).all()


def get_deletion_apis_by_type(db: Session, api_type: models.APIType, api_field: models.APIFieldType):
    apis_by_type = db.query(models.DeletionAPI).filter(models.DeletionAPI.api_type == api_type.value).filter(
        models.DeletionAPI.api_field == api_field.value).all()
    return apis_by_type


def create_deletion_service_api(db: Session, deletion_API: schemas.DeletionAPICreate, deletion_service_id: int):
    db_deletion_API = models.DeletionAPI(
        **deletion_API.dict(), deletion_service_id=deletion_service_id)
    db.add(db_deletion_API)
    db.commit()
    db.refresh(db_deletion_API)
    return db_deletion_API


def delete_deletion_api(db: Session, deletion_api_id: int):

    db_result = db.query(models.DeletionAPI).filter(
        models.DeletionAPI.id == deletion_api_id).delete()
    db.commit()
    return db_result


# Orig
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_ssn(db: Session, ssn: str):
    return db.query(models.User).filter(models.User.ssn == ssn).all()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def delete_user(db: Session, user_id: int):

    db_result = db.query(models.User).filter(
        models.User.id == user_id).delete()
    db.commit()
    return db_result


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    user_fields = user.dict()
    user_fields.pop('password')
    db_user = models.User(
        **user_fields, hashed_password=fake_hashed_password)
    db_user.e_discovery = models.EDiscovery()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_fake_user():
    fake_user = fake.profile()
    fake_user.pop('current_location', None)
    fake_user.pop('website', None)
    fake_user.pop('residence', None)
    fake_user['email'] = fake_user.pop('mail', "missing@missing.com")
    fake_user['birthdate'] = str(fake_user.pop('birthdate', None))
    password = fake.password()

    user = schemas.UserCreate(**fake_user, password=password)
    return user


def create_test_user(db: Session):
    user = create_fake_user()
    user.name = models.TEST_USER_NAME
    return create_user(db, user)
