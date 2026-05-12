import { readFile } from 'node:fs/promises';
import { relative, resolve } from 'node:path';
import type { SourceRegisterEntry, WorkbenchCorpus, WorkbenchLink, WorkbenchSource } from '$lib/workbench/types';
import { countValues, createCorpus, extractSummary, toFacetValues } from '$lib/workbench/model';

export const defaultChallengeRoot = () => resolve(process.cwd(), '..');

type NarrativePackItem = {
  id: string;
  name: string;
  short_name?: string;
  icon?: string;
  image?: string;
  images?: string[];
  category_path?: string;
  tile_subtitle?: string;
  info_text?: string;
  properties?: Record<string, unknown>;
  links?: WorkbenchLink[];
};

type NarrativePackCollection = {
  id: string;
  name: string;
  item_ids?: string[];
  sourceIds?: string[];
};

type NarrativePack = {
  meta?: { id?: string; title?: string; packKind?: string; version?: string };
  items: NarrativePackItem[];
  collections?: NarrativePackCollection[];
};

const asStringArray = (value: unknown) => {
  if (Array.isArray(value)) return value.map((entry) => String(entry).trim()).filter(Boolean);
  if (value === null || value === undefined || value === '') return [];
  return [String(value).trim()].filter(Boolean);
};

const firstString = (value: unknown, fallback: string) => asStringArray(value)[0] ?? fallback;

const numberOrNull = (value: unknown) => {
  const number = Number(value);
  return Number.isFinite(number) ? number : null;
};

export const defaultRepoRoot = (challengeRoot = defaultChallengeRoot()) => resolve(challengeRoot, '..');

const loadChallengeCorpusFromDisk = async (challengeRoot = defaultChallengeRoot()) => {
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

export const narrativePackPath = (repoRoot = defaultRepoRoot()) =>
  resolve(repoRoot, 'research/hmrc-beyond-hype/narrative/seelinks/pack.json');

const loadNarrativeCorpusFromDisk = async (repoRoot = defaultRepoRoot()): Promise<WorkbenchCorpus> => {
  const pack = JSON.parse(await readFile(narrativePackPath(repoRoot), 'utf-8')) as NarrativePack;
  const sources: WorkbenchSource[] = await Promise.all(
    pack.items.map(async (item) => {
      const props = item.properties ?? {};
      const repoPath = firstString(props.repo_path, '');
      let noteText = '';
      if (repoPath) {
        try {
          noteText = await readFile(resolve(repoRoot, repoPath), 'utf-8');
        } catch {
          noteText = item.info_text ?? '';
        }
      } else {
        noteText = item.info_text ?? '';
      }
      const sourceFamilies = asStringArray(props.source_family);
      const stages = asStringArray(props.narrative_stage);
      const assetTypes = asStringArray(props.asset_type);
      const evidenceRoles = asStringArray(props.evidence_role);
      const governanceThemes = asStringArray(props.governance_theme);
      const talkSections = asStringArray(props.talk_section);
      const provenanceModes = asStringArray(props.provenance_mode);
      const topicGroups = asStringArray(props.topic_group);
      const topics = asStringArray(props.tags);
      const screenfulls = numberOrNull(props.screenfulls);
      const source: WorkbenchSource = {
        sourceId: item.id,
        title: item.name,
        sourcePath: firstString(props.source_path, repoPath),
        notePath: repoPath,
        format: firstString(props.asset_type, 'narrative'),
        documentType: firstString(props.evidence_role, 'narrative'),
        department: firstString(props.source_family, 'HMRC narrative'),
        status: firstString(props.provenance_mode, 'tracked'),
        version: null,
        publicationDate: null,
        lastUpdated: null,
        audience: ['HMRC Data Science Academy', 'Public-sector engineering teams'],
        topics,
        entities: [...sourceFamilies, ...governanceThemes, ...topicGroups],
        supersedes: [],
        relatedSources: [],
        flags: governanceThemes.filter((theme) => /risk|security|data handling/i.test(theme)),
        dataOrigin: firstString(props.provenance_mode, 'narrative_pack'),
        syntheticDataNotice:
          'HMRC talk narrative material is generated or imported preparation evidence. Recheck live product and policy claims before presenting.',
        extractionMethod: 'narrative-seelinks-pack',
        extractionQuality: 'curated',
        extractionWarnings: [],
        tableCount: 0,
        containsRealPersonalData: false,
        containsSyntheticIdentifiers: false,
        classification: null,
        sizeBytes: null,
        sha256: null,
        summary: item.info_text || extractSummary(noteText, item.name),
        noteText,
        searchText: '',
        categoryPath: item.category_path ?? null,
        tileSubtitle: item.tile_subtitle ?? null,
        properties: props,
        gallery: [...asStringArray(item.images), ...asStringArray(props.gallery)],
        thumbnailPath: item.image ?? item.icon ?? null,
        sourceFamilies,
        stages,
        assetTypes,
        evidenceRoles,
        governanceThemes,
        talkSections,
        provenanceModes,
        topicGroups,
        screenfulls,
        links: item.links ?? [],
      };
      source.searchText = [
        source.sourceId,
        source.title,
        source.summary,
        source.sourcePath,
        source.notePath,
        source.format,
        source.documentType,
        source.department,
        source.status,
        ...source.topics,
        ...source.entities,
        ...source.flags,
        ...sourceFamilies,
        ...stages,
        ...assetTypes,
        ...evidenceRoles,
        ...governanceThemes,
        ...talkSections,
        ...provenanceModes,
        ...topicGroups,
        source.screenfulls ? String(source.screenfulls) : '',
        source.noteText,
      ]
        .join(' ')
        .toLowerCase();
      return source;
    })
  );

  const topicCounts = countValues(sources.flatMap((source) => source.topics));
  const entityCounts = countValues(sources.flatMap((source) => source.entities));
  const stats = {
    formats: countValues(sources.map((source) => source.format)),
    statuses: countValues(sources.map((source) => source.status)),
    departments: countValues(sources.map((source) => source.department)),
    flaggedSources: sources.filter((source) => source.flags.length > 0).length,
    workbookSources: 0,
  };
  return {
    generatedAt: new Date().toISOString(),
    title: pack.meta?.title ?? 'HMRC Narrative Arc Workbench',
    packId: pack.meta?.id ?? 'hmrc-narrative',
    packKind: pack.meta?.packKind ?? 'hmrc-narrative',
    version: pack.meta?.version ?? '1.0.0',
    packMeta: pack.meta ?? {},
    sourceCount: sources.length,
    syntheticData: false,
    syntheticDataNotice:
      'HMRC talk narrative material is generated or imported preparation evidence. Recheck live product and policy claims before presenting.',
    sources,
    topics: Object.entries(topicCounts).map(([id, count]) => ({ id, label: id, count })),
    entities: Object.entries(entityCounts).map(([id, count]) => ({ id, label: id, count })),
    facets: [
      { id: 'sourceFamilies', label: 'Source Family', values: toFacetValues(countValues(sources.flatMap((source) => source.sourceFamilies ?? []))) },
      { id: 'stages', label: 'Narrative Stage', values: toFacetValues(countValues(sources.flatMap((source) => source.stages ?? []))) },
      { id: 'talkSections', label: 'Talk Section', values: toFacetValues(countValues(sources.flatMap((source) => source.talkSections ?? []))) },
      { id: 'assetTypes', label: 'Asset Type', values: toFacetValues(countValues(sources.flatMap((source) => source.assetTypes ?? []))) },
      { id: 'evidenceRoles', label: 'Evidence Role', values: toFacetValues(countValues(sources.flatMap((source) => source.evidenceRoles ?? []))) },
      { id: 'governanceThemes', label: 'Governance Theme', values: toFacetValues(countValues(sources.flatMap((source) => source.governanceThemes ?? []))) },
      { id: 'topicGroups', label: 'Topic Group', values: toFacetValues(countValues(sources.flatMap((source) => source.topicGroups ?? []))), metadata: true },
      { id: 'provenanceModes', label: 'Provenance Mode', values: toFacetValues(countValues(sources.flatMap((source) => source.provenanceModes ?? []))), metadata: true },
      {
        id: 'screenfulls',
        label: 'Screenfulls',
        kind: 'measure',
        metadata: true,
        values: toFacetValues(countValues(sources.flatMap((source) => (source.screenfulls ? [String(source.screenfulls)] : [])))),
      },
      { id: 'topics', label: 'Tag', values: toFacetValues(topicCounts), metadata: true },
    ],
    collections: (pack.collections ?? []).map((collection) => ({
      id: collection.id,
      name: collection.name,
      sourceIds: collection.sourceIds ?? collection.item_ids ?? [],
      createdAt: new Date().toISOString(),
    })),
    graph: {
      nodes: [
        ...Object.entries(topicCounts).map(([id, count]) => ({ id, label: id, kind: 'topic', count })),
        ...sources.map((source) => ({ id: source.sourceId, label: source.title, kind: 'source' })),
      ],
      edges: sources.flatMap((source) =>
        source.topics.map((topic) => ({ source: topic, target: source.sourceId, kind: 'topic-source', count: 1 }))
      ),
    },
    stats,
  };
};

export const loadCorpusFromDisk = async (challengeRoot = defaultChallengeRoot(), packId = 'challenge-2') => {
  if (packId === 'hmrc-narrative') {
    return loadNarrativeCorpusFromDisk(defaultRepoRoot(challengeRoot));
  }
  return loadChallengeCorpusFromDisk(challengeRoot);
};

export const loadAllCorporaFromDisk = async (challengeRoot = defaultChallengeRoot()) =>
  Promise.all([loadChallengeCorpusFromDisk(challengeRoot), loadNarrativeCorpusFromDisk(defaultRepoRoot(challengeRoot))]);

export const narrativeAssetEntries = async (repoRoot = defaultRepoRoot()) => {
  const pack = JSON.parse(await readFile(narrativePackPath(repoRoot), 'utf-8')) as NarrativePack;
  const paths = new Set(['assets/note-card.svg']);
  for (const item of pack.items) {
    const image = item.image ?? item.icon;
    if (image?.startsWith('/api/narrative-asset/')) {
      paths.add(image.replace('/api/narrative-asset/', ''));
    }
  }
  return Array.from(paths).map((path) => ({ path }));
};

export const narrativeAssetPath = (assetPath: string, repoRoot = defaultRepoRoot()) => {
  if (assetPath === 'assets/note-card.svg') return null;
  if (!assetPath.startsWith('assets/')) {
    throw new Error('Narrative asset path must stay inside the narrative assets folder.');
  }
  const assetRoot = resolve(repoRoot, 'research/hmrc-beyond-hype/narrative/assets');
  const resolved = resolve(repoRoot, 'research/hmrc-beyond-hype/narrative', assetPath);
  const relativeToRoot = relative(assetRoot, resolved);
  if (!relativeToRoot || relativeToRoot.startsWith('..') || relativeToRoot.startsWith('/')) {
    throw new Error('Narrative asset path must stay inside the narrative assets folder.');
  }
  return resolved;
};
