def test_dataset_info():
    from malloc.polish_bond.bond import BondMaker
    dsi = BondMaker.get_dataset_info()    
    assert dsi.file_url.endswith(".xls")