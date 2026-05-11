import { browser } from '$app/environment';
import type { PageLoad } from './$types';

export const prerender = true;
export const ssr = false;

export const load: PageLoad = async ({ fetch }) => {
  const search = browser ? new URLSearchParams(window.location.search) : new URLSearchParams();
  const pack = search.get('pack') === 'hmrc-narrative' ? 'hmrc-narrative' : 'challenge-2';
  const corpusUrl = pack === 'challenge-2' ? '/api/corpus.json' : `/api/corpus/${pack}.json`;
  const response = await fetch(corpusUrl);
  if (!response.ok) {
    throw new Error(`Unable to load corpus: ${response.status}`);
  }
  return {
    corpus: await response.json(),
    pack,
  };
};
