from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from .schemas.device import Device, DeviceIn
from .schemas.command import Command, Scene
from sqlalchemy.orm import Session
from .database import DB_INITIALIZER
from . import crud, config
import typing
import logging
from fastapi.logger import logger

# setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=2,
    format="%(levelname)-9s %(message)s"
)

# load config
cfg: config.Config = config.load_config()

logger.info(
    'Service configuration loaded:\n' +
    f'{cfg.json(by_alias=True, indent=4)}'
)

# init database
logger.info('Initializing database...')
SessionLocal = DB_INITIALIZER.init_database(cfg.postgres_dsn)



app = FastAPI(
    version='0.0.2',
    title='Device Management Service'
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/devices", status_code=201, response_model=Device,
    summary='Добавляет устройство в базу'
)
async def add_device(device: DeviceIn, db: Session = Depends(get_db)) -> Device :
    return crud.create_device(db=db, device=device)

@app.get(
    "/devices",
    summary='Возвращает список устройств',
    response_model=list[Device]
)
async def get_device_list(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
    ) -> typing.List[Device] :
    return crud.get_devices(db, skip, limit)

@app.get("/devices/{deviceId}", summary='Возвращает информацию об устройстве')
async def get_device_info(
        deviceId: int, db: Session = Depends(get_db)
    ) -> Device :
    device = crud.get_device(db, deviceId)
    if device != None:
        return device
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.put("/devices/{deviceId}", summary='Обновляет информацию об устройстве')
async def update_device(
        deviceId: int, 
        device: DeviceIn,
        db: Session = Depends(get_db)
    ) -> Device :

    device = crud.update_device(db, deviceId, device)
    if device != None:
        return device
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.delete("/devices/{deviceId}", summary='Удаляет устройство из базы')
async def delete_device(
        deviceId: int, db: Session = Depends(get_db)
    ) -> Device :
    if crud.delete_device(db, deviceId):
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.get("/devices/{deviceId}/fetch", summary='Инициирует запрос актуальной информации с устройства')
async def fetch_device_data(deviceId: int) -> Device :
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.post("/devices/{deviceId}/command", summary='Посылает команду на устройство')
async def execute_device_command(deviceId: int, command: Command) -> Device :
    return JSONResponse(status_code=404, content={"message": "Item not found"})