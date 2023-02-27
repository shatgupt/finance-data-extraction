import requests
from datetime import datetime
from datetime import date


class ExchangeRate:
    __exchange_rates = {}
    __fallback_rates = {}

    @classmethod
    def load_US_treasury_INR_rates(cls):
        # https://www.fincen.gov/reporting-maximum-account-value
        # https://fiscaldata.treasury.gov/datasets/treasury-reporting-rates-exchange/treasury-reporting-rates-of-exchange
        exchange_rate_url = 'https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/od/rates_of_exchange?fields=record_date,country_currency_desc,exchange_rate&filter=country_currency_desc:in:(India-Rupee),record_date:gte:2017-01-01'
        data = requests.get(exchange_rate_url).json()
        for d in data['data']:
            ExchangeRate.__exchange_rates[date.fromisoformat(d['record_date'])] = float(d['exchange_rate'])

        return ExchangeRate.__exchange_rates

    @classmethod
    def __previous_quarter_end(cls, cur_date):
        # Return the same date if it is end of quarter
        q1 = date(cur_date.year, 3, 31)
        q2 = date(cur_date.year, 6, 30)
        q3 = date(cur_date.year, 9, 30)
        q4 = date(cur_date.year, 12, 31)
        # end_of_quarter = [q1, q2, q3, q4]
        # if cur_date in end_of_quarter:
        #     return cur_date

        if cur_date.month < 4:
            return date(cur_date.year - 1, 12, 31)
        elif cur_date.month < 7:
            return q1
        elif cur_date.month < 10:
            return q2
        return q3

    @classmethod
    def __year_end(cls, cur_date):
        return date(cur_date.year, 12, 31)

    # Returns year-end date for previous years and last quarter-end date for current year
    @classmethod
    def __get_date_for_exchange_rate(cls, cur_date):
        today = date.today()
        if (today.year == cur_date.year):
            return ExchangeRate.__previous_quarter_end(cur_date)
        else:
            return ExchangeRate.__year_end(cur_date)

    @classmethod
    def get_inr_rate_from_fallback(cls, cur_date):
        if cur_date not in ExchangeRate.__fallback_rates:
            # url = 'https://api.exchangerate-api.com/v4/latest/USD'
            url = f"https://api.exchangerate.host/{cur_date.isoformat()}?base=USD&symbols=INR"
            data = requests.get(url).json()
            ExchangeRate.__fallback_rates[cur_date] = data['rates']['INR']
        return ExchangeRate.__fallback_rates[cur_date]

    @classmethod
    def get_inr_rate(cls, cur_date):
        exchange_date = ExchangeRate.__get_date_for_exchange_rate(cur_date)
        if exchange_date in ExchangeRate.__exchange_rates:
            return ExchangeRate.__exchange_rates[exchange_date]
        else:
            return ExchangeRate.get_inr_rate_from_fallback(exchange_date)

    @classmethod
    def get_rates(cls):
        return ExchangeRate.__exchange_rates


# Code to print all values
if __name__ == "__main__":
    ExchangeRate.load_US_treasury_INR_rates()
    for y in ['2018-12-31', '2019-12-31', '2020-12-31', '2021-12-31', '2022-12-31', '2023-01-31']:
        rate = ExchangeRate.get_inr_rate(date.fromisoformat(y))
        print(f"{y},{rate}")