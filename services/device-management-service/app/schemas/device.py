from pydantic import BaseModel, Field
from typing import Optional

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

class DeviceBase(BaseModel):
    '''
    Базовая модель устройства
    '''
    name:str = Field(title='Название устройства')
    description: Optional[str] = Field(title='Краткое описание устройства')
    ieee_address: str = Field(title='IEEEE-адрес устройства')
    info: dict = Field(title='Информация об устройстве', default=FAKE_DEVICE_INFO)

    class Config:
        orm_mode = True

class Device(DeviceBase):
    '''
    Модель используемая при запросе информации об устройстве
    '''
    id: int = Field(title='Идентификатор устройства', default=None)

class DeviceIn(DeviceBase):
    '''
    Модель для добавления/обновления устройства, т.к при добавлении/обновлении
    id не передается или передается через url, а не через тело запроса
    '''
    pass