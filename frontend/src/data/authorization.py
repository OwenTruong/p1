from pydantic import BaseModel, Field

class Authorization(BaseModel):
  is_authenticated: bool = Field(default=False, examples=[True, False])
  username: str | None = Field(default=None, examples=[None, "test_dev"])
  error_message: str | None = Field(default=None, examples=[None, 'Session has expired. Please re-authenticate'])