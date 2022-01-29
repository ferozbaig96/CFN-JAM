import boto3
import json
import socket

score = 0
ec2Client = boto3.client('ec2')

# VPCID = event.get("VPCId", {})
VPCID = 'vpc-8c995af6'

rules = ec2Client.describe_security_groups(
  Filters=[
    {
      'Name': 'vpc-id',
      'Values': [ VPCID ]
    },
    {
      'Name': 'group-name',
      'Values': [ 'MyWebDMZ' ]
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
          score = 60
          completed = True
          message = "The challenge has been completed"

# address = event.get("ServerIPAddress", {})
address = "52.73.191.204"
port = 22
s = socket.socket()
s.settimeout(3)
try:
  s.connect((address, int(port)))
  s.shutdown(socket.SHUT_RDWR)
  score += 40
except Exception as e:
  print("something's wrong with %s:%d. Exception is %s" % (address, port, e))
  score += 0
finally:
  s.close()
