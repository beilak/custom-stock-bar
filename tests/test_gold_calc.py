import decimal as dec
import pandas as pd
from datetime import datetime

from custom_bar.bar_divider.gold_bar_divider.gold_calc import GoldBarCalc
from custom_bar.bar_divider.gold_bar_divider.gold_models import GoldBar, GoldBarTypes


class TestGoldBarCalc:
    def test_init(self) -> None:
        gold_df = pd.DataFrame({
            'date_time': [datetime(2023, 1, 1)],
            'close': [60.0]
        })
        calc = GoldBarCalc(gold_df)
        assert calc._gold_df.equals(gold_df)

    def test_calc_gold_price_gram(self) -> None:
        gold_df = pd.DataFrame({
            'date_time': [
                datetime(2023, 1, 1, 9, 0),
                datetime(2023, 1, 1, 10, 0),
                datetime(2023, 1, 1, 11, 0)
            ],
            'close': [59.0, 60.0, 61.0]
        })
        calc = GoldBarCalc(gold_df)
        
        gold_bar = GoldBar(count=1, bar_type=GoldBarTypes.GRAM)
        test_time = datetime(2023, 1, 1, 10, 30)
        
        result = calc.calc_gold_price(gold_bar, test_time)
        expected = round(dec.Decimal('60.0') * dec.Decimal('1'), 4)
        assert result == expected

    def test_calc_gold_price_troy_ounce(self) -> None:
        gold_df = pd.DataFrame({
            'date_time': [datetime(2023, 1, 1, 9, 0)],
            'close': [60.0]
        })
        calc = GoldBarCalc(gold_df)
        
        gold_bar = GoldBar(count=1, bar_type=GoldBarTypes.T_OUNCE)
        test_time = datetime(2023, 1, 1, 10, 0)
        
        result = calc.calc_gold_price(gold_bar, test_time)
        expected = round(dec.Decimal('60.0') * dec.Decimal('31.1034768'), 4)
        assert result == expected

    def test_calc_gold_price_kilogram(self) -> None:
        gold_df = pd.DataFrame({
            'date_time': [datetime(2023, 1, 1, 9, 0)],
            'close': [60.0]
        })
        calc = GoldBarCalc(gold_df)
        
        gold_bar = GoldBar(count=1, bar_type=GoldBarTypes.KG)
        test_time = datetime(2023, 1, 1, 10, 0)
        
        result = calc.calc_gold_price(gold_bar, test_time)
        expected = round(dec.Decimal('60.0') * dec.Decimal('1000'), 4)
        assert result == expected

    def test_calc_gold_price_multiple_units(self) -> None:
        gold_df = pd.DataFrame({
            'date_time': [datetime(2023, 1, 1, 9, 0)],
            'close': [60.0]
        })
        calc = GoldBarCalc(gold_df)
        
        gold_bar = GoldBar(count=5, bar_type=GoldBarTypes.GRAM)
        test_time = datetime(2023, 1, 1, 10, 0)
        
        result = calc.calc_gold_price(gold_bar, test_time)
        expected = round(dec.Decimal('60.0') * dec.Decimal('5'), 4)
        assert result == expected

    def test_calc_gold_price_exact_time_match(self) -> None:
        test_time = datetime(2023, 1, 1, 10, 0)
        gold_df = pd.DataFrame({
            'date_time': [
                datetime(2023, 1, 1, 9, 0),
                test_time,
                datetime(2023, 1, 1, 11, 0)
            ],
            'close': [59.0, 60.0, 61.0]
        })
        calc = GoldBarCalc(gold_df)
        
        gold_bar = GoldBar(count=1, bar_type=GoldBarTypes.GRAM)
        
        result = calc.calc_gold_price(gold_bar, test_time)
        expected = round(dec.Decimal('60.0') * dec.Decimal('1'), 4)
        assert result == expected

    def test_calc_gold_price_uses_latest_before_time(self) -> None:
        gold_df = pd.DataFrame({
            'date_time': [
                datetime(2023, 1, 1, 9, 0),
                datetime(2023, 1, 1, 10, 0),
                datetime(2023, 1, 1, 11, 0)
            ],
            'close': [59.0, 60.0, 61.0]
        })
        calc = GoldBarCalc(gold_df)
        
        gold_bar = GoldBar(count=1, bar_type=GoldBarTypes.GRAM)
        test_time = datetime(2023, 1, 1, 10, 30)
        
        result = calc.calc_gold_price(gold_bar, test_time)
        expected = round(dec.Decimal('60.0') * dec.Decimal('1'), 4)
        assert result == expected

    def test_calc_gold_price_rounding(self) -> None:
        gold_df = pd.DataFrame({
            'date_time': [datetime(2023, 1, 1, 9, 0)],
            'close': [60.123456]
        })
        calc = GoldBarCalc(gold_df)
        
        gold_bar = GoldBar(count=1, bar_type=GoldBarTypes.T_OUNCE)
        test_time = datetime(2023, 1, 1, 10, 0)
        
        result = calc.calc_gold_price(gold_bar, test_time)
        
        unrounded = dec.Decimal('60.123456') * dec.Decimal('31.1034768')
        expected = round(unrounded, 4)
        assert result == expected

    def test_calc_gold_price_gost_28058(self) -> None:
        gold_df = pd.DataFrame({
            'date_time': [datetime(2023, 1, 1, 9, 0)],
            'close': [60.0]
        })
        calc = GoldBarCalc(gold_df)
        
        gold_bar = GoldBar(count=1, bar_type=GoldBarTypes.KG_11)
        test_time = datetime(2023, 1, 1, 10, 0)
        
        result = calc.calc_gold_price(gold_bar, test_time)
        expected = round(dec.Decimal('60.0') * dec.Decimal('11000'), 4)
        assert result == expected

    def test_calc_gold_price_400_troy_ounce(self) -> None:
        gold_df = pd.DataFrame({
            'date_time': [datetime(2023, 1, 1, 9, 0)],
            'close': [60.0]
        })
        calc = GoldBarCalc(gold_df)
        
        gold_bar = GoldBar(count=1, bar_type=GoldBarTypes.T_OUNCE_400)
        test_time = datetime(2023, 1, 1, 10, 0)
        
        result = calc.calc_gold_price(gold_bar, test_time)
        expected = round(dec.Decimal('60.0') * dec.Decimal('31.1034768') * dec.Decimal('400'), 4)
        assert result == expected