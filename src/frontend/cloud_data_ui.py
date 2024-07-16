import gradio as gr
from src.cloud_management.data_retrieval import DataRetrieval
from src.cloud_management.data_sync import DataSync

data_retrieval = DataRetrieval('your-s3-bucket-name')
data_sync = DataSync('/path/to/local/directory', 'your-s3-bucket-name')

def list_cloud_footage():
    return data_retrieval.list_footage()

def download_footage(object_key):
    local_path = f"/path/to/downloads/{object_key.split('/')[-1]}"
    success = data_retrieval.download_footage(object_key, local_path)
    return f"Downloaded to {local_path}" if success else "Download failed"

def sync_to_cloud():
    data_sync.sync_to_cloud()
    return "Sync to cloud completed"

def sync_from_cloud():
    data_sync.sync_from_cloud()
    return "Sync from cloud completed"

with gr.Blocks() as cloud_data_ui:
    gr.Markdown("# Cloud Data Management")
    
    with gr.Tab("Browse Footage"):
        list_button = gr.Button("List Cloud Footage")
        footage_list = gr.Dropdown(label="Select Footage")
 