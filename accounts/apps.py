from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    # Call signal to create superuser automatically
    def ready(self):
        import accounts.signals
