const rawData = data.message.split('\n').slice(1).map(row => row.split(',')).map(cols => ({
    Symbol: cols[0],
    'Buy/sell': cols[1],
    'Order comment': cols[2],
    'Open date': cols[3],
    'Open time': cols[4],
    'Open price': parseFloat(cols[5]),
    Lots: parseFloat(cols[6]), // Parse 'Lots' as a float
    Profit: parseFloat(cols[7]),
    Swap: parseFloat(cols[8]),
    Commission: parseFloat(cols[9]),
    'Net profit': parseFloat(cols[10])
  }));
  
  const grouped = {};
  
  rawData.forEach(item => {
    const key = `${item.Symbol}|${item['Buy/sell']}|${item['Order comment']}`;
    if (!grouped[key]) {
      grouped[key] = { ...item, Count: 1 };
    } else {
      const group = grouped[key];
      group.Profit += item.Profit;
      group.Swap += item.Swap;
      group.Commission += item.Commission;
      group.Lots += item.Lots; // Sum 'Lots' for each item in the group
      group['Net profit'] += item['Net profit'];
      group['Open price'] = (group['Open price'] * group.Count + item['Open price']) / (group.Count + 1); // Recalculate average
      group.Count += 1;
    }
  });
  
  const result = Object.values(grouped).map(item => ({
    Symbol: item.Symbol,
    'Buy/sell': item['Buy/sell'],
    'Order comment': item['Order comment'],
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