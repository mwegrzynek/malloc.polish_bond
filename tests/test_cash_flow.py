import datetime as dt


import pytest


from malloc.polish_bond.bond import CashFlowEvent


def test_cash_flow_1(COI0924):
    fr = COI0924.cash_flow.loc[dt.date(2021, 9, 14)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(1.3, 0.001)

    fr = COI0924.cash_flow.loc[dt.date(2022, 9, 14)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(5.75, 0.001)


def test_cash_flow_2(ROR0124):
    fr = ROR0124.cash_flow.loc[dt.date(2023, 2, 14)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(0.56, 0.001)

    fr = ROR0124.cash_flow.loc[dt.date(2023, 9, 14)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(0.56, 0.001)


def test_cash_flow_3(DOR1024):
    fr = DOR1024.cash_flow.loc[dt.date(2022, 11, 1)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(0.57, 0.001)

    fr = DOR1024.cash_flow.loc[dt.date(2023, 11, 1)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(0.51, 0.001)


def test_cash_flow_4(TOZ0624):
    fr = TOZ0624.cash_flow.loc[dt.date(2022, 6, 12)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(1., 0.001)

    fr = TOZ0624.cash_flow.loc[dt.date(2023, 12, 12)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(3.48, 0.001)


    
    