from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app import models

class BaseCollector(ABC):
    """
    Abstract base class for all external event collectors.
    """
    def __init__(self, db: Session, provider: models.external_account.Provider):
        self.db = db
        self.provider = provider

    @abstractmethod
    def collect(self, user: models.User, account: models.external_account.ExternalAccount) -> int:
        """
        Collects events for a specific user and their external account.

        :param user: The user for whom to collect data.
        :param account: The external account to use for collection.
        :return: The number of new interactions collected.
        """
        pass
