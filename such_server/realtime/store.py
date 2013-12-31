from django.conf import settings
from ws4redis.store import RedisStore


class SuchRedisStore(RedisStore):
    def subscribe_channels(self, request, channels):
        self._user = request.user
        self._session = request.session

        def subscribe_for(prefix):
            key = request.path_info.replace(settings.WEBSOCKET_URL, prefix, 1)
            self._subscription.subscribe(key)

        self._subscription = self._connection.pubsub()

        # subscribe to these Redis channels for outgoing messages
        if 'subscribe-session' in channels and request.session:
            subscribe_for('{0}:'.format(request.session.session_key))
        if 'subscribe-user' in channels and request.user:
            subscribe_for('{0}:'.format(request.user))
        if 'subscribe-broadcast' in channels:
            subscribe_for('_broadcast_:')

    def publish_message(self, message):
        if not self._user or not self._user.is_authenticated():
            return

        if False:
            for n in range(int(message)):
                self._connection.publish('_broadcast_:foobar', str(n))
        else:
            self._connection.publish('_broadcast_:foobar', message)
            self._connection.publish('%s:foobar' % self._user.email, 'you made something. nice')

    def send_persited_messages(self, websocket):
        pass
