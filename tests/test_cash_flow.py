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

def test_cash_flow_2(ROR0124):
    from malloc.polish_bond_value.bond import CashFlowEvent    

    fr = ROR0124.cash_flow.loc[dt.date(2023, 2, 14)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(0.56, 0.001)

    fr = ROR0124.cash_flow.loc[dt.date(2023, 9, 14)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(0.56, 0.001)


def test_cash_flow_3(DOR1024):
    from malloc.polish_bond_value.bond import CashFlowEvent

    fr = DOR1024.cash_flow.loc[dt.date(2022, 11, 1)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(0.57, 0.001)

    fr = DOR1024.cash_flow.loc[dt.date(2023, 11, 1)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(0.51, 0.001)


def test_cash_flow_4(TOS0626):
    from malloc.polish_bond_value.bond import CashFlowEvent

    print(TOS0626.cash_flow)

    fr = TOS0626.cash_flow.loc[dt.date(2022, 11, 1)]
    assert fr["event"] == CashFlowEvent.coupon
    assert fr["value"] == pytest.approx(0.57, 0.001)

    