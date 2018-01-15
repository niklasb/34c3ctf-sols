class SecHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['X-Content-Type-Options'] = "no-sniff"
        response['X-Frame-Options'] = "DENY"
        response['Referrer-Policy'] = "no-referrer"
        response['X-XSS-Protection'] = "1; mode=block"
        response['Content-Security-Policy'] = (
            "default-src 'none'; "
            "base-uri 'none'; "
            "frame-ancestors 'none'; "
            "connect-src 'self'; "
            "img-src 'self'; "
            "style-src 'self' https://fonts.googleapis.com/; "
            "font-src 'self' https://fonts.gstatic.com/s/materialicons/; "
            "form-action 'self'; "
            "script-src 'self'; "
            )
        return response
