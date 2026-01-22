import decimal as dec
from datetime import datetime

from custom_bar.bar_divider.price_bar_divider.price_bar_divider import PriceDivider


class TestPriceDivider:
    def test_init(self) -> None:
        restriction = dec.Decimal('1000.0')
        divider = PriceDivider(restriction)
        assert divider._restriction == restriction

    def test_calc_bar_restriction_no_args(self) -> None:
        restriction = dec.Decimal('1000.0')
        divider = PriceDivider(restriction)
        result = divider.calc_bar_restriction()
        assert result == restriction

    def test_calc_bar_restriction_with_args(self) -> None:
        restriction = dec.Decimal('500.0')
        divider = PriceDivider(restriction)
        
        test_time = datetime(2023, 1, 1, 10, 0)
        result = divider.calc_bar_restriction(test_time)
        assert result == restriction

    def test_calc_bar_restriction_with_kwargs(self) -> None:
        restriction = dec.Decimal('2000.0')
        divider = PriceDivider(restriction)
        
        result = divider.calc_bar_restriction(for_date_time=datetime(2023, 1, 1))
        assert result == restriction

    def test_calc_bar_restriction_ignores_parameters(self) -> None:
        restriction = dec.Decimal('1500.0')
        divider = PriceDivider(restriction)
        
        result = divider.calc_bar_restriction(
            datetime(2023, 1, 1),
            some_param="value",
            another_param=123
        )
        assert result == restriction

    def test_different_restrictions(self) -> None:
        restrictions = [
            dec.Decimal('100.0'),
            dec.Decimal('1000.0'),
            dec.Decimal('10000.0'),
            dec.Decimal('0.1')
        ]
        
        for restriction in restrictions:
            divider = PriceDivider(restriction)
            result = divider.calc_bar_restriction()
            assert result == restriction