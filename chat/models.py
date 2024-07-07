from dynamorm import Dyn

# Configure DynamORM to use the local DynamoDB instance
Dyn.configure(
    endpoint_url='http://localhost:8000',
    aws_access_key_id='your_access_key_id',
    aws_secret_access_key='your_secret_access_key',
    region_name='your_region'
)

# Define the first table model
class Table1(Dyn.Table):
    table_name = 'table1'
    schema = {
        'id': str,
        'name': str
    }

# Define the second table model
class Table2(Dyn.Table):
    table_name = 'table2'
    schema = {
        'id': str,
        'email': str
    }