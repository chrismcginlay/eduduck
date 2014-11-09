#core/middleware.py

from django.utils import timezone
import logging
logger = logging.getLogger(__name__)

class TimezoneMiddleware(object):

    def process_request(self, request):
        try:
            tz = request.user.profile.user_tz
            timezone.activate(tz)
        except:
            logger.warning("Reverting to default timezone UTC")
            timezone.activate(timezone.utc)
        return None
            
