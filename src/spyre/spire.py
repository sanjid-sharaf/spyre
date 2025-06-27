from .client import SpireClient
from .sales import OrdersClient, InvoiceClient
from .customers import CustomerClient
from .inventory import InventoryClient

class Spire:
    def __init__(self, host : str, company : str, username : str, password : str):
        self.client = SpireClient(host, company, username, password)
        self.orders = OrdersClient(self.client)
        self.invoices = InvoiceClient(self.client)
        self.customers = CustomerClient(self.client)
        self.inventory = InventoryClient(self.client)


