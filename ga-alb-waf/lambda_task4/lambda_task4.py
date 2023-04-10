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

    wafId = stackOutputParams.get("WAFId", {})

    ipsetName = "SecurityAllowedIPs"
    ipAddresses = [
        '1.2.3.4/32',
        '5.6.7.8/32'
    ]

    wafClient = boto3.client('wafv2')

    result = wafClient.list_ip_sets(
        Scope='REGIONAL'
    )

    if len(result['IPSets']):
        ipset = list(filter(lambda a: a['Name'] == ipsetName, result['IPSets']))

        if (ipset):
            ipsetName = ipset[0]['Name']
            ipsetId = ipset[0]['Id']

            result = wafClient.get_ip_set(
                Scope='REGIONAL',
                Name=ipsetName,
                Id=ipsetId,
            )

            addresses = result['IPSet']['Addresses']

            if len(addresses) == 2 and addresses.sort() == ipAddresses.sort():
                # check for IPSet Rule

                result = wafClient.get_web_acl(
                    Name='SecurityWAF',
                    Scope='REGIONAL',
                    Id=wafId
                )

                try:
                    ruleAllowedIPSet = list(
                        filter(lambda a: a['Name'] == 'SecurityAllowedIPsRule', result['WebACL']['Rules']))

                    if len(ruleAllowedIPSet):
                        priority = ruleAllowedIPSet[0]['Priority']
                        headerName = ruleAllowedIPSet[0]['Statement']['IPSetReferenceStatement']['IPSetForwardedIPConfig']['HeaderName']
                        actionName = ruleAllowedIPSet[0]['Action']['Allow']['CustomRequestHandling']['InsertHeaders'][0]['Name']
                        actionValue = ruleAllowedIPSet[0]['Action']['Allow']['CustomRequestHandling']['InsertHeaders'][0]['Value']

                        if priority == 0 and \
                                headerName == 'X-Client-Ip' and \
                                actionName == 'Authorization' and \
                                actionValue == 'QWxsb3dlZElwcw==':
                            completed = True
                            message = "The challenge has been completed"
                except Exception as e:
                    print(e)
                finally:
                    return {
                        "completed": completed,  # required: whether this task is completed
                        "message": message,  # required: a message to display to the team indicating progress or next steps
                        "progressPercent": 0,  # optional: any whole number between 0 and 100
                        "metadata": {},  # optional: a map of key:value attributes to display to the team
                    }

    return {
        "completed": completed,  # required: whether this task is completed
        "message": message,  # required: a message to display to the team indicating progress or next steps
        "progressPercent": 0,  # optional: any whole number between 0 and 100
        "metadata": {},  # optional: a map of key:value attributes to display to the team
    }
