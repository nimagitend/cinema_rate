import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cinema_rate.settings')

# --- اضافه شده: اجرای migrate خودکار ---
import django
from django.core.management import call_command

django.setup()
try:
    call_command('migrate', interactive=False)
except Exception as e:
    # اگر خطایی در migrate باشد، چاپ می‌شود ولی برنامه ادامه می‌دهد
    print("Migrate error:", e)

# ------------------------------------

application = get_wsgi_application()