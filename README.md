PyLemonway
==========

Description
-----------

Lemonway wrapper for *DIRECTKITJSON2* implementation.


Usage
-----

Library should be used importing it as:

    from pylemonway.pylemonway import Lemonway

Next you can setup your client as:

     client = Lemonway(login, password, customer, sandbox=True)

**pyLemonway** API client accept many parameters, but on top of them:

- `credentials`: customer, login and password. Other parameters:
- `sandbox`: specify if you like to call production API (real money!) or play in a sandbox
- `version`: specify API version to be used
- `language`: specify language for responses
- `auto_wallet`: if you do not want to handle wallet external id numbering we can do that with random generated value (default `True`)

Methods explanation to be done.

Example
-------

    from pylemonway.pylemonway import Lemonway


    l = Lemonway("login", "password", "customer", sendbox=True)

    # registering wallet
    wallet_data = dict(clientMail='frank@music.com',
                       clientFirstName='Frank', clientLastName='Sinatra')

    wallet = l.wallet_register(wallet_data)

    charge_data = dict(wallet=1234, amountTot='2.00', amountCom='1.00',
                       wkToken=uuid.uuid4().__str__(),
                       returnUrl='http://yoursite.com', cancelUrl='http://yoursite.com',
                       errorUrl='http://yoursite.com')

    transaction_url = l.card_charge_page(charge_data)
