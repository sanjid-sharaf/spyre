from client import SpireClient
from sales import *
from customers import *

class Spire:
    def __init__(self, company, username, password):
        self.client = SpireClient(company, username, password)
        self.orders = OrdersClient(self.client)
        self.invoices = InvoiceClient(self.client)
        self.customers = CustomerClient(self.client)

    def get_client(self):
        return self.client

