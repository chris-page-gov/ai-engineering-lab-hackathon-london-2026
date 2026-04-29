import { error } from '@sveltejs/kit';
import { loadCorpusFromDisk } from '$lib/server/corpus';
import type { RequestHandler } from './$types';

export const prerender = true;

export const entries = async () => {
  const corpus = await loadCorpusFromDisk();
  return corpus.sources.map((source) => ({ sourceId: source.sourceId }));
};

export const GET: RequestHandler = async ({ params }) => {
  const corpus = await loadCorpusFromDisk();
  const source = corpus.sources.find((candidate) => candidate.sourceId === params.sourceId);
  if (!source) {
    throw error(404, 'Source note not found');
  }
  return new Response(source.noteText, {
    headers: {
      'content-type': 'text/markdown; charset=utf-8',
    },
  });
};
