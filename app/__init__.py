from aiohttp.web import Application

from .routes import (
    check_crypto_payment,
    marzban_request,
    check_crypto_charge_payment,
)


def setup_routes(app: Application):
    app.router.add_post("/marz", marzban_request)
    app.router.add_post("/coinos_payment/ct/{pk}", check_crypto_payment)
    app.router.add_post("/coinos_payment/wt/{pk}", check_crypto_charge_payment)


__all__ = (
    "setup_routes",
)
