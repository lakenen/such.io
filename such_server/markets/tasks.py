from django.db import transaction
from django.utils.timezone import now

from .models import Market, Order


def _open_orders(market, **kwargs):
    return Order.objects.filter(market_id=market.id, status=Order.STATUS.OPEN, **kwargs)


def do_transaction(buy, sell):
    assert buy.market_id == sell.market_id
    assert buy.type == Order.TYPE.BUY
    assert sell.type == Order.TYPE.SELL
    assert sell.rate <= buy.rate


    try:
        with transaction.atomic():

            new_buy, new_sell = None, None
            if buy.amount > sell.amount:
                new_buy = buy.clone()
                new_buy.amount = buy.amount - sell.amount
                new_buy.save()

                buy.is_partial = True
                buy.filled_amount = \
                sell.filled_amount = sell.amount

            elif buy.amount < sell.amount:
                new_sell = sell.clone()
                new_sell.amount = sell.amount - buy.amount
                new_sell.save()

                sell.is_partial = True
                buy.filled_amount = \
                sell.filled_amount = buy.amount

            else:
                buy.filled_amount = \
                sell.filled_amount = buy.amount

            buy.status = Order.STATUS.FILLED
            sell.status = Order.STATUS.FILLED

            buy.filled_at = \
            sell.filled_at = now()

            buy.filled_rate = \
            sell.filled_rate = sell.rate

            buy.save()
            sell.save()

            return new_buy, new_sell
    except Exception:
        #TODO error handling
        raise


def _fill_orders(market):
    try:
        best_sell = _open_orders(market, type=Order.TYPE.SELL).order_by('rate')[0]
        best_buy = _open_orders(market, type=Order.TYPE.BUY).order_by('-rate')[0]
    except IndexError:
        # there are either no open buys or no open sells, so nothing to do
        return

    clearable_sells = list(_open_orders(market, type=Order.TYPE.SELL, rate__lte=best_buy.rate).order_by('ordered_at', 'rate'))
    clearable_buys = list(_open_orders(market, type=Order.TYPE.BUY, rate__gte=best_sell.rate).order_by('ordered_at', '-rate'))

    #TODO optimize the shit out of this
    while len(clearable_buys) > 0:
        buy = clearable_buys[0]

        buy_cleared = False
        for index, sell in enumerate(clearable_sells):

            if buy.cancel_requested_at and buy.cancel_requested_at < sell.ordered_at:
                continue

            if sell.cancel_requested_at and sell.cancel_requested_at < buy.ordered_at:
                continue

            if sell.rate <= buy.rate:
                buy_cleared = True
                new_buy, new_sell = do_transaction(buy, sell)
                if new_buy:
                    clearable_buys[0] = new_buy
                    clearable_sells.pop(index)
                elif new_sell:
                    clearable_buys.pop(0)
                    clearable_sells[index] = new_sell
                else:
                    clearable_buys.pop(0)
                    clearable_sells.pop(index)

        if not buy_cleared:
            clearable_buys.pop(0)

def clear_market(market):
    if not isinstance(market, Market):
        market = Market.objects.get(id=market)

    _fill_orders(market)

    # fulfill order cancellation requests
    _open_orders(market, cancel_requested_at__isnull=False).update(status=Order.STATUS.CANCELLED, cancelled_at=now())
