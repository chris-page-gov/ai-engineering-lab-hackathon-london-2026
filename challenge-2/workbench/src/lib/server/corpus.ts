import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import type { SourceRegisterEntry } from '$lib/workbench/types';
import { createCorpus } from '$lib/workbench/model';

export const defaultChallengeRoot = () => resolve(process.cwd(), '..');

export const loadCorpusFromDisk = async (challengeRoot = defaultChallengeRoot()) => {
  const registerPath = resolve(challengeRoot, 'wiki/data/source-register.json');
  const register = JSON.parse(await readFile(registerPath, 'utf-8')) as SourceRegisterEntry[];
  const noteTexts: Record<string, string> = {};
  await Promise.all(
    register.map(async (entry) => {
      try {
        noteTexts[entry.note_path] = await readFile(resolve(challengeRoot, entry.note_path), 'utf-8');
      } catch {
        noteTexts[entry.note_path] = '';
      }
    })
  );
  return createCorpus(register, noteTexts);
};
