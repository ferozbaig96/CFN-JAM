import json
import boto3

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
  
  cognitoIdpClient = boto3.client('cognito-idp')
  UserPoolId = stackOutputParams.get("UserPoolId", {})
  
  response = cognitoIdpClient.list_users(UserPoolId=UserPoolId)
  
  if (response['Users']):
    completed = True
    message = "The challenge has been completed"
  else:
    message = "No users added to the Amazon Cognito user pool. Please test the lambda function to create user"
  
  return {
    "completed": completed, # required: whether this task is completed
    "message": message, # required: a message to display to the team indicating progress or next steps
    "progressPercent": 0, # optional: any whole number between 0 and 100
    "metadata": {}, # optional: a map of key:value attributes to display to the team
  }