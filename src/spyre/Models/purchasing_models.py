from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, model_validator
from .shared_models import Vendor, Address, Currency, Contact

class InventoryRef(BaseModel):
    id: Optional[int] = None
    whse: Optional[str] = None
    partNo: Optional[str] = None
    description: Optional[str] = None

class PurchaseOrderItem(BaseModel):
    id: Optional[int] = None
    whse: Optional[str] = None
    partNo: Optional[str] = None
    sequence: Optional[int] = None
    inventory: Optional[InventoryRef] = None
    serials: Optional[Any] = None
    description: Optional[str] = None
    orderQty: Optional[str] = None
    receiveQty: Optional[str] = None
    receivedQty: Optional[str] = None
    unitPrice: Optional[str] = None
    freight: Optional[str] = None
    purchaseMeasure: Optional[str] = None
    taxFlags: Optional[List[bool]] = None
    udf: Optional[Dict[str,Any]] = None
    requiredDate: Optional[str] = None
    referenceNo: Optional[str] = None
    comment: Optional[str] = None

class PurchaseOrder(BaseModel):
    id: Optional[int] = None
    number: Optional[str] = None
    vendor: Optional[Vendor] = None
    currency: Optional[Union[Currency, Dict[str, Any]]] = None
    status: Optional[str] = None
    Date: Optional[str] = None
    requiredDate: Optional[str] = None
    address: Optional[Address] = None
    shippingAddress: Optional[Address] = None
    vendorPO: Optional[str] = None
    referenceNo: Optional[str] = None
    fob: Optional[str] = None
    incoterms: Optional[str] = None
    incotermsPlace: Optional[str] = None
    subtotal: Optional[str] = None
    total: Optional[str] = None
    deposit: Optional[str] = None
    items: Optional[List[PurchaseOrderItem]] = None
    udf: Optional[Dict[str,Any]] = None
    createdBy: Optional[str] = None
    modifiedBy: Optional[str] = None
    created: Optional[str] = None
    modified: Optional[str] = None
    links: Optional[Dict[str,str]] = None

    @model_validator(mode="before")
    @classmethod
    def clean_problematic_fields(cls, data: dict) -> dict:
        if data.get("currency") == "":
            data["currency"] = None

        contact = data.get("contact")
        if contact:
            for field in ("phone", "fax"):
                phone_data = contact.get(field)
                if isinstance(phone_data, dict) and phone_data.get("number") is None:
                    phone_data["number"] = ""
        return data








