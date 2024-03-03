import datetime as dt


from pydantic import BaseModel, AnyHttpUrl
import requests


DATASET_INFO_URL: AnyHttpUrl = "https://api.dane.gov.pl/1.4/datasets/805,podstawowe-informacje-na-temat-obligacji-detalicznych/resources"


class DatasetInfo(BaseModel):

    description: str
    data_date: dt.date
    file_url: str

    @classmethod
    def get_dataset_info(cls) -> "DatasetInfo":
        """Find the dataset info of the bond Excel data."""
        attrs = requests.get(DATASET_INFO_URL).json()["data"][0]["attributes"]
        return cls(**attrs)
