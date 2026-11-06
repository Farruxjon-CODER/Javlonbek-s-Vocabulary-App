/**
 * Excel to JSON converter for Oxford 3000 vocabulary dataset
 * Runs the canonical column-major generator that reads the Excel sheet
 * column-by-column (top-to-bottom, columns 1 through 36).
 */
import { spawnSync } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const scriptPath = path.resolve(__dirname, 'generate_canonical_vocabulary.py');
console.log('🚀 Running canonical vocabulary generator:', scriptPath);

const result = spawnSync('python', [scriptPath], { stdio: 'inherit' });
if (result.status !== 0) {
  console.error('❌ Generation failed with exit code:', result.status);
  process.exit(result.status || 1);
} else {
  console.log('✅ Canonical vocabulary generation succeeded.');
}


