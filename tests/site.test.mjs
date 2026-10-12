import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,readdirSync,existsSync,statSync} from 'node:fs';
import {join,resolve} from 'node:path';
import {load} from 'cheerio';
const root=resolve('dist');
function files(dir){return readdirSync(dir).flatMap(f=>{const p=join(dir,f);return statSync(p).isDirectory()?files(p):[p]});}
const pages=files(root).filter(p=>p.endsWith('.html'));
test('static pages have metadata, one heading, and valid local links',()=>{
assert.ok(pages.length>=10);
for(const page of pages){const $=load(readFileSync(page,'utf8'));assert.equal($('h1').length,1,page);assert.ok($('title').text(),page);assert.ok($('meta[name=description]').attr('content'),page);assert.ok($('link[rel=canonical]').attr('href')?.startsWith('https://poytaytoy.github.io/'),page);
for(const el of $('a[href]').toArray()){const href=$(el).attr('href');if(!href.startsWith('/')&&!href.startsWith('#'))continue;const [path,hash]=href.split('#');const target=path?join(root,path):page;const destination=target.endsWith('/')||existsSync(target)&&statSync(target).isDirectory()?join(target,'index.html'):target;assert.ok(existsSync(destination),`${page} -> ${href}`);if(hash&&destination.endsWith('.html')){const targetDoc=load(readFileSync(destination,'utf8'));assert.ok(targetDoc(`[id="${decodeURIComponent(hash)}"]`).length,`${page} -> missing anchor ${href}`);}}
}});
test('technical writing renders math, highlighted code, TOC, and interactive component',()=>{const $=load(readFileSync(join(root,'writing/smoothing-noisy-signals/index.html'),'utf8'));assert.ok($('.katex').length>3);assert.ok($('pre.astro-code span[style]').length>10);assert.ok($('nav[aria-label="Table of contents"] a').length>=5);assert.ok($('signal-lab input[type=range]').length===1);});
test('diagram example and syndication are present',()=>{assert.match(readFileSync(join(root,'writing/state-machines/index.html'),'utf8'),/data-diagram/);assert.match(readFileSync(join(root,'rss.xml'),'utf8'),/Finding the signal in the noise/);assert.ok(existsSync(join(root,'sitemap-index.xml')));});
