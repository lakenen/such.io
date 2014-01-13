import logging
from django.db import transaction
from django.db.models import F

from core.models import Balance
from ..models import Wallet, DepositAddress, Transaction
from ..conn import WalletConnection


logger = logging.getLogger(__name__)


def _update_deposit(wallet, conn, tx):
    logger.info('%s: updating receive tx %s.', conn, tx.txid)

    try:
        address = DepositAddress.objects.select_related('balance').get(address=tx.address)
    except DepositAddress.DoesNotExist:
        logger.info('address %s not found, skipping transaction.', tx.address)
        return

    try:
        deposit = Transaction.objects.get(tx_id=tx.txid)
    except Transaction.DoesNotExist:
        if tx.confirmations == 0:
            logger.info('previously unknown tx has zero confirmations, skipping transaction %s' % tx.txid)
            return

        deposit = Transaction.objects.create(
                type=Transaction.TYPE.DEPOSIT,
                wallet=wallet,
                balance=address.balance,
                tx_id=tx.txid,
                amount=tx.amount
        )

    if deposit.is_orphaned:
        logger.info('%s is already orphaned, nothing to do.', deposit)
        return

    if deposit.is_cleared:
        logger.info('%s is already cleared, nothing to do.', deposit)
        return True

    if tx.confirmations == 0:
        deposit.is_orphaned = True
        deposit.save(update_fields=['is_orphaned'])
        logger.info('transaction %s has zero confirmations, orphaning deposit %s' % (tx.txid, deposit))
        return
    elif not deposit.wallet.currency.is_enough_confirmations(tx.confirmations):
        logging.info('%s only has %s confirmations, which is not enough to clear it.', tx.txid, tx.confirmations)
        return

    logging.info('clearing tx %s since it has %s confirmations.', tx.txid, tx.confirmations)
    try:
        with transaction.atomic():
            logging.info('adding %s to the user\'s balance', tx.amount)

            balance_query = Balance.objects.filter(id=address.balance.id)
            num_updated = balance_query.update(amount=F('amount') + tx.amount)
            if num_updated != 1:
                raise Exception('updated %d rows when clearing %s on %s, aborting.' % (num_updated, deposit, address.balance))

            deposit.is_cleared = True
            deposit.save(update_fields=['is_cleared'])

            return True
    except:
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


def update_transactions(wallet):
    if isinstance(wallet, int):
        wallet = Wallet.objects.get(id=wallet)
    conn = WalletConnection(wallet)

    newest_cleared_tx_id = None
    for tx in conn.get_transactions_since(wallet.last_cleared_tx_id):
        if tx.category == 'receive':
            cleared_tx = _update_deposit(wallet, conn, tx)
            if newest_cleared_tx_id is None and cleared_tx:
                newest_cleared_tx_id = tx.txid

    if newest_cleared_tx_id:
        wallet.last_cleared_tx_id = newest_cleared_tx_id
        wallet.save(update_fields=['last_cleared_tx_id'])
