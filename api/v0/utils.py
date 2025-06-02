from Models.sales import *
from typing import Optional
from typing import TypeVar, Type
import re
from copy import deepcopy

T = TypeVar('T', bound=BaseModel)

def create_sales_order_from_invoice(invoice: Invoice) -> SalesOrder:

    """ Creates A Sales Order from an Invoice """

    return SalesOrder(
        orderNo=invoice.orderNo,
        division=invoice.division,
        location=invoice.location,
        profitCenter=invoice.profitCenter,
        customer=deepcopy(invoice.customer),
        currency=deepcopy(invoice.currency),
        status = "O",
        type="O",
        hold = False,
        orderDate=invoice.orderDate,
        address=create_duplicate_record(invoice.address),
        shippingAddress=create_duplicate_record(invoice.shippingAddress),
        customerPO=invoice.customerPO,
        fob=invoice.fob,
        incoterms=invoice.incoterms,
        incotermsPlace=invoice.incotermsPlace,
        referenceNo=invoice.referenceNo,
        shippingCarrier=invoice.shippingCarrier,
        shipDate=invoice.shipDate,
        trackingNo=invoice.trackingNo,
        termsCode=invoice.termsCode,
        termsText=invoice.termsText,
        freight=invoice.freight,
        subtotal=invoice.subtotal,
        total=invoice.total,
        items = [create_duplicate_record(item) for item in invoice.items or []],
        payments=deepcopy(invoice.payments),
        udf=deepcopy(invoice.udf),
    )


def create_duplicate_record(instance: T, exclude_fields: Optional[list[str]] = None) -> T:
    """
    Create a copy of a Pydantic model instance excluding fields like `id`, links, and any others specified.

    Args:
        instance (T): The Pydantic model instance to duplicate.
        exclude_fields (Optional[list[str]]): Additional field names to exclude.

    Returns:
        T: A new instance of the same model with specified fields excluded.
    """
    if exclude_fields is None:
        exclude_fields = []

    # Default fields to exclude
    fields_to_exclude = {'id', 'linkTable', 'linkType', 'linkNo'}
    fields_to_exclude.update(exclude_fields)

    # Create a dict excluding these fields
    data = instance.model_dump(exclude={field: True for field in fields_to_exclude})

    # Return a new instance of the same class
    return instance.__class__(**data)