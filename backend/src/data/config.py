from pydantic import BaseModel, Field
from typing import Literal

class Config(BaseModel):
  db_host: str = Field(examples=["localhost"])
  db_name: str = Field(examples=["my_db"])
  db_user: str = Field(examples=["my_db_user"])
  db_password: str = Field(examples=["MyVeryImportantPassword"])
  mode: Literal["Production", "Development"] = Field(examples=["Production", "Development"])
  jwt_secret_key: str = Field(min_length=8, examples=["MyVeryImportantSecret"])
  jwt_algorithm: str = Field(examples=["HS256"])
  backend_port: int = Field(ge=0, le=65535, examples=[80, 443, 5000, 8080, 25500])