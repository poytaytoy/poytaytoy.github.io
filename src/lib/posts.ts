import { getCollection } from 'astro:content';
export const getPosts = async () => (await getCollection('posts', ({data}) => !data.draft))
  .sort((a,b) => b.data.date.valueOf() - a.data.date.valueOf());
export const formatDate = (date: Date) => date.toLocaleDateString('en-US', {month:'short', day:'numeric', year:'numeric', timeZone:'UTC'});
