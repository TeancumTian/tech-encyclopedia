// Run after UI edits: npm install --prefix tools/localization && node scripts/extract_ui.cjs
const fs = require('node:fs');
const crypto = require('node:crypto');
const {spawnSync} = require('node:child_process');
const acorn = require(process.env.TECH_I18N_PARSER || '../tools/localization/node_modules/acorn');
const files=['app.js','book-reader.js','reading.js','review.js','learning.js','storage.js','browser-storage.js'];
const strings=new Set(), hashes={};
function visit(node) {
  if(!node || typeof node!=='object')return;
  if(node.type==='Literal' && typeof node.value==='string' && /[\u3400-\u9fff]/.test(node.value))strings.add(node.value);
  if(node.type==='TemplateLiteral') {
    const value=node.quasis.map((q,i)=>(q.value.cooked||q.value.raw)+(i<node.expressions.length?'{'+i+'}':'')).join('');
    if(/[\u3400-\u9fff]/.test(value))strings.add(value);
  }
  for(const value of Object.values(node)) {if(Array.isArray(value))value.forEach(visit);else if(value&&typeof value==='object')visit(value);}
}
for(const file of files) {
  const path='web/'+file, source=fs.readFileSync(path,'utf8');
  hashes[path]=crypto.createHash('sha256').update(source).digest('hex');
  visit(acorn.parse(source,{ecmaVersion:'latest',sourceType:'module'}));
}
const result=spawnSync('python3',['scripts/collect_ui.py'],{input:JSON.stringify({sources:hashes,strings:[...strings]}),encoding:'utf8'});
process.stdout.write(result.stdout||'');process.stderr.write(result.stderr||'');process.exit(result.status||0);
