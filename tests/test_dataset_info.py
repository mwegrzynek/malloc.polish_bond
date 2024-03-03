def test_dataset_info():
    from malloc.polish_bond import DatasetInfo
    dsi = DatasetInfo.get_dataset_info()    
    assert dsi.file_url.endswith(".xls")