from django.apps import AppConfig


class CarsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cars'

    def ready(self) -> None:
        from currencies import start_background_updates as start_background_currencies_updates
        from car_prices_updater import start_background_updates as start_background_car_prices_updates

        start_background_currencies_updates()
        start_background_car_prices_updates()
