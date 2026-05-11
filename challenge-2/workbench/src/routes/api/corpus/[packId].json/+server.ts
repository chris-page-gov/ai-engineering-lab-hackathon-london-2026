import { error, json } from '@sveltejs/kit';
import { loadCorpusFromDisk } from '$lib/server/corpus';
import type { RequestHandler } from './$types';

export const prerender = true;

export const entries = () => [{ packId: 'hmrc-narrative' }];

export const GET: RequestHandler = async ({ params }) => {
  if (params.packId !== 'hmrc-narrative') {
    throw error(404, 'Corpus pack not found');
  }
  return json(await loadCorpusFromDisk(undefined, params.packId));
};
