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
  
  ec2Client = boto3.client('ec2')
  VPCID = stackOutputParams.get("VPCId", {})
  
  rules = ec2Client.describe_security_groups(
    Filters=[
      {
        'Name': 'vpc-id',
        'Values': [ VPCID ]
      },
      {
        'Name': 'group-name',
        'Values': [ 'JAMSG' ]
      }
    ]
  )
  
  for rule in range (len(rules["SecurityGroups"][0]['IpPermissions'])):
    ipPermission = rules['SecurityGroups'][0]['IpPermissions'][rule]
    if ipPermission['IpRanges']:
      if ipPermission['IpRanges'][0]['CidrIp'] == "0.0.0.0/0" :
        if ipPermission['IpProtocol'] == "tcp" :
          # Only SSH Access
          if ipPermission['FromPort'] == 22 and ipPermission['ToPort'] == 22 :
            completed = True
            message = "The challenge has been completed"
  
  return {
    "completed": completed, # required: whether this task is completed
    "message": message, # required: a message to display to the team indicating progress or next steps
    "progressPercent": 0, # optional: any whole number between 0 and 100
    "metadata": {}, # optional: a map of key:value attributes to display to the team
  }