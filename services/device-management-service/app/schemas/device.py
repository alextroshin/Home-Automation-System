from pydantic import BaseModel, Field
from typing import Optional


class DeviceBase(BaseModel):
    name:str = Field(title='Название устройства')
    description: Optional[str] = Field(title='Краткое описание устройства')
    ieee_address: str = Field(title='IEEEE-адрес устройства')

class Device(DeviceBase):
    id: int = Field(title='Идентификатор устройства')
    info: dict = Field(title='Информация об устройстве')