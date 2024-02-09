// Assuming `data.message` contains the corrected CSV string
const csvString = data.message;

// Split the CSV string into an array of lines
const lines = csvString.split('\r\n');

// Extract headers
const headers = lines[0].split(',');

// Map each line to an object, skipping the first line (headers)
const transformedData = lines.slice(1).map(line => {
  const values = line.split(',');
  const obj = headers.reduce((acc, header, index) => {
    // Convert numeric fields to numbers
    const numericFields = ['Lots', 'Open price', 'Close price', 'Profit', 'Swap', 'Commission', 'Net profit', 'T/P', 'S/L', 'Pips', 'Trade duration (hours)'];
    if (numericFields.includes(header)) {
      acc[header] = parseFloat(values[index]);
    } else {
      acc[header] = values[index];
    }
    return acc;
  }, {});
  return obj;
});

// Return the transformed data
return transformedData;