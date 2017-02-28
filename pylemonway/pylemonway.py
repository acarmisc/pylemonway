import requests
import uuid
import json

from .lexceptions import LemonwayException

class WebTransaction(object):

    def __init__(self, token, transaction_id, payment_url):
        self.token = token
        self.transaction_id = transaction_id
        self.payment_url = payment_url + self.token

class Wallet(object):

    def __init__(self, **params):
        self.__dict__.update(params)

    def __repr__(self):
        return '<LemowayWallet %s>' % self.ID

    def is_blocked(self):
        return self.BLOCKED or False

    def get_id(self):
        return self.ID

    def get_lwid(self):
        return self.LWID

    def serialize(self):
        import json
        return json.dumps(self.__dict__)

class Transaction(object):
    
    def __init__(self, **params):
        self.__dict__.update(params)

    def __repr__(self):
        return '<LemonwayTransaction %s>' % self.HPAY['ID']

    def get_id(self):
        return self.HPAY['ID']

    def serialize(self):
        import json
        return json.dumps(self.__dict__)


class TransactionHistory(object):

    def __init__(self, **params):
        self.__dict__.update(params)

    def __repr__(self):
        return '<LemonwayTransactionHistory %s>' % str(uuid.uuid4())

    def serialize(self):
        import json
        return json.dumps(self.__dict__)

class Card(object):

    def __init__(self, **params):
        self.__dict__.update(params)

    def __repr__(self):
        return '<LemonwayCard %s>' % self.ID

    def serialize(self):
        import json
        return json.dumps(self.__dict__)

    def get_id(self):
        return self.ID

class LemonwayResponse(object):

    def __init__(self, raw):
        self.raw = raw
        self.error = False

    def parse_response(self):
        parsed = self.raw
        response = parsed.get('d')

        if "WALLET" in response.keys():
            self.response_type = 'WALLET'
            self.payload = response.get('WALLET')

        if "MONEYINWEB" in response.keys():
            self.response_type = 'MONEYINWEB'
            self.payload = response.get('MONEYINWEB')

        if "CARD" in response.keys():
            self.response_type = 'CARD'
            self.payload = response.get('CARD')

        if "TRANS" in response.keys():
            self.response_type = 'TRANS'
            self.payload = response.get('TRANS')
 
        if "E" in response.keys() and response.get('E'):
            self.error = True
            self.error_message = response.get('E').get('Msg')
            self.error_code = response.get('E').get('Code')

        return self

    def is_error(self):
        return self.error


class Lemonway(object):

    def __init__(self, login, password, customer, customer_ip='127.0.0.1', customer_ua='Mozilla/5.0 (Windows NT 6.1; WOW64)', sandbox=False, language='en', base_url=None, version='1.1', auto_wallet=True):
        """
        First of all Lemonway needs credentials: customer, login and password. Other parameters:
        - sandbox: specify if you like to call production API (real money!) or play in a sandbox
        - version: specify API version to be used
        - language: specify language for responses
        - auto_wallet: if you do not want to handle wallet external id numbering
                       we can do that with random generated value
        """

        self.headers = {"Content-type": "application/json", "charset": "utf-8"}
        self.protocol = 'DIRECTKITJSON2'
        self.auto_wallet = auto_wallet
        self.customer = customer
        self.login = login
        self.password = password

        if sandbox:
            self.base_url = base_url or 'https://sandbox-api.lemonway.fr/mb/%s/dev/directkitjson2/service.asmx'
            self.webkit_card_url = 'https://sandbox-webkit.lemonway.fr/%s/dev/?moneyintoken=' % customer
        else:
            self.base_url = base_url or 'https://ws.lemonway.fr/mb/%s/prod/directkitjson2/service.asmx'
            self.webkit_card_url = 'https://webkit.lemonway.fr/mb/%s/prod/?moneyintoken=' % customer

        self.endpoint = base_url or self.base_url % self.customer
        self.common_data = dict(wlPass=self.password, wlLogin=self.login,
                                language=language, version=version,
                                walletIp=customer_ip, walletUa=customer_ua)

        print self.endpoint

    def _do(self, method, request_data, version=None):
        url = '%s/%s' % (self.endpoint, method)
        composed_data = self.common_data

        composed_data.update(request_data)

        if version:
            composed_data['version'] = version

        # fixing float to two decimal
        for k, v in composed_data.iteritems(): composed_data[k] = '{:.2f}'.format(v) if type(v) is float else v
        
        payload = json.dumps(dict(p=composed_data))

        response = requests.post(url, data=payload, headers=self.headers)

        if response.status_code != 200:
            raise Exception('Unknown exception %s' % response.status_code)

        resp = LemonwayResponse(response.json()).parse_response()

        if resp.is_error():
            raise LemonwayException(resp.error_message, resp.error_code)

        return resp.payload

    def wallet_register(self, data):
        if 'wallet' not in data.keys() and self.auto_wallet == True:
            data['wallet'] = str(uuid.uuid4())

        resp = self._do('RegisterWallet', data)
        wallet = Wallet(**resp)

        return wallet

    def wallet_details(self, data):
        resp = self._do('GetWalletDetails', data)
        wallet = Wallet(**resp)

        return wallet

    def card_charge_page(self, data):
        resp = self._do('MoneyInWebInit', data, version='1.2')
        transaction = WebTransaction(token=resp.get('TOKEN'),
                                     transaction_id=resp.get('ID'),
                                     payment_url=self.webkit_card_url)

        return transaction

    def card_register(self, data):
        resp = self._do('RegisterCard', data, version='1.2')
        card = Card(**resp)

        return card

    def card_unregister(self, data):
        resp = self._do('UnregisterCard', data, version='1.2')
	card = Card(**resp)

        return card

    def money_in_with_card_id(self,data):
        resp = self._do('MoneyInWithCardId', data, version='1.2')
        transaction = Transaction(**resp)

        return transaction
    
    def refund_money_in(self,data):
        resp = self._do('RefundMoneyIn', data, version='1.2')
        transaction = Transaction(**resp)

        return transaction

    def get_wallet_trans_history(self,data):
        resp = self._do('GetWalletTransHistory', data, version='1.2')
        wallet_transaction_history = TransactionHistory(**resp)

        return wallet_transaction_history
