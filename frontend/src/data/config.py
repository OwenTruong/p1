from pydantic import BaseModel, Field
from typing import Literal

class Config(BaseModel):
  mode: Literal["Production", "Development"] = Field(examples=["Production", "Development"])
  backend_url: str = Field(min_length=8, examples=["127.0.0.1:8080", "10.0.1.4"])
  fastapi_port: int = Field(ge=0, le=65535, examples=[80, 443, 5000, 8080, 25500])