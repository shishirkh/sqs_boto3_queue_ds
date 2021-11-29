import boto3
sqs=boto3.client(
    'sqs',
    aws_access_key_id='',
    aws_secret_access_key='',
    region_name='us-east-1'
)

def create_queue(name_of_queue):
    create_queue_response=sqs.create_queue(QueueName=name_of_queue)
    return create_queue_response

def get_queue_url(name_of_queue):
    queue_url=sqs.get_queue_url(QueueName=name_of_queue)
    return queue_url['QueueUrl']
    
def delete_queue(name_of_queue):
    queue_url=get_queue_url(name_of_queue)
    delete_queue_response=sqs.delete_queue(QueueUrl=queue_url)
    return delete_queue_response

def push(name_of_queue,body):
    queue_url=get_queue_url(name_of_queue)
    response=sqs.send_message(
        QueueUrl=queue_url,
        DelaySeconds=10,
        MessageAttributes={
            'NameOfQueue':{
                'DataType':'String',
                'StringValue':name_of_queue
            }
        },
        MessageBody=body
    )
    #print(response['MessageId'])
    return response

def get_head(name_of_queue):
    queue_url=get_queue_url(name_of_queue)
    response=sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    print(response)
    #print(response['Messages'][0]['Body'])
    return response#['Messages'][0]['Body']

def pop(name_of_queue):
    queue_url=get_queue_url(name_of_queue)
    response=sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0
    )
    message=response['Messages'][0]
    receipt_handle=message['ReceiptHandle']
    delete_message_response=sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    return delete_message_response

create_queue('test4')

#push('test4','one')
#push('test4','two')

get_head('test4')

