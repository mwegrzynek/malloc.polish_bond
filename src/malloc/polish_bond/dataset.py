import datetime as dt


from pydantic import BaseModel
import requests


class DatasetInfo(BaseModel):
    _dataset_info_url = "https://api.dane.gov.pl/1.4/datasets/805,podstawowe-informacje-na-temat-obligacji-detalicznych/resources"
    
    description: str
    data_date: dt.date
    file_url: str

    @classmethod
    def get_dataset_info(cls) -> "DatasetInfo":
        """Find the dataset info of the bond Excel data."""        
        attrs = requests.get(cls.dataset_info_url).json()["data"][0]["attributes"]        
        return cls(**attrs)
    