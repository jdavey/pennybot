import requests

URL = "https://poloniex.com/public?command={}"
PRICE_CMD = "returnTicker"
PRICE_URL = URL.format(PRICE_CMD)

FIAT_MAP = {
    "USD": "USDT"
}


class PoloniexApi:
    def __init__(self):
        pass

    @staticmethod
    def get_tickers(fiat="USD"):
        response = requests.get(PRICE_URL)
        fiat_name = FIAT_MAP[fiat]
        keys = filter(lambda key: fiat_name in key, response.json().keys())
        return sorted(map(lambda key: str(key.replace(fiat_name + "_", "")), keys))

    @staticmethod
    def get_prices(ccys, fiat="USD"):
        if fiat not in FIAT_MAP:
            raise Exception("Invalid CCY - {}".format(fiat))

        response = requests.get(PRICE_URL)
        if response.status_code is not 200:
            raise Exception("Bad response from server - {}".format(response.status_code))

        fiat_name = FIAT_MAP[fiat]
        ccy_pairs = map(lambda ccy:
                        {"key": "{}_{}".format(fiat_name, ccy),
                         "ccy": ccy,
                         "fiat": fiat}
                        , ccys)

        response_dict = response.json()
        return_values = []
        for ccy_pair in ccy_pairs:
            record = response_dict[ccy_pair["key"]]

            return_values.append({
                "fiat": ccy_pair["fiat"],
                "ccy": ccy_pair["ccy"],
                "price": round(float(record["last"]), 3),
                "pct_chg": round(float(record["percentChange"]) * 100, 3)
            })

        return return_values
