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
  
  routes = ec2Client.describe_route_tables(
    Filters=[
      {
        'Name': 'vpc-id',
        'Values': [ VPCID ]
      },
      {
        'Name': 'association.main',
        'Values': [ 'false' ]
      }
    ]
  )
  
  igw = ec2Client.describe_internet_gateways(
    Filters=[
      {
        'Name': 'attachment.vpc-id',
        'Values': [ VPCID ]
      }
    ]
  )
  
  IGWID = igw['InternetGateways'][0]['InternetGatewayId']
  
  for route in range(len(routes['RouteTables'][0]['Routes'])):
    if routes['RouteTables'][0]['Routes'][route]['DestinationCidrBlock'] == '0.0.0.0/0':
      if 'GatewayId' in routes['RouteTables'][0]['Routes'][route]:
        if routes['RouteTables'][0]['Routes'][route]['GatewayId'] == IGWID:
          completed = True
          message = "The challenge has been completed"
  
  return {
    "completed": completed, # required: whether this task is completed
    "message": message, # required: a message to display to the team indicating progress or next steps
    "progressPercent": 0, # optional: any whole number between 0 and 100
    "metadata": {}, # optional: a map of key:value attributes to display to the team
  }