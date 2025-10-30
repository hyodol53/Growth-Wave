from pydantic import BaseModel, ConfigDict
from app.models.external_account import Provider

# Shared properties
class ExternalAccountBase(BaseModel):
    provider: Provider
    account_id: str

# Properties to receive on item creation
class ExternalAccountCreate(ExternalAccountBase):
    credentials: str # API Token, OAuth Token, etc.

# Properties to return to client (never include credentials)
class ExternalAccount(ExternalAccountBase):
    id: int

    model_config = ConfigDict(from_attributes=True)