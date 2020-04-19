import csv
import boto3

def main(): 
    client = boto3.Session(region_name='us-east-2', aws_access_key_id='', aws_secret_access_key='').client('dynamodb')
    
    # Write to Dynamo DB
    table_name = "foo"
    params = {
        'TableName' : table_name, 
        'KeySchema': [       
            { 'AttributeName': "timestamp", 'KeyType': "HASH"}    # Partition key
        ],
        'AttributeDefinitions': [       
            { 'AttributeName': "timestamp", 'AttributeType': "S" }
        ],
        'ProvisionedThroughput': {       
            'ReadCapacityUnits': 10, 
            'WriteCapacityUnits': 10
        }
    }

    # Create the table
    client.create_table(**params)

    # Wait for the table to exist before exiting
    print('Waiting for {} ...'.format(table_name))
    waiter = client.get_waiter('table_exists')
    waiter.wait(TableName=table_name)

    with open('form_responses.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            print(' || '.join(row))

            params = {
                "TableName": table_name,
                "Item": {
                    "timestamp": {
                        "S": row[0]
                    },
                    "type": {
                        "S": row[1]
                    },
                    "pending_date": {
                        "S": row[2]
                    },
                    "approved_date": {
                        "S": row[3]
                    },
                    "state": {
                        "S": row[4]
                    },
                    "nfa_item_type": {
                        "S": row[5]
                    },
                    "form_type": {
                        "S": row[6]
                    },
                    "duration": {
                        "S": row[7]
                    }
                }
            }
            response = client.put_item(**params)

            print("Response:[{}]".format(response))

if __name__ == '__main__':
    main()
