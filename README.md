# Spire API Python Client

A robust and extensible Python client for interacting with the [Spire Business Software API](https://developer.spiresystems.com/reference). This client provides an object-oriented interface to get, create, update, delete, query, filter, sort, and manage various Spire modules such as Sales Orders, Invoices, Inventory Items, and more.

---

## ✨ Features

- ✅ Object-oriented resource wrappers for each module (e.g., `salesOrder`, `invoice`, `item`)
- 🔍 Full-text search via `q` parameter
- 🔁 Pagination with `start` and `limit` support
- 🧾 JSON-based advanced filtering (supports `$gt`, `$lt`, `$in`, `$or`, etc.)
- ↕️ Multi-field sorting with ascending/descending control
- 🔧 Clean abstraction layer for API endpoints
- 📦 Powered by `pydantic` models for validation

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuration

- How to set up your spire client

### Find Your Spire Domain
https://{your-spire-domain}/api/v2/companies/

### Set up your client with your credentials

```python
from spyre import Spire

client = Spire(host = 'your-spire-domain', company = 'comapany-name' , username = 'username' , password = 'password' )

```

## Example : Updating the status of an inventory item 
```python
item = client.inventory.items.get_item(1101)    # Gets item with id 1101
item.status = 1                                 # Use either item. or item.model. . item.model. will bring up all attributes
item.update()
```