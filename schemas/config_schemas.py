from pydantic import BaseModel

class ConfigSchema(BaseModel):
    value: str
