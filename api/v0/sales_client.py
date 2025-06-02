from baseClient import BaseClient
from Models.sales import *
import utils

class OrdersClient(BaseClient):

    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "sales/orders"
    
    def get_order(self, id: int):
        """Get an sales order by id"""
        
        return self._get(f"/{self.endpoint}/{str(id)}")
    
    def create_order(self, product_data):
        """Create an sales order"""
        
        return self._post(f"/{self.endpoint}", json=product_data)
    
    def update_order(self, id: int, product_data):
        """Update an sales order by id"""
        
        return self._put(f"/{self.endpoint}/{str(id)}", json=product_data)
    
    def delete_order(self, id: int):
        """Delete an sales order by id"""
        
        return self._delete(f"/{self.endpoint}/{str(id)}")
    
    def process_order(self, id: int):
        """Set the status of an order with @id to Process"""

        return self._put(f"/{self.endpoint}/{str(id)}", json={"status" : "P"}) 
    
    def invoice_order(self, id: int):
        """Invoice A sales order by id"""

        return self._post(f"/{self.endpoint}/{str(id)}/invoice")
    

    
class InvoiceClient(BaseClient):
    
    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "sales/invoices"

    def get_invoice(self, id: int):
        """Get an sales invoice by id"""
        
        return self._get(f"/{self.endpoint}/{str(id)}")   
    
    def reverse_invoice(self, id:int):
        """Creates a sales order from an Invoice with id @id"""

        invoice = self.get_invoice(206355)
        invoice_model = Invoice(**invoice)
        order_converted = utils.create_sales_order_from_invoice(invoice_model)
        return OrdersClient(client=self.client).create_order(order_converted.model_dump(exclude_unset=True, exclude_none=True))\
        

class Customer(BaseClient):

    def __init__(self, client):
        super().__init__(client)
        self.endpoint = "customers"

    def get_customer(self, id: int):
        """Get a customer by id"""

        return self._get(f"{self}")
    
