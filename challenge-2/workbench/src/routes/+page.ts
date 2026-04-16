import type { PageLoad } from './$types';

export const prerender = true;

export const load: PageLoad = async ({ fetch }) => {
  const response = await fetch('/api/corpus.json');
  if (!response.ok) {
    throw new Error(`Unable to load corpus: ${response.status}`);
  }
  return {
    corpus: await response.json(),
  };
};
