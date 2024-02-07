import awswrangler as wr
import pandas as pd

def lambda_handler(event, context):
    # Define the S3 path for the source CSV file
    source_path = 's3://fdasdata/ttb_open_positions.csv'
    
    # Define the S3 path for the processed (output) CSV file
    output_path = 's3://fdasdata/ttb_grouped_agg_open_positions.csv'

    # Reading the CSV file from S3 into a Pandas DataFrame with the correct delimiter
    df = wr.s3.read_csv(path=source_path)  # Defaults to comma as separator
    
    # Print the column names to verify they are as expected
    #print("Column names in the DataFrame:", df.columns.tolist())

    # Assuming you want to group by 'Symbol', 'Buy/sell', and 'Order comment'
    # and perform aggregation on 'Open date', 'Open time' (oldest) and 'Open price' (average).
    grouped_df = df.groupby(['Symbol', 'Buy/sell', 'Order comment']).agg({
        'Open date': 'min',  # Oldest 'Open date'
        'Open time': 'min',  # Oldest 'Open time'
        'Open price': 'mean',  # Average 'Open price'
        'Profit': 'sum',  # Sum of 'Profit'
        'Swap': 'sum',  # Sum of 'Swap'
        'Commission': 'sum',  # Sum of 'Commission'
        'Net profit': 'sum'  # Sum of 'Net profit'
    }).reset_index()

    # Writing the processed DataFrame back to S3 as CSV
    wr.s3.to_csv(df=grouped_df, path=output_path, index=False)

    return {
        'statusCode': 200,
        'body': 'Successfully processed and uploaded the file.'
    }