from .client import APIResource, SpireClient
from requests.exceptions import HTTPError, RequestException
from .Exceptions import CreateRequestError
from typing import Any, Optional, List, Dict
from urllib.parse import urlparse
from .utils import *
import json

from .Models.purchasing_models import PurchaseOrder

class PurchasingClient:

    def __init__(self, client: SpireClient):
        self.client = client
        self.endpoint = "purchasing/orders"

    def get_purchase_order(self, id: int = None, PO_number: str = None) -> 'purchaseOrder':
        """
        Retrieve a purchase order by its ID or PO number.

        Args:
            id (int, optional): The ID of the purchase order to retrieve.
            PO_number (str, optional): The purchase order number of the purchase order to retrieve.

        Returns:
            purchaseOrder: A `purchaseOrder` wrapper instance containing the retrieved data.

        Raises:
            ValueError: If neither id nor PO_number is provided, or if no matching order is found.
        """
        if id is not None:
            response = self.client._get(f"/{self.endpoint}/{str(id)}")
            return purchaseOrder.from_json(response, self.client)
        elif PO_number is not None:
            orders = self.query_purchase_order(query=PO_number)
            for order in orders:
                if getattr(order, "number", None) == PO_number:
                    return self.get_purchase_order(order.id)
            raise ValueError(f"No purchase order found for purchase order {PO_number}")
        else:
            raise ValueError("Either 'id' or 'PO_number' must be provided.")

    def create_purchase_order(self, purchase_order: 'PurchaseOrder') -> 'purchaseOrder':
        """
        Create a new purchase order.

        Sends a POST request to the purchase order endpoint.

        Args:
            purchase_order (dict): A PurchaseOrder instance containing the purchase order details.

        Returns:
            purchaseOrder: The create PurchaseOrder instance.

        Raises:
            CreateRequestError: If the creation fails or response is invalid.
        """
        if hasattr(purchase_order, "model_dump_json"):  # Pydantic v2
            payload = json.loads(
                purchase_order.model_dump_json(
                    exclude_unset=True,
                    exclude_none=True,
                    by_alias=True,   # keep camelCase if you use aliases
                )
            )
        else:  # Pydantic v1 fallback
            payload = json.loads(
                purchase_order.json(
                    exclude_unset=True,
                    exclude_none=True,
                    by_alias=True,
                )
            )
        response = self.client._post(f"/{self.endpoint}", json=payload)
        if response.get('status_code') == 201:
            location = response.get('headers').get('location')
            parsed_url = urlparse(location)
            path_segments = parsed_url.path.rstrip("/").split("/")
            id = path_segments[-1]
            return self.get_purchase_order(id)
        else:
            error_message = response.get('content')
            raise CreateRequestError(self.endpoint, status_code=response.get('status_code'), error_message=error_message)
        
    def update_purchase_order(self, id: int, purchase_order: 'purchaseOrder') -> 'purchaseOrder':
        """
        Update an existing purchase order by ID.

        Sends a PUT request to the purchase order endpoint with the provided sales order data
        to update the existing record. Returns a wrapped `purchaseOrder` object containing
        the updated information.

        Args:
            id (int): The ID of the purchase order to update.
            purchase_order (PurchaseOrder): A PurchaseOrder instance with the purchase order details.

        Returns:
            purchaseOrder: An instance of the purchaseOrder wrapper class initialized with the 
                           updated data and client session.
        """
        if purchase_order.status == "I":
            raise ValueError(f"Cannot update an issued purchase order for {purchase_order.number}")
        else:
            response = self.client._put(f"/{self.endpoint}/{str(id)}", json=purchase_order.model_dump(exclude_none=True, exclude_unset=True))
        return purchaseOrder.from_json(response, self.client)

    def delete_purchase_order(self, id: int) -> bool:
        """
        Delete a purchase order by its ID.

        Sends a DELETE request to the purchase order endpoint to remove the specified
        purchase order from the system.

        Args:
            id (int): The ID of the purchase order to delete.

        Returns:
            bool: True if the sales order was successfully deleted, False otherwise.
        """
        order = self.get_purchase_order(id)
        if order.model.status in ("I", "R"):
            raise ValueError(f"Cannot delete an issued or received purchase order for {order.number}")
        else:
            return self.client._delete(f"/{self.endpoint}/{str(id)}")

    def query_purchase_order(
            self,
            *,
            query: Optional[str] = None,
            sort: Optional[Dict[str,str]] = None,
            filter: Optional[Dict[str, Any]] = None,
            all: bool = False,
            limit: int = 1000,
            start: int = 0,
            **extra_params
    ) -> List["purchaseOrder"]:
        """
        Query purchase orders with optional full-text search, filtering, multi-field sorting, and pagination.

        Args:
            query (str, optional): Full-text search string.
            sort (dict, optional): Dictionary of sorting rules (e.g., {"date": "desc", "number": "asc"}).
            filter (dict, optional): Dictionary of filters to apply (will be JSON-encoded and URL-safe).
            all (bool, optional): If True, retrieves all pages of results.
            limit (int, optional): Number of results per page (max 1000).
            start (int, optional): Starting offset for pagination.
            **extra_params (Any): Any additional parameters to include in the query.
        
        Returns:
            List[purchaseOrder]: List of wrapped purchase order resources.
        """
        return self.client._query(
            endpoint=self.endpoint,
            resource_cls=purchaseOrder,
            query=query,
            sort=sort,
            filter=filter,
            all=all,
            limit=limit,
            start=start,
            **extra_params
        )

    def issue_purchase_order(self, id:int) -> 'purchaseOrder':
        """
        Issue a purchase order by its ID.

        Sends a request to Spire to change the purchase order's status to
        “Issued”. Issuing an order typically means it has been confirmed
        and is ready to be sent to the vendor.

        Args:
            id (int): The ID of the purchaseOrder to issue.

        Returns:
            purchaseOrder: The updated purchase order object with the status set to "I" (Issued).

        Raises:
            CreateRequestError: If the request fails or the API returns an error status.
        """
        response = self.client._post(f"/{self.endpoint}/{str(id)}/issue")
        if response.get("status_code") != 200:
            raise CreateRequestError(f"Failed to issue purchase order: {id}: {response.text}")
        return purchaseOrder.from_json(response, self.client)

    def receive_purchase_order(self, id: int, receiveAll: bool = None) -> 'purchaseOrder':
        """
        Receive a purchase order by its ID.

        This updates the order in Spire to reflect that items have been received. 
        Typically, this should only be called on purchase orders with status "Issued".
       
        Args:
            id (int): The ID of the purchaseOrder to receive.
            receiveAll (bool, optional): An optional boolean to recieve all quantites on the purchase order.

        Returns:
            purchaseOrder: The updated purchase order object with the status set to "R" (Received).

        Raises: CreateRequestError: If the request fails or the API returns an error status.
        """
        if receiveAll:
            order = self.get_purchase_order(id)
            for item in order.model.items:
                item.receiveQty = item.orderQty
            order.update()
        response = self.client._post(f"/{self.endpoint}/{str(id)}/receive")
        if response.get("status_code") != 200:
            raise CreateRequestError(f"Failed to receive purchase order: {id}: {response.text}")
        return purchaseOrder.from_json(response, self.client)

class PurchasingHistoryClient:

    def __init__(self, client: SpireClient):
        self.client = client
        self.endpoint = "purchasing/history"

    def get_purchase_history_order(self, id: int = None, PO_number: str = None) -> 'purchaseOrder':
        """
        Retrieve an archived purchase order by its ID or PO number.

        Args:
            id (int, optional): The ID of the purchase order to retrieve.
            PO_number (str, optional): The purchase order number of the purchase order to retrieve.

        Returns:
            purchaseOrder: A `purchaseOrder` wrapper instance containing the retrieved data.

        Raises:
            ValueError: If neither id nor PO_number is provieded, or if no matching purchase order is found.
        """
        if id is not None:
            response = self.client._get(f"/{self.endpoint}/{str(id)}")
            return purchaseOrder.from_json(response, self.client)
        elif PO_number is not None:
            orders = self.query_purchase_history_order(query=PO_number)
            for order in orders:
                if getattr(order, "number", None) == PO_number:
                    return self.get_purchase_history_order(order.id)
            raise ValueError(f"No purchase order found for purchase order {PO_number}")
        else:
            raise ValueError("Either 'id' or 'PO_number' must be provided.")

    def query_purchase_history_order(
            self,
            *,
            query: Optional[str] = None,
            sort: Optional[Dict[str,str]] = None,
            filter: Optional[Dict[str, Any]] = None,
            all: bool = False,
            limit: int = 1000,
            start: int = 0,
            **extra_params
    ) -> List["purchaseOrder"]:
        """
        Query archived purchase orders with optional full-text search, filtering, multi-field sorting, and pagination.

        Args:
            query (str, optional): Full-text search string.
            sort (dict, optional): Dictionary of sorting rules (e.g., {"date": "desc", "number": "asc"}).
            filter (dict, optional): Dictionary of filters to apply (will be JSON-encoded and URL-safe).
            all (bool, optional): If True, retrieves all pages of results.
            limit (int, optional): Number of results per page (max 1000).
            start (int, optional): Starting offset for pagination.
            **extra_params (Any): Any additional parameters to include in the query.
        
        Returns:
            List[purchaseOrder]: List of wrapped purchase order resources.
        """
        return self.client._query(
            endpoint=self.endpoint,
            resource_cls=purchaseOrder,
            query=query,
            sort=sort,
            filter=filter,
            all=all,
            limit=limit,
            start=start,
            **extra_params
        )
  
class purchaseOrder(APIResource[PurchaseOrder]):
    endpoint = "purchasing/orders"
    Model = PurchaseOrder

    def issue(self) -> 'purchaseOrder':
        """
        Issue this purchase order.

        Sends a POST request to Spire to change the purchase order's status to
        “I” (Issued). Issuing an order typically means it has been confirmed
        and is ready to be sent to the vendor.

        Returns:
            purchaseOrder: The updated purchase order object with the status set to "I" (Issued).

        Raise:
            CreateRequestError: If the request fails or the API returns an error status.
        """
        response = self._client._post(f"/{self.endpoint}/{str(self.id)}/issue")
        if response.get("status_code") != 200:
            raise CreateRequestError(f"Failed to issue purchase order: {self.id}: {response.text}")
        return purchaseOrder.from_json(response, self._client)

    def delete(self) -> bool:
        """
        Cancels and deletes this purchase order.

        Sends a DELETE request to the API to remove the purchase order with the current ID.

        Returns:
            bool: True if the order was successfully deleted (HTTP 204 or 200), False otherwise.
        """
        return self._client._delete(f"/{self.endpoint}/{str(self.id)}")
    
    def update(self, order: "purchaseOrder" = None) -> 'purchaseOrder':
        """
        Update this sales order.

        If no purchase order object is provided, updates the current instance on the server.
        If a purchase order object is provided, updates the purchase order using the given data.

        Args:
            order (purchaseOrder, optional): An optional purchaseOrder instance to use for the update.

        Returns: 
            purchaseOrder: The updated purchaseOrder object reflecting the new status.
        """
        data = order.model_dump(exclude_unset=True, exclude_none=True) if order else self.model_dump(exclude_unset=True, exclude_none=True)
        response = self._client._put(f"/{self.endpoint}/{str(self.id)}", json=data)
        return purchaseOrder.from_json(response, self._client)
    
    def receive(self, receiveAll: bool = None) -> 'purchaseOrder':
        """
        Receive this purchase order.

        Sends a POST request to Spire to change the purchase order's status to
        "R" (Received). Receiving an order typically means the received quantites have been
        entered and the order is ready to be invoiced.

        Args:
            receiveAll (bool, optional): An optional boolean to recieve all quantites on the purchase order.

        Returns:
            purchaseOrder: The updated purchase order object with the status set to "R" (Received).
        
        Raise: 
            CreateRequestError: If the request fails or the API returns an error status.
        """
        if receiveAll:
            for item in self.model.items:
                item.receiveQty = item.orderQty
            self.update()
        response = self._client._post(f"/{self.endpoint}/{str(self.id)}/receive")
        if response.get('status_code') != 200:
            raise CreateRequestError(f"Failed to receive purchase order: {self.id}. (Check Order Quantites): {response.text}")
        return purchaseOrder.from_json(response, self._client)
      
        
        
            
    

