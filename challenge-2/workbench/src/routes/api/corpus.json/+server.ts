import { json } from '@sveltejs/kit';
import { loadCorpusFromDisk } from '$lib/server/corpus';

export const prerender = true;

export async function GET() {
  return json(await loadCorpusFromDisk());
}
