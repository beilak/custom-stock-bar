import decimal as dec
from datetime import datetime
from unittest.mock import Mock

from custom_bar.bar_divider.gold_bar_divider.gold_bar_divider import GoldBarDivider
from custom_bar.bar_divider.gold_bar_divider.gold_calc import GoldBarCalc
from custom_bar.bar_divider.gold_bar_divider.gold_models import GoldBar, GoldBarTypes


class TestGoldBarDivider:
    def test_init(self) -> None:
        mock_calc = Mock(spec=GoldBarCalc)
        mock_bars = Mock(spec=GoldBar)
        
        divider = GoldBarDivider(mock_calc, mock_bars)
        assert divider._gold_bar_calc == mock_calc
        assert divider._gold_bars == mock_bars

    def test_calc_bar_restriction(self) -> None:
        mock_calc = Mock(spec=GoldBarCalc)
        mock_bars = Mock(spec=GoldBar)
        
        expected_price = dec.Decimal('1000.5')
        mock_calc.calc_gold_price.return_value = expected_price
        
        divider = GoldBarDivider(mock_calc, mock_bars)
        test_time = datetime(2023, 1, 1, 10, 0)
        
        result = divider.calc_bar_restriction(test_time)
        
        assert result == expected_price
        mock_calc.calc_gold_price.assert_called_once_with(
            gold_unit=mock_bars,
            for_date_time=test_time
        )

    def test_calc_bar_restriction_different_times(self) -> None:
        mock_calc = Mock(spec=GoldBarCalc)
        mock_bars = Mock(spec=GoldBar)
        
        mock_calc.calc_gold_price.side_effect = [
            dec.Decimal('1000.0'),
            dec.Decimal('1100.0'),
            dec.Decimal('900.0')
        ]
        
        divider = GoldBarDivider(mock_calc, mock_bars)
        
        times = [
            datetime(2023, 1, 1, 10, 0),
            datetime(2023, 1, 1, 11, 0),
            datetime(2023, 1, 1, 12, 0)
        ]
        
        results = [divider.calc_bar_restriction(time) for time in times]
        
        assert results[0] == dec.Decimal('1000.0')
        assert results[1] == dec.Decimal('1100.0')
        assert results[2] == dec.Decimal('900.0')
        
        assert mock_calc.calc_gold_price.call_count == 3

    def test_integration_with_real_gold_bar(self) -> None:
        mock_calc = Mock(spec=GoldBarCalc)
        mock_calc.calc_gold_price.return_value = dec.Decimal('50000.0')
        
        gold_bar = GoldBar(count=1, bar_type=GoldBarTypes.GRAM)
        divider = GoldBarDivider(mock_calc, gold_bar)
        
        test_time = datetime(2023, 1, 1, 10, 0)
        result = divider.calc_bar_restriction(test_time)
        
        assert result == dec.Decimal('50000.0')
        mock_calc.calc_gold_price.assert_called_once_with(
            gold_unit=gold_bar,
            for_date_time=test_time
        )