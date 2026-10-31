import aiohttp
from config import TEZCHECK_BASE_URL, TEZCHECK_SECRET

class TezCheck:
    """tezcheck.uz API klienti. Endpoint'larni ularning hujjatiga moslang."""
    def __init__(self):
        self.base = TEZCHECK_BASE_URL.rstrip("/")
        self.headers = {"Authorization": f"Bearer {TEZCHECK_SECRET}"}

    async def verify_keys(self, account_api: str, kassa_api: str) -> bool:
        # TODO: haqiqiy tekshiruv endpointi bilan almashtiring
        async with aiohttp.ClientSession() as s:
            try:
                async with s.post(
                    f"{self.base}/v1/merchant/verify",
                    json={"account_api": account_api, "kassa_api": kassa_api},
                    headers=self.headers, timeout=10,
                ) as r:
                    return r.status == 200
            except Exception:
                return False

    async def create_invoice(self, amount: int, order_id: str) -> dict | None:
        async with aiohttp.ClientSession() as s:
            try:
                async with s.post(
                    f"{self.base}/v1/invoice",
                    json={"amount": amount, "order_id": order_id},
                    headers=self.headers, timeout=10,
                ) as r:
                    return await r.json() if r.status == 200 else None
            except Exception:
                return None