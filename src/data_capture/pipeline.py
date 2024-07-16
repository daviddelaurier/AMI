import asyncio
from src.data_capture.obs_connector import OBSConnector
from src.data_capture.camera_connector import CameraConnector
from src.data_capture.sensor_connector import SensorConnector
from src.backend.core import process_data

class DataPipeline:
    def __init__(self):
        self.obs_connector = OBSConnector()
        self.camera_connector = CameraConnector()
        self.sensor_connector = SensorConnector()
        self.data_queue = asyncio.Queue()

    async def collect_data(self):
        while True:
            obs_data = await self.obs_connector.get_data()
            camera_data = await self.camera_connector.get_data()
            sensor_data = await self.sensor_connector.get_data()
            
            combined_data = {
                'obs': obs_data,
                'camera': camera_data,
                'sensor': sensor_data
            }
            
            await self.data_queue.put(combined_data)

    async def process_data(self):
        while True:
            data = await self.data_queue.get()
            processed_data = process_data(data)
            # Store or further process the data as needed
            print(f"Processed data: {processed_data}")

    async def run(self):
        await asyncio.gather(
            self.collect_data(),
            self.process_data()
        )

# Usage
pipeline = DataPipeline()
asyncio.run(pipeline.run())