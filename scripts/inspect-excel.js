const XLSX = require('xlsx');
const path = require('path');

// Try both files
const files = [
  'C:\\Users\\Farruxjon\\Downloads\\Oxford_3000_36_katak_WORD_POS_bitta_katak.xlsx',
  'C:\\Users\\Farruxjon\\Downloads\\Oxford_3000_36_katak_aralashtirilgan.xlsx'
];

for (const filePath of files) {
  try {
    console.log('\n========================================');
    console.log('FILE:', path.basename(filePath));
    console.log('========================================');
    
    const workbook = XLSX.readFile(filePath);
    
    console.log('Sheet names:', workbook.SheetNames);
    
    for (const sheetName of workbook.SheetNames) {
      const sheet = workbook.Sheets[sheetName];
      const range = XLSX.utils.decode_range(sheet['!ref'] || 'A1');
      console.log(`\nSheet: "${sheetName}"`);
      console.log(`Range: ${sheet['!ref']}`);
      console.log(`Rows: ${range.e.r - range.s.r + 1}, Cols: ${range.e.c - range.s.c + 1}`);
      
      // Show first 20 rows
      const data = XLSX.utils.sheet_to_json(sheet, { header: 1, defval: '' });
      console.log('\nFirst 20 rows:');
      for (let i = 0; i < Math.min(20, data.length); i++) {
        console.log(`Row ${i}: ${JSON.stringify(data[i])}`);
      }
      
      // Show last 5 rows
      console.log('\nLast 5 rows:');
      for (let i = Math.max(0, data.length - 5); i < data.length; i++) {
        console.log(`Row ${i}: ${JSON.stringify(data[i])}`);
      }
      
      console.log('\nTotal rows with data:', data.length);
    }
  } catch (e) {
    console.log(`Error reading ${filePath}:`, e.message);
  }
}
