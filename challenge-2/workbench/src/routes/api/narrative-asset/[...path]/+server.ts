import { readFile } from 'node:fs/promises';
import { error } from '@sveltejs/kit';
import { narrativeAssetEntries, narrativeAssetPath } from '$lib/server/corpus';
import type { RequestHandler } from './$types';

export const prerender = true;

const NOTE_CARD_SVG = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 360" role="img" aria-label="Narrative note">
  <rect width="640" height="360" rx="18" fill="#f7faf9"/>
  <rect x="56" y="58" width="528" height="244" rx="14" fill="#ffffff" stroke="#b8c7c4" stroke-width="4"/>
  <path d="M112 118h336M112 166h416M112 214h300" stroke="#24564f" stroke-width="22" stroke-linecap="round"/>
  <circle cx="486" cy="246" r="42" fill="#d9eee9" stroke="#2f766d" stroke-width="10"/>
  <path d="M470 245l14 14 28-34" fill="none" stroke="#15413c" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>
</svg>`;

export const entries = narrativeAssetEntries;

const contentType = (path: string) => {
  if (path.endsWith('.svg')) return 'image/svg+xml; charset=utf-8';
  if (path.endsWith('.jpg') || path.endsWith('.jpeg')) return 'image/jpeg';
  if (path.endsWith('.png')) return 'image/png';
  return 'application/octet-stream';
};

export const GET: RequestHandler = async ({ params }) => {
  const assetPath = params.path;
  if (assetPath === 'assets/note-card.svg') {
    return new Response(NOTE_CARD_SVG, {
      headers: { 'content-type': contentType(assetPath), 'cache-control': 'public, max-age=3600' },
    });
  }
  let resolved: string;
  try {
    resolved = narrativeAssetPath(assetPath) ?? '';
  } catch {
    throw error(404, 'Narrative asset not found');
  }
  if (!resolved) {
    throw error(404, 'Narrative asset not found');
  }
  try {
    const body = await readFile(resolved);
    return new Response(body, {
      headers: { 'content-type': contentType(assetPath), 'cache-control': 'public, max-age=3600' },
    });
  } catch {
    throw error(404, 'Narrative asset not found');
  }
};
