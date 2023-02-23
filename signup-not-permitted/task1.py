import boto3

def lambda_handler(event, context):
    
    score = 0
    print(event)
    Output = event['outputs']
    print(Output)
    UserPoolId = list(filter(lambda x : x['OutputKey'] == 'UserPoolId', Output))[0]['OutputValue']
    print(UserPoolId)
    
    client = boto3.client('cognito-idp')
    
    response = client.describe_user_pool(
    UserPoolId = UserPoolId
    )
    
    config = response['UserPool']['AdminCreateUserConfig']['AllowAdminCreateUserOnly']
    print(config)
    
    response1 = client.list_users(UserPoolId=UserPoolId)
    
    if(config == False):
        score = 50
        if (response1['Users']):
            score = 100
    
    return {
        "totalScore": score,
        "splitScore": { 
            "Resolver": score 
        }
    }
