import rss from '@astrojs/rss';
import {getPosts} from '../lib/posts';
import type {APIContext} from 'astro';
export async function GET(context:APIContext){return rss({title:'Clement — a working notebook',description:'Notes on code, systems, and the ideas underneath.',site:context.site!,items:(await getPosts()).map(p=>({title:p.data.title,pubDate:p.data.date,description:p.data.description,link:`/writing/${p.id}/`}))});}
