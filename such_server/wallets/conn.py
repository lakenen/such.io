from bitcoinrpc import connect_to_remote


class WalletConnection(object):
    def __init__(self, wallet):
        self._host = wallet.rpc_host
        self._port = wallet.rpc_port
        self._conn =  connect_to_remote(
                wallet.rpc_username,
                wallet.rpc_password,
                host=self._host,
                port=self._port
        )

    def __repr__(self):
        return '<%s: %s:%s>' % (self.__class__.__name__, self._host, self._port)

    #def __getattr__(self, name):
    #    return getattr(self._conn, name)

    def _get_account_name(self, user):
        return 'user-%d' % user.id

    def get_new_address(self, user):
        return self._conn.getnewaddress(self._get_account_name(user))

    def get_receives(self):
        count = 100
        start = 0
        def get_transactions(count, start):
            return self._conn.listtransactions('*', count, start)

        txs = get_transactions(count, start)
        while len(txs) > 0:
            txs.sort(key=lambda tx: tx.time, reverse=True)
            for tx in txs:
                if tx.category == 'receive':
                    yield tx
            start += count
            txs = get_transactions(count, start)

    def transfer(self, from_account, to_account, amount, comment):
        self._conn.move(from_account, to_account, float(amount), comment=comment)
