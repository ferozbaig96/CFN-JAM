import json
import socket

def lambda_handler(event, context):
  
  # Available data provided in the event
  eventTitle = event.get("eventTitle", None)
  challengeTitle = event.get("challengeTitle", None)
  taskTitle = event.get("taskTitle", None)
  teamDisplayName = event.get("teamDisplayName", None)
  userInput = event.get("userInput", None) # <-- userInput only available if using the 'Lambda With Input' validation type
  stackOutputParams = event.get("stackOutputParams", {})
  
  completed = False
  message = "Not yet completed"
  
  address = stackOutputParams.get("InstanceIpAddress", {})
  port = 22
  s = socket.socket()
  s.settimeout(3)
  try:
    s.connect((address, int(port)))
    s.shutdown(socket.SHUT_RDWR)
    completed = True
    message = "The challenge has been completed"
  except Exception as e:
    print("something's wrong with %s:%d. Exception is %s" % (address, port, e))
  finally:
    s.close()
  
  return {
    "completed": completed, # required: whether this task is completed
    "message": message, # required: a message to display to the team indicating progress or next steps
    "progressPercent": 0, # optional: any whole number between 0 and 100
    "metadata": {}, # optional: a map of key:value attributes to display to the team
  }