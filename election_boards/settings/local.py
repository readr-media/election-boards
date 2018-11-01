from .base import *

SECRET_KEY = 'bWFuYWdlLnB55Yiw5bqV5piv5bm55Zib55qECg=='
DEBUG = True
SPREADSHEET_ID = '19UjwwLiQ_jfpzsjG_VKlNn1b3dGoFCs3ZOR4s7yGb0I'

LOGGING = {
    'version': 1,
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers':['console'],
        },
    },
}
# # Configs for local with uwsgi
# DEBUG = False
# ALLOWED_HOSTS = ['*']
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'normal': {
#             'format': '[%(levelname)s] %(asctime)s | %(name)s:%(lineno)d | %(message)s'
#         },
#         'simple': {
#             'format': '[%(levelname)s] %(message)s'
#         },
#     },
#     # 'filters': {
#     #     'require_debug_true': {
#     #         '()': 'django.utils.log.RequireDebugTrue',
#     #     },
#     # },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',  # Default logs to stderr
#             'formatter': 'normal',  # use the above "normal" formatter
#             # 'filters': ['require_debug_true'],  # add filters
#         },
#     },
#     'loggers': {
#         '': {  # means "root logger"
#             'handlers': ['console'],  # use the above "console" handler
#             'level': 'INFO',  # logging level
#         },
#         'some_app.some_module': {  # Modify logger in some modules
#             'handlers': ['console'],
#             'level': 'DEBUG',
#             'propagate': True, 
#         },
#     },
# }

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql',
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'election_boards',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

CELERY_BROKER_URL = 'redis://:@127.0.0.1:6379'

STATIC_ROOT = 'static'
STATIC_URL = '/static/'


# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]
