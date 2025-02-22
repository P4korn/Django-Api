import logging

class AddRemoteIPFilter(logging.Filter):
    def filter(self, record):
        from django.utils.log import get_request
        request = get_request()
        record.remote_ip = request.META.get('REMOTE_ADDR', 'unknown') if request else 'unknown'
        return True