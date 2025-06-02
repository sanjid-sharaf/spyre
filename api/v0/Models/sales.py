from typing import List, Optional, Dict, Union
from pydantic import BaseModel

class PhoneFax(BaseModel):
    number: str
    format: Optional[int] = 1

class Contact(BaseModel):
    id: Optional[int] = None
    contact_type: Optional[dict] = 1
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[PhoneFax] = None
    fax: Optional[PhoneFax] = None


class Salesperson(BaseModel):
    code: Optional[str] = None
    name: Optional[str] = None


class Territory(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None


class Address(BaseModel):
    id: Optional[int] = None
    type: Optional[str] = None
    linkTable: Optional[str] = None
    linkType: Optional[str] = None
    linkNo: Optional[str] = None
    shipId: Optional[str] = None
    name: Optional[str] = None
    line1: Optional[str] = None
    line2: Optional[str] = None
    line3: Optional[str] = None
    line4: Optional[str] = None
    city: Optional[str] = None
    postalCode: Optional[str] = None
    provState: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[PhoneFax] = None
    fax: Optional[PhoneFax] = None
    email: Optional[str] = None
    website: Optional[str] = None
    shipCode: Optional[str] = None
    shipDescription: Optional[str] = None
    salesperson: Optional[Salesperson] = None
    territory: Optional[Territory] = None
    sellLevel: Optional[int] = None
    glAccount: Optional[str] = None
    defaultWarehouse: Optional[str] = None
    udf: Optional[dict] = None
    created: Optional[str] = None
    modified: Optional[str] = None
    contacts: Optional[List[Contact]] = None
    salesTaxes: Optional[List[Dict[str, Union[int, str]]]] = None


class Currency(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    description: Optional[str] = None
    country: Optional[str] = None
    units: Optional[str] = None
    fraction: Optional[str] = None
    symbol: Optional[str] = None
    decimalPlaces: Optional[int] = None
    symbolPosition: Optional[str] = None
    rate: Optional[str] = None
    rateMethod: Optional[str] = None
    glAccountNo: Optional[str] = None
    thousandsSeparator: Optional[str] = None
    lastYearRate: Optional[List[str]] = None
    thisYearRate: Optional[List[str]] = None
    nextYearRate: Optional[List[str]] = None


class Customer(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    customerNo: Optional[str] = None
    name: Optional[str] = None
    foregroundColor: Optional[int] = None
    backgroundColor: Optional[int] = None


class Inventory(BaseModel):
    id: Optional[int] = None
    whse: Optional[str] = None
    partNo: Optional[str] = None
    description: Optional[str] = None


class Item(BaseModel):
    id: Optional[int] = None
    orderNo: Optional[str] = None
    sequence: Optional[int] = None
    parentSequence: Optional[int] = None
    inventory: Optional[Inventory] = None
    serials: Optional[str] = None
    whse: Optional[str] = None
    partNo: Optional[str] = None
    description: Optional[str] = None
    comment: Optional[str] = None
    orderQty: Optional[str] = None
    committedQty: Optional[str] = None
    backorderQty: Optional[str] = None
    sellMeasure: Optional[str] = None
    retailPrice: Optional[str] = None
    unitPrice: Optional[str] = None
    userPrice: Optional[bool] = None
    discountable: Optional[bool] = None
    discountPct: Optional[str] = None
    discountAmt: Optional[str] = None
    currentCost: Optional[str] = None
    averageCost: Optional[str] = None
    standardCost: Optional[str] = None
    taxFlags: Optional[List[bool]] = None
    vendor: Optional[str] = None
    inventoryAccountNo: Optional[str] = None
    revenueAccountNo: Optional[str] = None
    costOfGoodsAccountNo: Optional[str] = None
    levyCode: Optional[str] = None
    referenceNo: Optional[str] = None
    requiredDate: Optional[str] = None
    extendedPriceOrdered: Optional[str] = None
    extendedPriceCommitted: Optional[str] = None
    kit: Optional[bool] = None
    suppress: Optional[bool] = None
    udf: Optional[dict] = None


class Tax(BaseModel):
    code: Optional[int] = None
    name: Optional[str] = None
    shortName: Optional[str] = None
    rate: Optional[Union[str, int]] = None
    exemptNo: Optional[str] = None
    total: Optional[Union[str, int]] = None


class SalesOrder(BaseModel):
    id: Optional[int] = None
    orderNo: Optional[str] = None
    division: Optional[str] = None
    location: Optional[str] = None
    profitCenter: Optional[str] = None
    invoiceNo: Optional[str] = None
    customer: Optional[Customer] = None
    creditApprovedAmount: Optional[str] = None
    creditApprovedDate: Optional[str] = None
    creditApprovedUser: Optional[str] = None
    currency: Optional[Currency] = None
    status: Optional[str] = None
    type: Optional[str] = None
    hold: Optional[bool] = None
    orderDate: Optional[str] = None
    invoiceDate: Optional[str] = None
    requiredDate: Optional[str] = None
    quoteExpires: Optional[str] = None
    recurrenceRule: Optional[str] = None
    address: Optional[Address] = None
    shippingAddress: Optional[Address] = None
    contact: Optional[Contact] = None
    customerPO: Optional[str] = None
    batchNo: Optional[str] = None
    fob: Optional[str] = None
    incoterms: Optional[str] = None
    incotermsPlace: Optional[str] = None
    referenceNo: Optional[str] = None
    shippingCarrier: Optional[str] = None
    shipDate: Optional[str] = None
    trackingNo: Optional[str] = None
    termsCode: Optional[str] = None
    termsText: Optional[str] = None
    freight: Optional[str] = None
    taxes: Optional[List[Tax]] = None
    subtotal: Optional[str] = None
    subtotalOrdered: Optional[str] = None
    discount: Optional[str] = None
    totalDiscount: Optional[str] = None
    total: Optional[str] = None
    totalOrdered: Optional[str] = None
    totalCostCurrent: Optional[str] = None
    totalCostAverage: Optional[str] = None
    grossProfit: Optional[str] = None
    items: Optional[List[Item]] = None
    payments: Optional[List[dict]] = None
    udf: Optional[dict] = None
    createdBy: Optional[str] = None
    modifiedBy: Optional[str] = None
    created: Optional[str] = None
    modified: Optional[str] = None
    deletedBy: Optional[str] = None
    deleted: Optional[str] = None
    links: Optional[Dict[str, str]] = None


class Invoice(BaseModel):
    id: Optional[int] = None
    invoiceNo: Optional[str] = None
    orderNo: Optional[str] = None
    division: Optional[str] = None
    location: Optional[str] = None
    profitCenter: Optional[str] = None
    customer: Optional['Customer'] = None
    currency: Optional['Currency'] = None
    orderDate: Optional[str] = None
    invoiceDate: Optional[str] = None
    requiredDate: Optional[str] = None
    address: Optional['Address'] = None
    shippingAddress: Optional['Address'] = None
    customerPO: Optional[str] = None
    fob: Optional[str] = None
    incoterms: Optional[str] = None
    incotermsPlace: Optional[str] = None
    referenceNo: Optional[str] = None
    shippingCarrier: Optional[str] = None
    shipDate: Optional[str] = None
    trackingNo: Optional[str] = None
    termsCode: Optional[str] = None
    termsText: Optional[str] = None
    freight: Optional[str] = None
    taxes: Optional[List['Tax']] = None
    subtotal: Optional[str] = None
    total: Optional[str] = None
    items: Optional[List['Item']] = None
    payments: Optional[List[dict]] = None
    udf: Optional[dict] = None
    createdBy: Optional[str] = None
    modifiedBy: Optional[str] = None
    created: Optional[str] = None
    modified: Optional[str] = None
    links: Optional[Dict[str, str]] = None