from pydantic import BaseModel
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

    class Config:
        from_attributes = True