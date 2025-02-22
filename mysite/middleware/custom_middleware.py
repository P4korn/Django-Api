import logging

class LogIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger("django")  # Use Django's logger

    def __call__(self, request):
        ip = self.get_client_ip(request)
        response = self.get_response(request)

        # Log everything in one line
        self.logger.info(f'Client IP: {ip} | {request.method} {request.path} | Status: {response.status_code}')
        
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")