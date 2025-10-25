from pydantic import BaseModel, ConfigDict
from app.models.external_account import AccountType


# Shared properties
class ExternalAccountBase(BaseModel):
    account_type: AccountType
    username: str

# Properties to receive on item creation
class ExternalAccountCreate(ExternalAccountBase):
    access_token: str

# Properties to return to client
class ExternalAccount(ExternalAccountBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)