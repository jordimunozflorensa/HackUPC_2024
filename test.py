from services import order_item_manager
from services import order_list_manager

df = order_item_manager.OrderItemManager()

df.add_item("000309", "PROPOFOL LIPURO 1%- BRAUN VET 50ml", "5701170421316", 150)

df.modify_item("PROPOFOL LIPURO 1%- BRAUN VET 50ml", 20)

df.delete_item("PROPOFOL LIPURO 1%- BRAUN VET 50ml")


