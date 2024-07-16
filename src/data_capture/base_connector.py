from abc import ABC, abstractmethod
import logging

class BaseConnector(ABC):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    async def get_data(self):
        pass

    async def validate_data(self, data):
        # Implement basic validation logic here
        if not data:
            raise ValueError("Data is empty")
        return data

    async def safe_get_data(self):
        try:
            data = await self.get_data()
            return await self.validate_data(data)
        except Exception as e:
            self.logger.error(f"Error getting data: {str(e)}")
            return None