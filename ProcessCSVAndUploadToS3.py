import boto3
import csv
import urllib.request

# Initialize the S3 client
s3 = boto3.client('s3')

def lambda_handler(event, context):
    csv_url = 'https://www.fxblue.com/users/compoundit/csv'
    bucket_name = 'fdasdata'
    
    # Download CSV to /tmp directory
    local_csv_path = '/tmp/original.csv'
    urllib.request.urlretrieve(csv_url, local_csv_path)
    
    # Initialize paths for temporary split files
    open_positions_path = '/tmp/ttb_open_positions.csv'
    closed_positions_path = '/tmp/ttb_closed_positions.csv'
    
    # Process and split the file
    with open(local_csv_path, mode='r') as infile, \
         open(open_positions_path, mode='w', newline='') as open_file, \
         open(closed_positions_path, mode='w', newline='') as closed_file:
        
        reader = csv.reader(infile)
        open_writer = csv.writer(open_file)
        closed_writer = csv.writer(closed_file)
        
        # Skip the first row (sep=,)
        next(reader)
        
        # Read the next row as headers
        headers = next(reader)
        
        # Write headers to each file
        open_writer.writerow(headers)
        closed_writer.writerow(headers)
        
        for row in reader:
            if row[0] == 'Open position':
                open_writer.writerow(row)
            elif row[0] == 'Closed position':
                closed_writer.writerow(row)
    
    # Upload the split files to S3
    s3.upload_file(Filename=open_positions_path, Bucket=bucket_name, Key='open_positions.csv')
    s3.upload_file(Filename=closed_positions_path, Bucket=bucket_name, Key='closed_positions.csv')

    return {
        'statusCode': 200,
        'body': 'Successfully processed and uploaded the CSV files.'
    }