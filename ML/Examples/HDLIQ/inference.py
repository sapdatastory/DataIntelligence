import json

# Global vars to keep track of model status
model = None
model_ready = False

# Validate input data is JSON
def is_json(data):
  try:
    json_object = json.loads(data)
  except ValueError as e:
    return False
  return True

# When Model Blob reaches the input port
def on_model(model_blob):
    global model
    global model_ready

    #model = model_blob
    import pickle
    model = pickle.loads(model_blob)
    model_ready = True
    api.logger.info("Model Received & Ready")

# Client POST request received
def on_input(msg):
    error_message = ""
    success = False
    prediction = None # This line needs to be added
    try:
        api.logger.info("POST request received from Client - checking if model is ready")
        if model_ready:
            api.logger.info("Model Ready")
            api.logger.info("Received data from client - validating json input")
            
            user_data = msg.body.decode('utf-8')
            # Received message from client, verify json data is valid
            if is_json(user_data):
                api.logger.info("Received valid json data from client - ready to use")
                
                # apply your model
                # obtain your results
                hm_minutes = json.loads(user_data)['half_marathon_minutes']
                prediction = model.predict([[hm_minutes]])
                success = True
            else:
                api.logger.info("Invalid JSON received from client - cannot apply model.")
                error_message = "Invalid JSON provided in request: " + user_data
                success = False
        else:
            api.logger.info("Model has not yet reached the input port - try again.")
            error_message = "Model has not yet reached the input port - try again."
            success = False
    except Exception as e:
        api.logger.error(e)
        error_message = "An error occurred: " + str(e)
    
    if success:
        # apply carried out successfully, send a response to the user
        #msg.body = json.dumps({'Results': 'Model applied to input data successfully.'})
        msg.body = json.dumps({'marathon_minutes_prediction': round(prediction[0], 1)})
    else:
        msg.body = json.dumps({'Error': error_message})
    
    api.send('output', msg)
    
api.set_port_callback("model", on_model)
api.set_port_callback("input", on_input)
