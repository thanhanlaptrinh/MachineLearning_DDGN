/** Real Chromium tests. Install playwright; CHROMIUM_EXECUTABLE optionally overrides its browser path. */
import {createRequire} from 'node:module';import fs from 'node:fs/promises';import assert from 'node:assert/strict';
const require=createRequire(import.meta.url);const {chromium}=require('playwright');
const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_EXECUTABLE?{executablePath:process.env.CHROMIUM_EXECUTABLE}:{}),args:['--no-sandbox','--disable-dev-shm-usage','--disable-gpu']});
const page=await browser.newPage({viewport:{width:1440,height:1000}});const errors=[],checks=[];const base=process.env.DEMO_URL||'http://localhost:3000';
page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(['error','warning'].includes(m.type()))errors.push(m.text());});
async function route(path){await page.goto(base+'/#/'+path);await page.waitForFunction(()=>document.querySelector('#status')?.textContent.includes('5 mô hình'));}
function pass(n){checks.push(n);}
try{
 await route('data');await page.locator('#run-training-report').click();await page.locator('#holdout-model').waitFor();assert.ok((await page.locator('#training-status').textContent()).includes('Cả 5'));pass('Train/Test recomputes five saved models');
 for(const slug of ['linear','tree','forest','boosting','xgboost']){
  await route('predict/'+slug);await page.locator('#model-evidence table').waitFor();await page.locator('#lookup-id').fill('340');await page.locator('#lookup-button').click();await page.waitForFunction(()=>document.querySelector('#input-source')?.textContent.includes('340'));
  await page.locator('#run-single').click();await page.locator('#single-result .prediction').filter({hasText:'₫'}).waitFor();assert.equal(await page.locator('#single-error').textContent(),'');assert.equal(await page.locator('#single-metric option[value="mse"]').count(),0);pass(slug+' lookup/inference/trace and model evidence');
 }
 await page.locator('[data-area="GrLivArea"]').fill('100');assert.equal(Number(await page.locator('[name="GrLivArea"]').inputValue()),1076.4);pass('m² to sqft conversion');
 await route('compare');await page.locator('#use-demo').click();await page.locator('#run-batch').click();await page.locator('.scope-banner.green').waitFor();pass('30 holdout green banner');
 const chart=await page.locator('#chart-one').innerHTML();await page.locator('#metric-apply').click();assert.equal(await page.locator('#chart-one').innerHTML(),chart);pass('Chart controls independent');
 await page.locator('#use-train').click();await page.waitForFunction(()=>document.querySelector('#batch-name')?.textContent==='train-30');await page.locator('#run-batch').click();await page.locator('.scope-banner.red').waitFor();assert.ok((await page.locator('.scope-banner.red').textContent()).includes('30/30'));pass('30 train red warning');
 await route('process');await page.locator('a[download]').first().waitFor();assert.equal(await page.locator('#view .step').count(),8);pass('Process manifest and download links');
 assert.equal((await page.request.get(base+'/favicon.ico')).status(),204);pass('Favicon no 404');
 await page.setViewportSize({width:375,height:850});for(const r of ['data','predict/boosting','compare','process']){await route(r);await page.waitForTimeout(150);const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth+2);assert.equal(overflow,false,r+' mobile horizontal overflow');pass('Mobile '+r);}
 assert.deepEqual(errors,[]);pass('No console error or warning');
 await fs.writeFile(new URL('../results/verification_browser.json',import.meta.url),JSON.stringify({status:'PASS',passed:checks.length,failed:0,engine:'Chromium '+browser.version(),checks,errors},null,2));console.log('PASS',checks.length,'real-browser checks');
 if(process.env.QA_SCREENSHOT)await page.screenshot({path:process.env.QA_SCREENSHOT,fullPage:true});
}finally{await browser.close();}
