import pandas as pd

df = pd.read_csv("products.csv", delimiter=';')
contenido = "CALIERCORTIN 4mg/ml- 50ml iny"
var = df[df["name"] == contenido]
var1 = var.values[0].tolist()
var1.append("5")
new_row = {"id": var1[0], "name": var1[1], "ean": var1[2], "quantity": var1[3]}

print(var1)

Karakulo -> agregar producto
KaraQtt -> cantidad
KaraBlaBla -> test
KaraPlin -> Eliminar producto
Krakrikra -> Crear lista
Krisafel -> Importar lista
Kruchuc -> Guardar lista

class KaraPlinHandler(AbstractRequestHandler):
    """Handler for Eliminar Item Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("KaraPlin")(handler_input)
        
    def handle(self, handler_input):
        list_manager = olm.OrderListManager()
        list_manager.create_order_list()
        speak_output = "Lista creada con exito!"
        return (
            handler_input.response_builder
               .speak(speak_output)
               .ask(speak_output)
               .response
        )

class KrisafelHandler(AbstractRequestHandler):
    """Handler for Importar Lista Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Krisafel")(handler_input)
        
    def handle(self, handler_input):
        list_manager = olm.OrderListManager()
        list_manager.create_order_list()
        speak_output = "Lista creada con exito!"
        return (
            handler_input.response_builder
               .speak(speak_output)
               .ask(speak_output)
               .response
        )
        
class KruchucHandler(AbstractRequestHandler):
    """Handler for Guardar Lista Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Kruchuc")(handler_input)
        
    def handle(self, handler_input):
        list_manager = olm.OrderListManager()
        list_manager.create_order_list()
        speak_output = "Lista creada con exito!"
        return (
            handler_input.response_builder
               .speak(speak_output)
               .ask(speak_output)
               .response
        )


sb.add_request_handler(KaraPlinHandler())
sb.add_request_handler(KrisafelHandler())
sb.add_request_handler(KruchucHandler())