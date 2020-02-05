import boto3

def lambda_handler(event, context):
    sagemakerClient = boto3.client('sagemaker')
    sagemakerList = sagemakerClient.list_notebook_instances(StatusEquals='InService')

    while sagemakerList:
        for instance in sagemakerList['NotebookInstances']:
            noShutdown = sagemakerClient.list_tags(ResourceArn=instance['NotebookInstanceArn'])
            print(noShutdown)
            if 'NoShutdown' not in [t['Key'] for t in noShutdown['Tags']]:
                response = sagemakerClient.stop_notebook_instance(NotebookInstanceName=instance['NotebookInstanceName'])
                return 200
        sagemakerList = sagemakerClient.list_notebook_instances(
            NextToken=sagemakerList['NextToken']) if 'NextToken' in sagemakerList else None