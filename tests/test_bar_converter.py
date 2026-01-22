import decimal as dec
import pandas as pd
from datetime import datetime
from unittest.mock import Mock

from custom_bar.converter.bar_converter import BarConverter
from custom_bar.converter.models import PriceBarModel
from custom_bar.converter.protocols.divider_protocol import BarDividerProtocol


class TestBarConverter:
    def test_init(self) -> None:
        mock_divider = Mock(spec=BarDividerProtocol)
        converter = BarConverter(mock_divider)
        assert converter._bar_divider == mock_divider

    def test_aggregate_price(self) -> None:
        ohlc_data = pd.Series({
            'open': 100.0,
            'high': 110.0,
            'low': 95.0,
            'close': 105.0
        })
        result = BarConverter._aggregate_price(ohlc_data)
        expected = (100.0 + 110.0 + 95.0 + 105.0) / 4
        assert result == expected

    def test_make_output_df(self) -> None:
        price_bars = [
            PriceBarModel(
                date_time=datetime(2023, 1, 1, 10, 0),
                open=dec.Decimal('100.0'),
                high=dec.Decimal('110.0'),
                low=dec.Decimal('95.0'),
                close=dec.Decimal('105.0'),
                volume=1000
            )
        ]
        df = BarConverter._make_output_df(price_bars)
        
        assert len(df) == 1
        assert set(df.columns) == {"date_time", "open", "high", "low", "close", "volume"}
        assert df.index[0] == datetime(2023, 1, 1, 10, 0)
        assert df.iloc[0]["open"] == dec.Decimal('100.0')

    def test_make_custom_bars_empty_data(self) -> None:
        mock_divider = Mock(spec=BarDividerProtocol)
        converter = BarConverter(mock_divider)
        
        empty_df = pd.DataFrame(columns=[
            'date_time', 'open', 'high', 'low', 'close', 'volume'
        ])
        result = converter.make_custom_bars(empty_df)
        assert len(result) == 0

    def test_make_custom_bars_single_bar(self) -> None:
        mock_divider = Mock(spec=BarDividerProtocol)
        mock_divider.calc_bar_restriction.return_value = dec.Decimal('1000.0')
        converter = BarConverter(mock_divider)
        
        trades = pd.DataFrame({
            'date_time': [datetime(2023, 1, 1, 10, 0)],
            'open': [100.0],
            'high': [105.0],
            'low': [95.0],
            'close': [102.0],
            'volume': [10]
        })
        
        result = converter.make_custom_bars(trades)
        assert len(result) == 1
        mock_divider.calc_bar_restriction.assert_called_once()

    def test_make_custom_bars_multiple_bars(self) -> None:
        mock_divider = Mock(spec=BarDividerProtocol)
        mock_divider.calc_bar_restriction.return_value = dec.Decimal('500.0')
        converter = BarConverter(mock_divider)
        
        trades = pd.DataFrame({
            'date_time': [
                datetime(2023, 1, 1, 10, 0),
                datetime(2023, 1, 1, 10, 1),
                datetime(2023, 1, 1, 10, 2),
                datetime(2023, 1, 1, 10, 3)
            ],
            'open': [100.0, 101.0, 102.0, 103.0],
            'high': [105.0, 106.0, 107.0, 108.0],
            'low': [95.0, 96.0, 97.0, 98.0],
            'close': [102.0, 103.0, 104.0, 105.0],
            'volume': [10, 10, 10, 10]
        })
        
        result = converter.make_custom_bars(trades)
        assert len(result) >= 1

    def test_make_custom_bars_last_row_handling(self) -> None:
        mock_divider = Mock(spec=BarDividerProtocol)
        mock_divider.calc_bar_restriction.return_value = dec.Decimal('10000.0')
        converter = BarConverter(mock_divider)
        
        trades = pd.DataFrame({
            'date_time': [
                datetime(2023, 1, 1, 10, 0),
                datetime(2023, 1, 1, 10, 1)
            ],
            'open': [100.0, 101.0],
            'high': [105.0, 106.0],
            'low': [95.0, 96.0],
            'close': [102.0, 103.0],
            'volume': [10, 10]
        })
        
        result = converter.make_custom_bars(trades)
        assert len(result) == 1