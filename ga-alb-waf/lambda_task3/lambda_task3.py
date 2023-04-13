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
    wafId = stackOutputParams.get("WAFId", {})

    result = wafClient.get_web_acl(
        Name='SecurityWAF',
        Scope='REGIONAL',
        Id=wafId
    )

    if len(result['WebACL']['Rules']) > 1:
        try:
            ruleCommonRulesSet = list(
                filter(lambda a: a['Name'] == 'AWS-AWSManagedRulesCommonRuleSet', result['WebACL']['Rules']))
            ruleRateBased = list(filter(lambda a: a['Name'] == 'RateBasedRule', result['WebACL']['Rules']))

            if len(ruleCommonRulesSet) and len(ruleRateBased):
                limit = ruleRateBased[0]['Statement']['RateBasedStatement']['Limit']
                searchString = ruleRateBased[0]['Statement']['RateBasedStatement']['ScopeDownStatement']['ByteMatchStatement']['SearchString']
                fieldToMatch = ruleRateBased[0]['Statement']['RateBasedStatement']['ScopeDownStatement']['ByteMatchStatement']['FieldToMatch']
                positionalConstraint = ruleRateBased[0]['Statement']['RateBasedStatement']['ScopeDownStatement']['ByteMatchStatement'][
                    'PositionalConstraint']
                action = ruleRateBased[0]['Action']

                if limit == 100 and \
                        searchString == b'login' and \
                        fieldToMatch == {'UriPath': {}} and \
                        positionalConstraint == 'ENDS_WITH' and \
                        action.get('Block') == {}:
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

