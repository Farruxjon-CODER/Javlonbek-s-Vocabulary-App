/**
 * Vocabulary dataset validator
 * Verifies completeness and quality of the vocabulary dataset
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Support passing target file as argument, defaulting to vocabulary.json or vocabulary.enriched.json
let targetFile = process.argv[2];
if (!targetFile) {
  const enrichedPath = path.resolve(__dirname, '..', 'public', 'data', 'vocabulary.enriched.json');
  const standardPath = path.resolve(__dirname, '..', 'public', 'data', 'vocabulary.json');
  if (fs.existsSync(enrichedPath)) {
    targetFile = enrichedPath;
  } else {
    targetFile = standardPath;
  }
} else {
  targetFile = path.resolve(process.cwd(), targetFile);
}

if (!fs.existsSync(targetFile)) {
  console.error(`File not found: ${targetFile}`);
  process.exit(1);
}

const data = JSON.parse(fs.readFileSync(targetFile, 'utf-8'));

let definitionsComplete = 0;
let definitionsMissing = 0;
let meaningUzComplete = 0;
let meaningUzMissing = 0;
let examplesComplete = 0;
let examplesMissing = 0;
let cefrComplete = 0;
let cefrMissing = 0;
let posComplete = 0;
let posMissing = 0;

let duplicateIds = 0;
let duplicateWordPOS = 0;
let invalidEntries = 0;
let multipleSensesCount = 0;

const seenIds = new Set();
const seenWordPOS = new Set();

const unresolvedEntries = [];

for (const entry of data) {
  let isInvalid = false;

  // ID check
  if (!entry.id || typeof entry.id !== 'number') {
    invalidEntries++;
    isInvalid = true;
  } else {
    if (seenIds.has(entry.id)) {
      duplicateIds++;
    }
    seenIds.add(entry.id);
  }

  // Word check
  if (!entry.word || typeof entry.word !== 'string' || !entry.word.trim()) {
    invalidEntries++;
    isInvalid = true;
  }

  // Word + POS duplicate check
  const wordPosKey = `${(entry.word || '').toLowerCase()}_${(entry.pos || '').toLowerCase()}`;
  if (seenWordPOS.has(wordPosKey)) {
    duplicateWordPOS++;
  }
  seenWordPOS.add(wordPosKey);

  // POS
  if (entry.pos && entry.pos.trim()) {
    posComplete++;
  } else {
    posMissing++;
  }

  // CEFR
  if (entry.cefr && entry.cefr.trim()) {
    cefrComplete++;
  } else {
    cefrMissing++;
  }

  // Definition
  const hasDef = (entry.definition && entry.definition.trim().length > 0) || 
                 (Array.isArray(entry.senses) && entry.senses.some(s => s.definition && s.definition.trim().length > 0));
  if (hasDef) {
    definitionsComplete++;
  } else {
    definitionsMissing++;
    unresolvedEntries.push({ id: entry.id, word: entry.word, issue: 'Missing definition' });
  }

  // Uzbek meaning
  const hasUz = (entry.meaningUz && entry.meaningUz.trim().length > 0) ||
                (Array.isArray(entry.senses) && entry.senses.some(s => s.meaningUz && s.meaningUz.trim().length > 0));
  if (hasUz) {
    meaningUzComplete++;
  } else {
    meaningUzMissing++;
  }

  // Example
  const hasEx = (entry.example && entry.example.trim().length > 0) ||
                (Array.isArray(entry.senses) && entry.senses.some(s => s.example && s.example.trim().length > 0));
  if (hasEx) {
    examplesComplete++;
  } else {
    examplesMissing++;
  }

  if (Array.isArray(entry.senses) && entry.senses.length > 1) {
    multipleSensesCount++;
  }
}

console.log('========================================');
console.log('LEXIFLOW VOCABULARY VALIDATION');
console.log('========================================\n');
console.log(`Total entries: ${data.length}\n`);

console.log('Definitions:');
console.log(`Complete: ${definitionsComplete}`);
console.log(`Missing: ${definitionsMissing}\n`);

console.log('Uzbek meanings:');
console.log(`Complete: ${meaningUzComplete}`);
console.log(`Missing: ${meaningUzMissing}\n`);

console.log('Examples:');
console.log(`Complete: ${examplesComplete}`);
console.log(`Missing: ${examplesMissing}\n`);

console.log('CEFR:');
console.log(`Complete: ${cefrComplete}`);
console.log(`Missing: ${cefrMissing}\n`);

console.log('POS:');
console.log(`Complete: ${posComplete}`);
console.log(`Missing: ${posMissing}\n`);

console.log(`Duplicate IDs: ${duplicateIds}`);
console.log(`Duplicate word/POS: ${duplicateWordPOS}\n`);

console.log(`Invalid entries: ${invalidEntries}\n`);
console.log(`Multiple senses: ${multipleSensesCount}\n`);
console.log('========================================');

if (unresolvedEntries.length > 0) {
  console.log(`\n⚠️  Unresolved entries (${unresolvedEntries.length}):`);
  unresolvedEntries.slice(0, 10).forEach(e => console.log(` - ID ${e.id}: ${e.word} (${e.issue})`));
}
