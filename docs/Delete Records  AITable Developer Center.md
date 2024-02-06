-   [](https://developers.aitable.ai/)
-   [Record](https://developers.aitable.ai/api/record)
-   Delete Records

We will show you how to [Delete records](https://developers.aitable.ai/api/reference#operation/delete-records).

## Example: delete the two records for the specified datasheet[](https://developers.aitable.ai/api/create-records#example-delete-the-two-records-for-the-specified-datasheet "Direct link to Example: delete the two records for the specified datasheet")

Assuming you have a datasheet, you would like to delete two of these records.

Your action steps below:

1.  Get your API Token.([How to get it](https://developers.aitable.ai/api/quick-start#get-api-token))
    
2.  Get the ID of the datasheet.([How to get it](https://developers.aitable.ai/api/introduction#datasheetid))
    
3.  Gets the ID of the 2 records you want to delete.([How to get it](https://developers.aitable.ai/api/introduction#recordid))
    
4.  Open the terminal on your computer, execute the following code and send the query request to the server (assuming datasheetId is `dstWUHwzTHd2YQaXEE`, two record Id is `recADeOmeoJHg` and `recpveDCZYO`):
    
    -   cURL
    -   Javascript SDK
    -   Python SDK
    
    ```
    <span><span>curl</span><span> -X DELETE </span><span>\</span><span></span><br></span><span><span></span><span>'https://aitable.ai/fusion/v1/datasheets/dstWUHwzTHd2YQaXEE/records?recordIds=recADeOmeoJHg,recfCpveDCZYO'</span><span> </span><span>\</span><span></span><br></span><span><span>-H </span><span>'Authorization: Bearer {Your API Token}'</span><br></span>
    ```
    
5.  The server returns the following JSON data, below the `"views"` is all data in this view:
    
    > For the meaning of each parameter in the response, please check the [API Reference](https://developers.aitable.ai/api/reference#operation/delete-records)
    > 
    > ```
    > <span><span>    </span><span>{</span><span></span><br></span><span><span>   </span><span>"success"</span><span>:</span><span> </span><span>true</span><span>,</span><span></span><br></span><span><span>   </span><span>"code"</span><span>:</span><span> </span><span>200</span><span>,</span><span></span><br></span><span><span>   </span><span>"message"</span><span>:</span><span> </span><span>"SUCCESS"</span><span>,</span><span></span><br></span><span><span>   </span><span>"data"</span><span>:</span><span> </span><span>true</span><span></span><br></span><span><span></span><span>}</span><br></span>
    > ```
    

[

Previous

Update Records

](https://developers.aitable.ai/api/update-records)[

Next

Field

](https://developers.aitable.ai/api/field)