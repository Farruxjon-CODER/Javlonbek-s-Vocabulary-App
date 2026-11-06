const XLSX = require('xlsx');

const filePath = 'C:\\Users\\Farruxjon\\Downloads\\Oxford_3000_36_katak_WORD_POS_bitta_katak (1).xlsx';

try {
  const workbook = XLSX.readFile(filePath);
  console.log('Sheet names:', workbook.SheetNames);
  
  for (const sheetName of workbook.SheetNames) {
    const sheet = workbook.Sheets[sheetName];
    const range = XLSX.utils.decode_range(sheet['!ref'] || 'A1');
    console.log(`\nSheet: "${sheetName}"`);
    console.log(`Range: ${sheet['!ref']}`);
    console.log(`Rows: ${range.e.r - range.s.r + 1}, Cols: ${range.e.c - range.s.c + 1}`);
    
    const data = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: '' });
    console.log('\nFirst 30 rows:');
    for (let i = 0; i < Math.min(30, data.length); i++) {
      console.log(`Row ${i}: ${JSON.stringify(data[i])}`);
    }
    
    console.log('\nTotal rows with data:', data.length);
  }
} catch (e) {
  console.log('Error:', e.message);
}
