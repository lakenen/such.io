import logging
from django.db import transaction
from django.db.models import F
from django.conf import settings

from core.models import Balance, Transaction
from ..models import Wallet, DepositAddress
from ..conn import WalletConnection


logger = logging.getLogger(__name__)


def _update_receive(conn, tx):
    logger.info('%s: updating receive tx %s.', conn, tx.txid)

    try:
        address = DepositAddress.objects.get(address=tx.address)
    except DepositAddress.DoesNotExist:
        logger.info('address %s not found, skipping transaction.', tx.address)
        return

    try:
        deposit = Transaction.objects.get(tx_id=tx.txid)
    except Transaction.DoesNotExist:
        deposit = Transaction.objects.create(
                type=Transaction.TYPE.DEPOSIT,
                address=address,
                tx_id=tx.txid,
                amount=tx.amount
        )

    if deposit.is_cleared:
        logging.info('%s is already cleared, nothing to do.', deposit)
        return False

    if not Transaction.is_enough_confirmations(tx.confirmations):
        logging.info('%s only has %s confirmations, which is not enough to clear it.', tx.txid, tx.confirmations)
        return False

    logging.info('clearing tx %s since it has %s confirmations.', tx.txid, tx.confirmations)
    try:
        with transaction.atomic():
            logging.info('adding %s to the cleared_amount of %s', tx.amount, address.balance)

            balance_query = Balance.objects.filter(id=address.balance.id)
            num_updated = balance_query.update(cleared_amount=F('cleared_amount') + tx.amount)
            if num_updated != 1:
                raise Exception('updated %d rows when clearing %s on %s, aborting.' % (num_updated, deposit, address.balance))

            deposit.is_cleared = True
            deposit.save(update_fields=['is_cleared'])

            #TODO does the transaction roll back if conn.transfer fails?
            conn.transfer(tx.account, settings.CLEARED_FUNDS_ACCOUNT, tx.amount, comment='clear %s' % tx.txid)
    except:
        #transaction is rolled back at this point
        logger.exception('error while clearning tx %s' % tx.txid)
        return False


def create_balance(user_id, currency_id):
    balance, created = Balance.objects.select_related('user', 'currency').get_or_create(
            user_id=user_id,
            currency_id=currency_id
    )

    if balance.depositaddress_set.count() == 0:
        wallet = Wallet.choose_wallet_for_user(balance.user, balance.currency)
        provision_deposit_address(balance, wallet)


def provision_deposit_address(balance, wallet):
    conn = WalletConnection(wallet)

    new_address = conn.get_new_address(balance.user)
    DepositAddress.objects.create(
            wallet=wallet,
            balance=balance,
            address=new_address
    )


def update_deposits(wallet):
    if isinstance(wallet, int):
        wallet = Wallet.objects.get(id=wallet)
    conn = WalletConnection(wallet)

    #TODO improve this so we don't iterate through the entire transaction history everytime
    receives = conn.get_receives()
    for tx in receives:
        _update_receive(conn, tx)
