import logging
from django.db import transaction
from django.db.models import F
from django.utils.timezone import now

from core.models import Balance
from .models import Market, Order


logger = logging.getLogger(__name__)


def do_transaction(buy, sell):
    assert buy.market_id == sell.market_id
    assert buy.type == Order.TYPE.BUY
    assert sell.type == Order.TYPE.SELL
    assert sell.rate <= buy.rate
    logger.info('clearing %s and %s' % (buy, sell))

    try:
        with transaction.atomic():

            new_buy, new_sell = None, None
            # make a partial buy order
            if buy.amount > sell.amount:
                new_buy = buy.clone()
                new_buy.amount = buy.amount - sell.amount
                new_buy.save()
                logger.info('generating partial buy: %s' % new_buy)

                buy.is_partial = True

                buy.filled_amount = sell.amount
                sell.filled_amount = sell.amount

            # make a partial sell order
            elif buy.amount < sell.amount:
                new_sell = sell.clone()
                new_sell.amount = sell.amount - buy.amount
                new_sell.save()
                logger.info('generating partial sell: %s' % new_sell)

                sell.is_partial = True

                buy.filled_amount = buy.amount
                sell.filled_amount = buy.amount

            # exact match. wow
            else:
                buy.filled_amount = buy.amount
                sell.filled_amount = buy.amount

            buy.status = Order.STATUS.FILLED
            sell.status = Order.STATUS.FILLED

            buy.filled_at = sell.filled_at = now()

            buy.filled_rate = sell.filled_rate = sell.rate

            buy.save()
            sell.save()

            # update seller's and buyer's balances
            for order in [sell, buy]:
                buy_currency, _ = order.get_buy_and_sell_currencies()
                buy_amount, _ = order.get_buy_and_sell_filled_amounts()
                balance = Balance.objects.get(user=order.user, currency=buy_currency)

                balance_query = Balance.objects.filter(id=balance.id)
                num_updated = balance_query.update(amount=F('amount') + buy_amount)

                if num_updated != 1:
                    raise Exception('updated %d rows when updating balance %s for %s' % (num_updated, balance, order))

            return new_buy, new_sell
    except Exception:
        #TODO error handling
        raise


def _fill_orders(market):
    try:
        best_sell = market.open_sells().order_by('rate')[0]
        best_buy = market.open_buys().order_by('-rate')[0]
    except IndexError:
        # there are either no open buys or no open sells, so nothing to do
        return

    clearable_sells = list(market.open_sells().filter(rate__lte=best_buy.rate).order_by('ordered_at', 'rate'))
    clearable_buys = list(market.open_buys().filter(rate__gte=best_sell.rate).order_by('ordered_at', '-rate'))

    #TODO optimize the shit out of this
    while len(clearable_buys) > 0:
        buy = clearable_buys[0]
        logger.info('BUY = %s' % buy)
        buy_cleared = False

        index = 0
        while index < len(clearable_sells):
            sell = clearable_sells[index]
            logger.info('SELL = %s' % sell)
            index += 1

            if buy.cancel_requested_at and buy.cancel_requested_at < sell.ordered_at:
                logger.info('skipping a buy due to cancel request')
                # break instead of continue since sells are sorted by ordered_at ascending
                break

            if sell.cancel_requested_at and sell.cancel_requested_at < buy.ordered_at:
                logger.info('skipping a sell due to cancel request')
                continue

            if sell.rate <= buy.rate:
                buy_cleared = True
                new_buy, new_sell = do_transaction(buy, sell)
                index -= 1
                if new_buy:
                    clearable_buys[0] = new_buy
                    clearable_sells.pop(index)
                elif new_sell:
                    clearable_buys.pop(0)
                    clearable_sells[index] = new_sell
                else:
                    clearable_buys.pop(0)
                    clearable_sells.pop(index)
                break

        if not buy_cleared:
            clearable_buys.pop(0)

def clear_market(market):
    if not isinstance(market, Market):
        market = Market.objects.get(id=market)

    # clear open buys and sells
    _fill_orders(market)

    # fulfill order cancellation requests
    update_query = market.open_orders().filter(cancel_requested_at__isnull=False)
    num_canceled = update_query.update(status=Order.STATUS.CANCELED, canceled_at=now())
    logger.info('canceled %d orders' % num_canceled)
