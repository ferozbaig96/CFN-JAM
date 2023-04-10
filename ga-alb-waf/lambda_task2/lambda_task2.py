import boto3


def lambda_handler(event, context):
    # Available data provided in the event
    eventTitle = event.get("eventTitle", None)
    challengeTitle = event.get("challengeTitle", None)
    taskTitle = event.get("taskTitle", None)
    teamDisplayName = event.get("teamDisplayName", None)
    userInput = event.get("userInput",
                          None)  # <-- userInput only available if using the 'Lambda With Input' validation type
    stackOutputParams = event.get("stackOutputParams", {})

    completed = False
    message = "Not yet completed"

    wafClient = boto3.client('wafv2')
    wafArn = stackOutputParams.get("WAFArn", {})
    albArn = stackOutputParams.get("ALBArn", {})

    result = wafClient.list_resources_for_web_acl(
        WebACLArn=wafArn
    )

    if len(result['ResourceArns']):
        if albArn in result['ResourceArns']:
            completed = True
            message = "The challenge has been completed"

    return {
        "completed": completed,  # required: whether this task is completed
        "message": message,  # required: a message to display to the team indicating progress or next steps
        "progressPercent": 0,  # optional: any whole number between 0 and 100
        "metadata": {},  # optional: a map of key:value attributes to display to the team
    }
