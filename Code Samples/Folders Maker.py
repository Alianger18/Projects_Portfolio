import os
base_path   = "F:\IT Pro\Python Developper"
source_path =  f"{base_path}\data\source\downloaded_at=2021-01-01\ppr-all.zip"
def create_directory_if_not_exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return None
create_directory_if_not_exists(source_path)