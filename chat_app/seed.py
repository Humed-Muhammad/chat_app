from settings import DYNAMODB_TABLES, dynamodb

for table_name, table_config in DYNAMODB_TABLES.items():
    table = dynamodb.create_table(
        TableName=table_config['table_name'],
        KeySchema=table_config['key_schema'],
        AttributeDefinitions=table_config['attribute_definitions'],
        ProvisionedThroughput=table_config['provisioned_throughput']
    )
    table.meta.client.get_waiter('table_exists').wait(TableName=table_config['table_name'])