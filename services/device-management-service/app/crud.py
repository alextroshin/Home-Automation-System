import typing
from sqlalchemy.orm import Session
from .database import models
from . import schemas

def create_device(
        db: Session, device: schemas.DeviceIn
    ) -> models.Device:
    '''
    Создает новое устройство в БД
    '''
    db_device = models.Device(
        name = device.name,
        description = device.description,
        ieee_address = device.ieee_address,
        info = device.info
    )

    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

def get_devices(
        db: Session, skip: int = 0, limit: int = 100
    ) -> typing.List[models.Device]:
    '''
    Возвращает инфомрмациб об устройствах
    '''
    return  db.query(models.Device) \
            .offset(skip) \
            .limit(limit) \
            .all()

def get_device(
        db: Session, device_id: int
    ) -> models.Device:
    '''
    Возвращает информацию о конкретном устройстве
    '''
    return  db.query(models.Device) \
            .filter(models.Device.id == device_id) \
            .first()

def update_device(
        db: Session, device_id: int, device: schemas.DeviceIn
    ) -> models.Device:
    '''
    Обновляет информацию об устройстве
    '''
    result =    db.query(models.Device) \
                .filter(models.Device.id == device_id) \
                .update(device.dict())
    db.commit()

    if result == 1:
        return get_device(db, device_id)
    return None


def delete_device(
        db: Session, device_id: int
    ) -> bool:
    '''
    Удаляет информацию об устройстве
    '''
    result =    db.query(models.Device) \
                .filter(models.Device.id == device_id) \
                .delete()
    db.commit()
    return result == 1