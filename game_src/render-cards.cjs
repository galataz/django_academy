// npm install && npx playwright install chromium && npm run render:cards
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require('playwright');
const {buildSync} = require('esbuild');
const root = path.resolve(__dirname, '..');
(async () => {
 const bundle = buildSync({entryPoints:[path.join(__dirname, 'card-art.js')],bundle:true,write:false,format:'iife',target:'es2020'}).outputFiles[0].text;
 const browser = await chromium.launch({headless:true,...(process.env.CARD_CHROMIUM_PATH ? {executablePath:process.env.CARD_CHROMIUM_PATH} : {})});
 try {
  const page = await browser.newPage({viewport:{width:640,height:420}});
  await page.setContent('<div id="destination-label"></div>');
  await page.addScriptTag({content:bundle});
  await page.waitForFunction(() => window.cardRendererReady);
  const specs = JSON.parse(fs.readFileSync(path.join(__dirname, 'card-specs.json'), 'utf8'));
  fs.mkdirSync(path.join(root,'static/cards'), {recursive:true});
  for (const section of ['units','lessons']) for (const spec of Object.values(specs[section])) {
   const data = await page.evaluate(s => window.renderCard(s), spec);
   fs.writeFileSync(path.join(root,'static',spec.file), Buffer.from(data.split(',')[1], 'base64'));
  }
  console.log('Miniaturas WebP exportadas según card-specs.json.');
 } finally {await browser.close();}
})().catch(error => {console.error(error);process.exitCode=1;});
