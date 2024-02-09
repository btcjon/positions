const rawData = data.message.split('\n').slice(1).map(row => row.split(',')).map(cols => ({
    Symbol: cols[0],
    'Buy/sell': cols[1],
    'Open date': cols[2],
    'Open time': cols[3],
    'Open price': parseFloat(cols[4]),
    Lots: parseFloat(cols[5]),
    Profit: parseFloat(cols[6]),
    Swap: parseFloat(cols[7]),
    Commission: parseFloat(cols[8]),
    'Net profit': parseFloat(cols[9])
  }));
  
  const grouped = {};
  
  rawData.forEach(item => {
    // Adjusted key to exclude 'Order comment'
    const key = `${item.Symbol}|${item['Buy/sell']}`;
    if (!grouped[key]) {
      grouped[key] = { ...item, Count: 1 };
    } else {
      const group = grouped[key];
      group.Profit += item.Profit;
      group.Swap += item.Swap;
      group.Commission += item.Commission;
      group.Lots += item.Lots;
      group['Net profit'] += item['Net profit'];
      // Adjust average open price calculation
      group['Open price'] = (group['Open price'] * group.Count + item['Open price']) / (group.Count + 1);
      group.Count += 1;
    }
  });
  
  const result = Object.values(grouped).map(item => ({
    Symbol: item.Symbol,
    'Buy/sell': item['Buy/sell'],
    'Total Profit': item.Profit,
    'Total Swap': item.Swap,
    'Lots': item.Lots,
    'Total Commission': item.Commission,
    'Total Net Profit': item['Net profit'],
    'Average Open Price': item['Open price'],
    'Count': item.Count
  }));
  
  // Sort the result by 'Lots' from largest to smallest
  result.sort((a, b) => b.Lots - a.Lots);
  
  return result;