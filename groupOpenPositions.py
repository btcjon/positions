import awswrangler as wr
import pandas as pd

def lambda_handler(event, context):
    # Define the S3 path for the source CSV file
    source_path = 's3://fdasdata/open_positions.csv'
    
    # Define the S3 path for the processed (output) CSV file
    output_path = 's3://fdasdata/grouped_open_positions.csv'

    # Reading the CSV file from S3 into a Pandas DataFrame with the correct delimiter
    df = wr.s3.read_csv(path=source_path)  # Defaults to comma as separator
    
    # Print the column names to verify they are as expected
    #print("Column names in the DataFrame:", df.columns.tolist())

    # Assuming you want to group by 'Symbol', 'Buy/sell', and 'Order comment'
    # and perform some aggregation or simply want to restructure the DataFrame.
    # Here's a simple example of grouping without aggregation:
    grouped_df = df.groupby(['Symbol', 'Buy/sell', 'Order comment']).apply(lambda x: x)

    # Reset index if you've done grouping that may affect the DataFrame index
    grouped_df = grouped_df.reset_index(drop=True)

    # Writing the processed DataFrame back to S3 as CSV
    wr.s3.to_csv(df=grouped_df, path=output_path, index=False)

    return {
        'statusCode': 200,
        'body': 'Successfully processed and uploaded the file.'
    }