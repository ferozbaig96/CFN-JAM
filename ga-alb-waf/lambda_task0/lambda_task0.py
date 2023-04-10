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

    gaClient = boto3.client('globalaccelerator', region_name='us-west-2')
    globalAcceleratorListenerArn = stackOutputParams.get("GlobalAcceleratorListenerArn", {})
    albArn = stackOutputParams.get("ALBArn", {})

    result = gaClient.list_endpoint_groups(
        ListenerArn=globalAcceleratorListenerArn
    )

    if len(result['EndpointGroups'][0]['EndpointDescriptions']):
        endpointDescriptions = result['EndpointGroups'][0]['EndpointDescriptions']

        for endpointDescription in endpointDescriptions:
            if endpointDescription['EndpointId'] == albArn:
                completed = True
                message = "The challenge has been completed"

    return {
        "completed": completed,  # required: whether this task is completed
        "message": message,  # required: a message to display to the team indicating progress or next steps
        "progressPercent": 0,  # optional: any whole number between 0 and 100
        "metadata": {},  # optional: a map of key:value attributes to display to the team
    }
