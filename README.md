# HackUPC_2024

pip install SpeechRecognition fuzzywuzzy

sudo apt-get install python3-pyaudio

pip install python-Levenshtein

pip install google-cloud-speech

## Execution to avoid a pile of messasges 
python3 main.py 2> errores.log

## TSP Implementation
we assume that the employer departs from the [0,0,0] position and ends it's traject also there.

S3
class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"
        data = [(1, 10), (2, 20), (3, 30), (4, 40), (5, 50)]

        file_name = "/tmp/data.csv"
        bucket_name = "b2496363-ec72-4d36-8a04-3572e490548d-us-east-1"
        object_key = "data.csv"
        
        try:
            with open(file_name, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerows(data)
            s3.upload_file(file_name, bucket_name, object_key)
            
            logger.info("Data saved to S3://%s/%s", bucket_name, object_key)

        except ClientError as e:
            logger.error("Error uploading data to S3: %s", str(e))
            raise e

class CargarListaHandler(CargarListaHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CargarListaHandler")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        download_file_path = "/tmp/data.csv"
        bucket_name = "b2496363-ec72-4d36-8a04-3572e490548d-us-east-1"
        object_key = "data.csv"
        
        try:
            s3.download_file(bucket_name, object_key, download_file_path)
            with open(download_file_path, 'r') as csvfile:
                csv_reader = csv.reader(csvfile)
                # ya tienes el csv en el /tmp/data.csv
 
            logger.info("Data saved to S3://%s/%s", bucket_name, object_key)

        except ClientError as e:
            logger.error("Error uploading data to S3: %s", str(e))
            raise e
