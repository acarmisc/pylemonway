from pylemonway import Lemonway
from pylemonway import LemonwayException
import json
import pdb

l = Lemonway("society", "123456", "demo", sandbox=True)

# registering wallet
print "-"*4 + "registering_wallet" + "-"*4

wallet_data = dict(clientMail='g______________@due.it',
                   clientFirstName='uno', clientLastName='due')
try:
    wallet = l.wallet_register(wallet_data)
    print wallet.serialize()


    # registering card
    print "-"*4 + "registering_card" + "-"*4
    card_data = dict(wallet=wallet.get_id(),
                     cardType='1',
                     cardNumber='5017670000006700',
                     cardCode='123',
                     cardDate='01/2018')

    card = l.card_register(card_data)
    print card.serialize()

    # money in with card id
    print "-"*4 + "money_in_with_card_id" + "-"*4
    money_in_with_card_id_data = dict(wallet=wallet.get_id(),
                      cardId=card.get_id(),
                      amountTot=10.00,
                      amountCom=10.00,
                      comment='pagamento di prova',
                      autoCommission=0)

    transaction = l.money_in_with_card_id(money_in_with_card_id_data)
    print transaction.serialize()

    # refund money
    print "-"*4 + "refund_money_in" + "-"*4
    refund_money_in_data = dict(transactionId= transaction.get_id(),
                    comment='prova rimborso transazione')
    refund_money_in = l.refund_money_in(refund_money_in_data)
    print refund_money_in.serialize()

    # get wallet transaction history
    print "-"*4 + "get_wallet_transaction_history" + "-"*4
    get_wallet_trans_history_data = dict(wallet=wallet.get_id())
    wallet_trans_history = l.get_wallet_trans_history(get_wallet_trans_history_data)
    print wallet_trans_history.serialize()

    # unregistering card
    print "-"*4 + "unregister_card" + "-"*4
    unregister_card_data = dict(wallet=wallet.get_id(),
                    cardId=card.get_id())
    unregister_card = l.card_unregister(unregister_card_data)
    print unregister_card.serialize()

except LemonwayException as e:
  print e.code
  print e.value
