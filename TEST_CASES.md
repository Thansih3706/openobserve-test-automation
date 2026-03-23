# Test Cases – Aquanow RFQ API

## Overview

This document contains the full list of executed test cases covering authentication, RFQ lifecycle, and validation scenarios.

---

## Test Case Inventory

| ID | Module  | Test Case                  | Scenario         | Objective                        | Status   |
| -- | ------- | -------------------------- | ---------------- | -------------------------------- | -------- |
| 1  | Auth    | create_quote_without_auth  | -                | Cannot create quote without auth | Passed   |
| 2  | Auth    | get_quote_without_auth     | -                | Cannot get quote without auth    | Passed   |
| 3  | Auth    | execute_quote_without_auth | buy_receive_btc  | Cannot execute without auth      | Passed   |
| 4  | Auth    | execute_quote_without_auth | sell_deliver_btc | Cannot execute without auth      | Passed   |
| 5  | Auth    | expire_quote_without_auth  | buy_receive_btc  | Cannot expire without auth       | Passed   |
| 6  | Auth    | expire_quote_without_auth  | sell_deliver_btc | Cannot expire without auth       | Passed   |
| 7  | Create  | missing_api_key            | -                | Fail when API key missing        | Passed   |
| 8  | Create  | missing_signature          | -                | Fail when signature missing      | Passed   |
| 9  | Create  | missing_nonce              | -                | Fail when nonce missing          | Passed   |
| 10 | Create  | invalid_api_key            | -                | Fail invalid API key             | Passed   |
| 11 | Create  | invalid_signature          | -                | Fail invalid signature           | Passed   |
| 12 | Create  | stale_nonce                | -                | Fail stale nonce                 | Passed   |
| 13 | Create  | replayed_nonce             | -                | Fail replayed nonce              | Passed   |
| 14 | Execute | execute_success            | buy_receive_btc  | Execute quote successfully       | Passed   |
| 15 | Execute | execute_success            | sell_deliver_btc | Execute quote successfully       | Passed   |
| 16 | Execute | invalid_quote_id           | invalid_format   | Fail invalid ID                  | Passed   |
| 17 | Execute | invalid_quote_id           | empty            | Fail empty ID                    | Passed   |
| 18 | Execute | invalid_quote_id           | whitespace       | Fail whitespace ID               | Passed   |
| 19 | Execute | invalid_quote_id           | random_uuid      | Fail unknown ID                  | Passed   |
| 20 | Execute | invalid_quote_id           | short_id         | Fail short ID                    | Passed   |
| 21 | Execute | invalid_quote_id           | special_chars    | Fail special chars               | Passed   |
| 22 | Execute | expired_quote              | buy_receive_btc  | Cannot execute expired quote     | Passed   |
| 23 | Execute | expired_quote              | sell_deliver_btc | Cannot execute expired quote     | Passed   |
| 24 | Execute | manually_expired           | buy_receive_btc  | Cannot execute expired           | Passed   |
| 25 | Execute | manually_expired           | sell_deliver_btc | Cannot execute expired           | Passed   |
| 26 | Auth    | execute_without_auth       | buy_receive_btc  | Cannot execute without auth      | Passed   |
| 27 | Auth    | execute_without_auth       | sell_deliver_btc | Cannot execute without auth      | Passed   |
| 28 | Execute | duplicate_execution        | buy_receive_btc  | Cannot execute twice             | Passed   |
| 29 | Execute | duplicate_execution        | sell_deliver_btc | Cannot execute twice             | Passed   |
| 30 | Expire  | expire_success             | -                | Expire quote successfully        | Passed   |
| 31 | Expire  | duplicate_expire           | -                | Cannot expire twice              | Passed   |
| 32 | Get     | get_quote                  | buy_deliver      | Valid get quote                  | Passed   |
| 33 | Get     | get_quote                  | buy_receive      | Valid get quote                  | Passed   |
| 34 | Get     | get_quote                  | sell_deliver     | Valid get quote                  | Passed   |
| 35 | Get     | get_quote                  | sell_receive     | Valid get quote                  | Passed   |
| 36 | Create  | create_quote               | buy_deliver      | Valid create                     | Passed   |
| 37 | Create  | create_quote               | buy_receive      | Valid create                     | Passed   |
| 38 | Create  | create_quote               | sell_deliver     | Valid create                     | Passed   |
| 39 | Create  | create_quote               | sell_receive     | Valid create                     | Passed   |
| 40 | Create  | quantity_precedence        | buy              | Deliver should win               | ❌ Failed |
| 41 | Create  | quantity_precedence        | sell             | Receive should win               | ❌ Failed |
| 42 | Get     | missing_ticker             | -                | Reject missing ticker            | Passed   |
| 43 | Get     | missing_account_id         | -                | Reject missing account id        | ❌ Failed |
| 44 | Get     | missing_trade_side         | -                | Reject missing trade side        | Passed   |
| 45 | Get     | missing_quantities         | -                | Reject missing quantities        | Passed   |
| 46 | Get     | invalid_trade_side         | -                | Reject invalid side              | Passed   |
| 47 | Get     | invalid_ticker             | -                | Reject invalid ticker            | Passed   |
| 48 | Get     | unsupported_ticker         | -                | Reject unsupported ticker        | Passed   |
| 49 | Get     | zero_quantity              | -                | Reject zero quantity             | Passed   |
| 50 | Get     | negative_quantity          | -                | Reject negative quantity         | Passed   |
| 51 | Get     | non_numeric_quantity       | -                | Reject non-numeric               | Passed   |
| 52 | Create  | missing_ticker             | -                | Reject missing ticker            | Passed   |
| 53 | Create  | missing_account_id         | -                | Reject missing account id        | Passed   |
| 54 | Create  | missing_trade_side         | -                | Reject missing trade side        | Passed   |
| 55 | Create  | missing_quantities         | -                | Reject missing quantities        | Passed   |
| 56 | Create  | invalid_trade_side         | -                | Reject invalid side              | Passed   |
| 57 | Create  | invalid_ticker             | -                | Reject invalid ticker            | Passed   |
| 58 | Create  | unsupported_ticker         | -                | Reject unsupported ticker        | Passed   |
| 59 | Create  | zero_quantity              | -                | Reject zero quantity             | Passed   |
| 60 | Create  | negative_quantity          | -                | Reject negative quantity         | Passed   |
| 61 | Create  | non_numeric_quantity       | -                | Reject non-numeric               | Passed   |
| 62 | Create  | same_currency_USD          | -                | Reject USD-USD                   | Passed   |
| 63 | Create  | same_currency_BTC          | -                | Reject BTC-BTC                   | Passed   |

---

## Notes

* Failed cases highlight **validation and business logic gaps**
* Test suite covers **authentication, validation, lifecycle, and edge cases**
