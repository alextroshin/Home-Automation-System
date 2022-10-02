from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .schemas.device import Device, DeviceBase
from .schemas.command import Command, Scene
import typing

FAKE_DEVICE_INFO =  {
        "ieee_address":"0x00158d00018255df",
        "type":"Router",
        "network_address":29159,
        "supported": True,
        "friendly_name":"my_plug",
        "description":"this plug is in the kitchen",
        "endpoints":{"1":{"bindings":[],"configured_reportings":[],"clusters":{"input":["genOnOff","genBasic"],"output":[]}}},
        "definition":{
            "model":"ZNCZ02LM",
            "vendor":"Xiaomi",
            "description":"Mi power plug ZigBee",
            "options": [],
            "exposes": []  
        },
        "power_source":"Mains (single phase)",
        "date_code":"02-28-2017",
        "model_id":"lumi.plug",
        "scenes": [{"id": 3, "name": "Chill scene"}],
        "interviewing":False,
        "interview_completed":True
    }

app = FastAPI(
    version='0.0.1',
    title='Device Management Service'
)
devices: typing.Dict[int, Device] = {}

@app.post(
    "/devices", status_code=201, response_model=Device,
    summary='Добавляет устройство в базу'
)
async def add_device(device: DeviceBase) -> Device :
    result = Device(
        **device.dict(),
        id=len(devices) + 1,
        info=FAKE_DEVICE_INFO
    )
    devices[result.id] = result
    return result

@app.get("/devices", summary='Возвращает список устройств', response_model=list[Device])
async def get_device_list() -> typing.Iterable[Device] :
    return [ v for k,v in devices.items() ]

@app.get("/devices/{deviceId}", summary='Возвращает информацию об устройстве')
async def get_device_info(deviceId: int) -> Device :
    if deviceId in devices: return devices[deviceId]
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.put("/devices/{deviceId}", summary='Обновляет информацию об устройстве')
async def update_device(deviceId: int, device: DeviceBase) -> Device :
    if deviceId in devices:
        result = Device(
            **device.dict(),
            id=deviceId,
            info=FAKE_DEVICE_INFO
        )
        devices[deviceId] = result
        return devices[deviceId]
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.delete("/devices/{deviceId}", summary='Удаляет устройство из базы')
async def delete_device(deviceId: int) -> Device :
    if deviceId in devices:
        del devices[deviceId]
        return JSONResponse(status_code=200, content={"message": "Item successfully deleted"})
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.get("/devices/{deviceId}/fetch", summary='Инициирует запрос актуальной информации с устройства')
async def fetch_device_data(deviceId: int) -> Device :
    if deviceId in devices: return devices[deviceId]
    return JSONResponse(status_code=404, content={"message": "Item not found"})

@app.post("/devices/{deviceId}/command", summary='Посылает команду на устройство')
async def execute_device_command(deviceId: int, command: Command) -> Device :
    if deviceId in devices: return devices[deviceId]
    return JSONResponse(status_code=404, content={"message": "Item not found"})