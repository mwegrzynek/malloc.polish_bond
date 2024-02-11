import datetime as dt


import pytest


def test_cash_flow_1(COI0924):
    from malloc.polish_bond_value.bond import CashFlowEvent

    fr = COI0924.cash_flow.loc[dt.date(2021, 9, 14)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(1.3, 0.001)

    fr = COI0924.cash_flow.loc[dt.date(2022, 9, 14)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(5.75, 0.001)