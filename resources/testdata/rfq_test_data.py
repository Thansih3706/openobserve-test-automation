GET_QUOTE_POSITIVE_CASES = [
    {
        "id": "buy_deliver_quantity",
        "title": "Get RFQ Quote - Buy BTC with USD deliver quantity",
        "payload_overrides": {
            "ticker": "BTC-USD",
            "tradeSide": "buy",
            "deliverQuantity": "100",
            "receiveQuantity": None,
        },
        "expected": {
            "symbol": "BTC-USD",
            "side": "buy",
            "deliverCurrency": "USD",
            "receiveCurrency": "BTC",
        },
    },
    {
        "id": "buy_receive_quantity",
        "title": "Get RFQ Quote - Buy BTC with BTC receive quantity",
        "payload_overrides": {
            "ticker": "BTC-USD",
            "tradeSide": "buy",
            "deliverQuantity": None,
            "receiveQuantity": "0.002",
        },
        "expected": {
            "symbol": "BTC-USD",
            "side": "buy",
            "deliverCurrency": "USD",
            "receiveCurrency": "BTC",
        },
    },
    {
        "id": "sell_deliver_quantity",
        "title": "Get RFQ Quote - Sell BTC with BTC deliver quantity",
        "payload_overrides": {
            "ticker": "BTC-USD",
            "tradeSide": "sell",
            "deliverQuantity": "0.002",
            "receiveQuantity": None,
        },
        "expected": {
            "symbol": "BTC-USD",
            "side": "sell",
            "deliverCurrency": "BTC",
            "receiveCurrency": "USD",
        },
    },
    {
        "id": "sell_receive_quantity",
        "title": "Get RFQ Quote - Sell BTC for USD receive quantity",
        "payload_overrides": {
            "ticker": "BTC-USD",
            "tradeSide": "sell",
            "deliverQuantity": None,
            "receiveQuantity": "100",
        },
        "expected": {
            "symbol": "BTC-USD",
            "side": "sell",
            "deliverCurrency": "BTC",
            "receiveCurrency": "USD",
        },
    },
]

CREATE_QUOTE_POSITIVE_CASES = [
    {
        "id": "buy_deliver_quantity",
        "title": "Create RFQ Quote - Buy BTC with USD deliver quantity",
        "payload_overrides": {
            "ticker": "BTC-USD",
            "tradeSide": "buy",
            "deliverQuantity": "100",
            "receiveQuantity": None,
        },
        "expected": {
            "symbol": "BTC-USD",
            "side": "buy",
            "deliverCurrency": "USD",
            "receiveCurrency": "BTC",
        },
    },
    {
        "id": "buy_receive_quantity",
        "title": "Create RFQ Quote - Buy BTC with BTC receive quantity",
        "payload_overrides": {
            "ticker": "BTC-USD",
            "tradeSide": "buy",
            "deliverQuantity": None,
            "receiveQuantity": "0.002",
        },
        "expected": {
            "symbol": "BTC-USD",
            "side": "buy",
            "deliverCurrency": "USD",
            "receiveCurrency": "BTC",
        },
    },
    {
        "id": "sell_deliver_quantity",
        "title": "Create RFQ Quote - Sell BTC with BTC deliver quantity",
        "payload_overrides": {
            "ticker": "BTC-USD",
            "tradeSide": "sell",
            "deliverQuantity": "0.002",
            "receiveQuantity": None,
        },
        "expected": {
            "symbol": "BTC-USD",
            "side": "sell",
            "deliverCurrency": "BTC",
            "receiveCurrency": "USD",
        },
    },
    {
        "id": "sell_receive_quantity",
        "title": "Create RFQ Quote - Sell BTC for USD receive quantity",
        "payload_overrides": {
            "ticker": "BTC-USD",
            "tradeSide": "sell",
            "deliverQuantity": None,
            "receiveQuantity": "100",
        },
        "expected": {
            "symbol": "BTC-USD",
            "side": "sell",
            "deliverCurrency": "BTC",
            "receiveCurrency": "USD",
        },
    },
]

CREATE_QUOTE_PRECEDENCE_CASES = [
    {
        "id": "buy_both_quantities_prefers_deliver",
        "title": "Create RFQ Quote - Buy with both quantities should prefer deliverQuantity",
        "payload_overrides": {
            "ticker": "BTC-USD",
            "tradeSide": "buy",
            "deliverQuantity": "100",
            "receiveQuantity": "999",
        },
        "expected": {
            "side": "buy",
            "deliverCurrency": "USD",
            "receiveCurrency": "BTC",
        },
    },
    {
        "id": "sell_both_quantities_prefers_receive",
        "title": "Create RFQ Quote - Sell with both quantities should prefer receiveQuantity",
        "payload_overrides": {
            "ticker": "BTC-USD",
            "tradeSide": "sell",
            "deliverQuantity": "999",
            "receiveQuantity": "100",
        },
        "expected": {
            "side": "sell",
            "deliverCurrency": "BTC",
            "receiveCurrency": "USD",
        },
    },
]

NEGATIVE_GET_CASES = [
    {
        "id": "missing_ticker",
        "title": "Get RFQ Quote - Missing ticker should fail",
        "payload_overrides": {"ticker": None},
        "expected_statuses": (400, 422),
    },
    {
        "id": "missing_account_id",
        "title": "Get RFQ Quote - Missing accountId should fail",
        "payload_overrides": {"accountId": None},
        "expected_statuses": (400, 422),
    },
    {
        "id": "missing_trade_side",
        "title": "Get RFQ Quote - Missing tradeSide should fail",
        "payload_overrides": {"tradeSide": None},
        "expected_statuses": (400, 422),
    },
    {
        "id": "missing_both_quantities",
        "title": "Get RFQ Quote - Missing both quantities should fail",
        "payload_overrides": {
            "deliverQuantity": None,
            "receiveQuantity": None,
        },
        "expected_statuses": (400, 422),
    },
    {
        "id": "invalid_trade_side",
        "title": "Get RFQ Quote - Invalid tradeSide should fail",
        "payload_overrides": {"tradeSide": "hold"},
        "expected_statuses": (400, 422),
    },
    {
        "id": "invalid_ticker_format",
        "title": "Get RFQ Quote - Invalid ticker format should fail",
        "payload_overrides": {"ticker": "BTCUSD"},
        "expected_statuses": (400, 403),
    },
    {
        "id": "unsupported_ticker",
        "title": "Get RFQ Quote - Unsupported ticker should fail",
        "payload_overrides": {"ticker": "BTC-XXX"},
        "expected_statuses": (400, 403),
    },
    {
        "id": "zero_deliver_quantity",
        "title": "Get RFQ Quote - Zero deliver quantity should fail",
        "payload_overrides": {
            "deliverQuantity": "0",
            "receiveQuantity": None,
        },
        "expected_statuses": (400, 422),
    },
    {
        "id": "negative_deliver_quantity",
        "title": "Get RFQ Quote - Negative deliver quantity should fail",
        "payload_overrides": {
            "deliverQuantity": "-1",
            "receiveQuantity": None,
        },
        "expected_statuses": (400, 422),
    },
    {
        "id": "non_numeric_deliver_quantity",
        "title": "Get RFQ Quote - Non numeric deliver quantity should fail",
        "payload_overrides": {
            "deliverQuantity": "abc",
            "receiveQuantity": None,
        },
        "expected_statuses": (400, 422,502),
    },
]

NEGATIVE_CREATE_CASES = [
    {
        "id": "missing_ticker",
        "title": "Create RFQ Quote - Missing ticker should fail",
        "payload_overrides": {"ticker": None},
        "expected_statuses": (400, 422, 502),
    },
    {
        "id": "missing_account_id",
        "title": "Create RFQ Quote - Missing accountId should fail",
        "payload_overrides": {"accountId": None},
        "expected_statuses": (400, 422, 502, 500),
    },
    {
        "id": "missing_trade_side",
        "title": "Create RFQ Quote - Missing tradeSide should fail",
        "payload_overrides": {"tradeSide": None},
        "expected_statuses": (400, 422),
    },
    {
        "id": "missing_both_quantities",
        "title": "Create RFQ Quote - Missing both quantities should fail",
        "payload_overrides": {
            "deliverQuantity": None,
            "receiveQuantity": None,
        },
        "expected_statuses": (400, 422, 502),
    },
    {
        "id": "invalid_trade_side",
        "title": "Create RFQ Quote - Invalid tradeSide should fail",
        "payload_overrides": {"tradeSide": "hold"},
        "expected_statuses": (400, 422, 502),
    },
    {
        "id": "invalid_ticker_format",
        "title": "Create RFQ Quote - Invalid ticker format should fail",
        "payload_overrides": {"ticker": "BTCUSD"},
        "expected_statuses": (400, 403),
    },
    {
        "id": "unsupported_ticker",
        "title": "Create RFQ Quote - Unsupported ticker should fail",
        "payload_overrides": {"ticker": "BTC-XXX"},
        "expected_statuses": (400, 403, 422, 502),
    },
    {
        "id": "zero_deliver_quantity",
        "title": "Create RFQ Quote - Zero deliver quantity should fail",
        "payload_overrides": {
            "deliverQuantity": "0",
            "receiveQuantity": None,
        },
        "expected_statuses": (400, 422, 500),
    },
    {
        "id": "negative_deliver_quantity",
        "title": "Create RFQ Quote - Negative deliver quantity should fail",
        "payload_overrides": {
            "deliverQuantity": "-1",
            "receiveQuantity": None,
        },
        "expected_statuses": (400, 422, 500),
    },
    {
        "id": "non_numeric_deliver_quantity",
        "title": "Create RFQ Quote - Non numeric deliver quantity should fail",
        "payload_overrides": {
            "deliverQuantity": "abc",
            "receiveQuantity": None,
        },
        "expected_statuses": (400, 422, 500, 502),
    },
    {
        "id": "same_currency_ticker_USD-USD",
        "title": "Create RFQ Quote - Same currency ticker should fail",
        "payload_overrides": {"ticker": "USD-USD"},
        "expected_statuses": (400, 422, 500, 502),
    },
    {
        "id": "same_currency_ticker_BTC-BTC",
        "title": "Create RFQ Quote - Same currency ticker should fail",
        "payload_overrides": {"ticker": "BTC-BTC"},
        "expected_statuses": (400, 422, 500, 502),
    },
]


EXECUTE_QUOTE_CASES = [
    {
        "id": "buy_receive_btc",
        "title": "Execute RFQ Quote - Buy BTC with BTC receive quantity",
        "payload_overrides": {
            "ticker": "BTC-USD",
            "tradeSide": "buy",
            "deliverQuantity": None,
            "receiveQuantity": "0.002",
        },
        "expected": {
            "symbol": "BTC-USD",
            "side": "buy",
            "deliverCurrency": "USD",
            "receiveCurrency": "BTC",
        },
    },
    {
        "id": "sell_deliver_btc",
        "title": "Execute RFQ Quote - Sell BTC with BTC deliver quantity",
        "payload_overrides": {
            "ticker": "BTC-USD",
            "tradeSide": "sell",
            "deliverQuantity": "0.002",
            "receiveQuantity": None,
        },
        "expected": {
            "symbol": "BTC-USD",
            "side": "sell",
            "deliverCurrency": "BTC",
            "receiveCurrency": "USD",
        },
    },
]
NEGATIVE_EXECUTE_CASES = [
    {
        "id": "invalid_format",
        "title": "Execute RFQ Quote - Invalid quote id format should fail",
        "quote_id": "not-a-real-quote-id",
        "expected_statuses": (400, 404, 422, 502),
    },
    {
        "id": "empty_quote_id",
        "title": "Execute RFQ Quote - Empty quote id should fail",
        "quote_id": "",
        "expected_statuses": (400, 404, 422, 502),
    },
    {
        "id": "whitespace_quote_id",
        "title": "Execute RFQ Quote - Whitespace quote id should fail",
        "quote_id": "   ",
        "expected_statuses": (400, 404, 422, 502),
    },
    {
        "id": "random_uuid_not_found",
        "title": "Execute RFQ Quote - Non-existent but valid quote id should fail",
        "quote_id": "11111111-1111-1111-1111-111111111111",
        "expected_statuses": (400, 404, 422, 502),
    },
    {
        "id": "short_quote_id",
        "title": "Execute RFQ Quote - Short quote id should fail",
        "quote_id": "123",
        "expected_statuses": (400, 404, 422, 502),
    },
    {
        "id": "special_characters_quote_id",
        "title": "Execute RFQ Quote - Special characters quote id should fail",
        "quote_id": "@@@###$$$",
        "expected_statuses": (400, 404, 422, 502),
    },
]