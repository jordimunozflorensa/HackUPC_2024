# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
#from lambda_session import get_session_data

from ask_sdk_model import Response

from services import order_list_manager as olm
from services import order_item_manager as oim

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
import pandas as pd
import re
import os

archivo_csv = 'data/products.csv'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hola, puedes decir crearOrden o Help. ¿Cual quieres probar?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class KarakuloHandler(AbstractRequestHandler):
    """Handler for agregar item {nombre} Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("Karakulo")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        contenido_slot = slots.get('contenido')
        if contenido_slot and contenido_slot.value:
            best_match = find_medication(contenido_slot.value)
            handler_input.attributes_manager.session_attributes['contenido'] = best_match
            speak_output = f"Orden creada: {handler_input.attributes_manager.session_attributes['contenido']}"
        else:
            speak_output = "No se encontró el valor de 'contenido'"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class KaraQttHandler(AbstractRequestHandler):
    """Handler for cantidad {numero} Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        #return handler_input.attributes_manager.session_attributes.get('contenido') is not None
        return ask_utils.is_intent_name("KaraQtt")(handler_input)
        
    def handle(self, handler_input):
        try:
            contenido = handler_input.attributes_manager.session_attributes['contenido']
            slots = handler_input.request_envelope.request.intent.slots
            cantidad = slots.get('cantidad').value
            
            df = pd.read_csv("data/products.csv", delimiter=';')
            var = df[df["name"] == contenido]
            var1 = var.values[0].tolist()
            var1.append(cantidad)
            item_manager = oim.OrderItemManager()
            item_manager.add_item(str(var1[0]), str(var1[1]), str(var1[2]), str(var1[3]))
            
            # speak_output = f"Orden creada con éxito: con {cantidad} unidades"
            speak_output = f"Orden creada: {cantidad} unidades de {contenido}"
        except Exception as e:
            speak_output = f"{e}"
        # Implementar la lógica para guardar la orden en S3
        return (
            handler_input.response_builder
               .speak(speak_output)
               .ask(speak_output)
               .response
        )


class KrakrikraHandler(AbstractRequestHandler):
    """Handler for Crear Lista Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        #return handler_input.attributes_manager.session_attributes.get('contenido') is not None
        return ask_utils.is_intent_name("Krakrikra")(handler_input)
        
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

class KaraBlaBlaHandler(AbstractRequestHandler):
    """Handler for TEST Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        #return handler_input.attributes_manager.session_attributes.get('contenido') is not None
        return ask_utils.is_intent_name("KaraBlaBla")(handler_input)
        
    def handle(self, handler_input):
        
        list_manager = olm.OrderListManager()
        item_manager = oim.OrderItemManager()
        list_manager.create_order_list()
        
        item_manager.add_item("hola","CALIERCORTIN 4mg/ml- 50ml iny", "adios", "10")
        item_manager.add_item("hola","CRCORTIN 4mg/ml- 50ml iny", "adios", "10")
        item_manager.add_item("hola","CALIERTIN 4mg/ml- 50ml iny", "adios", "10")
        item_manager.add_item("hola","CALIERCfdsafsdjofadsoORTIN 4mg/ml- 50ml iny", "adios", "10")
        item_manager.add_item("adios","ADTAB GATO 12mg 0,5-2kg 1cp", "adios", "15")
        #df = pd.read_csv("data/products.csv", delimiter=';')
        #contenido = "CALIERCORTIN 4mg/ml- 50ml iny"
        #var = df[df["name"] == contenido]
        #var1 = var.values[0].tolist()
        #var1.append("5")
        #item_manager.add_item(str(var1[0]), str(var1[1]), str(var1[2]), str(var1[3]))
        
        #contenido = "ADTAB GATO 12mg 0,5-2kg 1cp"
        #var = df[df["name"] == contenido]
        #var1 = var.values[0].tolist()
        #var1.append("8")
        #item_manager.add_item(str(var1[0]), str(var1[1]), str(var1[2]), str(var1[3]))
        
        #speak_output = f"{var1}"
        speak_output = "hola"
        return (
            handler_input.response_builder
               .speak(speak_output)
               .ask(speak_output)
               .response
        )

class KaraPlinHandler(AbstractRequestHandler):
    """Handler for Eliminar Item Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("KaraPlin")(handler_input)
        
    def handle(self, handler_input):
        try:
            slots = handler_input.request_envelope.request.intent.slots
            contenido_slot = slots.get('contenido')
            #speak_output = f"{contenido_slot}"
            if contenido_slot and contenido_slot.value:
                best_match = find_medication(contenido_slot.value)
                item_manager = oim.OrderItemManager()
                item_manager.delete_item(best_match)
                speak_output = f"Item {best_match} eliminado"
            else:
                speak_output = "No se encontró el valor de 'contenido'"
        except Exception as e:
            speak_output = f"{e}"
        return (
            handler_input.response_builder
               .speak(speak_output)
               .ask(speak_output)
               .response
        )

medications = []

with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
    # Leer el archivo CSV
    lector_csv = csv.reader(csvfile, delimiter=';')
    # Iterar sobre cada fila del archivo
    for fila in lector_csv:
        # Agregar el elemento de la segunda columna a la lista
        medications.append(fila[1])
    # Eliminar el encabezado
    medications = medications[1:]
    #print("Medications:", medications)
    
def find_medication(input_text):
    max_similarity = 0
    best_match = None
    print("Input text:", input_text)
    for medication in medications:
        similarity = fuzz.ratio(input_text, medication.lower())
        if similarity > max_similarity:
            print("Similarity:", similarity, "Medication:", medication)
            max_similarity = similarity
            best_match = medication
    return best_match

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(KarakuloHandler())
sb.add_request_handler(KaraQttHandler())
sb.add_request_handler(KrakrikraHandler())
sb.add_request_handler(KaraBlaBlaHandler())

sb.add_request_handler(KaraPlinHandler())


sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()