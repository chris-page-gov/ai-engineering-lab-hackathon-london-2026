import { resolve } from 'node:path';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { loadCorpusFromDisk } from '$lib/server/corpus';
import {
  SYNTHETIC_DATA_NOTICE,
  buildBrowserPrompt,
  buildContextExport,
  buildEvidenceMarkdown,
  copyText,
  countValues,
  createCorpus,
  extractExcerpts,
  extractSummary,
  filterSources,
  runSavedQuery,
  toFacetValues,
  toggleFilterValue,
} from './model';
import { EMPTY_FILTERS, type SourceRegisterEntry } from './types';

const challengeRoot = resolve(process.cwd(), '..');

const registerEntry = (overrides: Partial<SourceRegisterEntry>): SourceRegisterEntry => ({
  source_id: 'DOC-TEST-001',
  title: 'Test Source',
  source_path: 'structured_files/test.md',
  note_path: 'wiki/sources/test.md',
  source_format: 'md',
  ...overrides,
});

afterEach(() => {
  vi.unstubAllGlobals();
});

describe('workbench corpus model', () => {
  it('loads and normalizes all Challenge 2 sources', async () => {
    const corpus = await loadCorpusFromDisk(challengeRoot);

    expect(corpus.sourceCount).toBe(43);
    expect(corpus.sources).toHaveLength(43);
    expect(corpus.syntheticData).toBe(true);
    expect(corpus.syntheticDataNotice).toContain('synthetic');
    expect(corpus.stats.workbookSources).toBe(3);
    expect(corpus.facets.find((facet) => facet.id === 'topics')?.values.length).toBeGreaterThan(5);
  });

  it('filters by search text and facets', async () => {
    const corpus = await loadCorpusFromDisk(challengeRoot);

    expect(filterSources(corpus.sources, EMPTY_FILTERS, 'DOC-HB-002')).toHaveLength(1);

    const filters = toggleFilterValue(EMPTY_FILTERS, 'formats', 'xlsx');
    const workbookSources = filterSources(corpus.sources, filters, '');

    expect(workbookSources).toHaveLength(3);
    expect(workbookSources.map((source) => source.sourceId)).toContain('UF-PROCUREMENT-THRESHOLDS-2024-25');

    const removed = toggleFilterValue(filters, 'formats', 'xlsx');
    expect(removed.formats).toEqual([]);
  });

  it('runs saved demo checks with expected evidence sources', async () => {
    const corpus = await loadCorpusFromDisk(challengeRoot);

    const councilTax = runSavedQuery(corpus, 'current-council-tax-reduction').map((source) => source.sourceId);
    expect(councilTax).toContain('DOC-HB-009');
    expect(councilTax).not.toContain('DOC-HB-003');

    const selfEmployed = runSavedQuery(corpus, 'self-employed-housing-benefit').map((source) => source.sourceId);
    expect(selfEmployed).toEqual(expect.arrayContaining(['DOC-SB-006', 'DOC-HB-001']));

    const procurement = runSavedQuery(corpus, 'it-hardware-5000').map((source) => source.sourceId);
    expect(procurement).toEqual(
      expect.arrayContaining(['UF-SPENDING-CONTROLS-GUIDANCE', 'UF-PROCUREMENT-THRESHOLDS-2024-25'])
    );

    const dhp = runSavedQuery(corpus, 'dhp-mentions');
    expect(dhp.length).toBeGreaterThan(1);
  });

  it('normalizes sparse source register entries and utility branches', () => {
    const corpus = createCorpus(
      [
        registerEntry({
          source_id: 'DOC-SPARSE-001',
          title: 'Sparse Policy',
          source_format: '',
          document_type: null,
          department: null,
          status: null,
          version: '1.0',
          publication_date: '2025-01-01',
          last_updated: '2025-02-01',
          audience: ['Officers', 'Officers'],
          topics: ['housing-benefit', 'housing-benefit'],
          matched_topics: ['discretionary-housing-payments'],
          matched_entities: ['dluhc'],
          supersedes: ['DOC-OLD'],
          related_sources: ['DOC-RELATED'],
          extraction: { method: '', quality: '', warnings: ['warning', 'warning'], table_count: 2 },
          sensitivity: { contains_synthetic_identifiers: true, classification: 'internal' },
          technical_metadata: { size_bytes: 12, sha256: 'hash' },
        }),
        registerEntry({
          source_id: 'UF-XLSX-001',
          title: 'Workbook',
          note_path: 'wiki/sources/workbook.md',
          source_format: 'xlsx',
          status: 'draft',
          flags: ['past-review'],
        }),
      ],
      {
        'wiki/sources/test.md': '---\nkey: value\n---\n## Summary\n- Useful summary\n| table | skipped |\n\n## Next\nBody',
        'wiki/sources/workbook.md': '',
      },
      '2026-04-16T00:00:00.000Z'
    );

    const sparse = corpus.sources.find((source) => source.sourceId === 'DOC-SPARSE-001');
    expect(sparse?.format).toBe('unknown');
    expect(sparse?.documentType).toBe('unknown');
    expect(sparse?.department).toBe('Unknown');
    expect(sparse?.status).toBe('unknown');
    expect(sparse?.summary).toBe('Useful summary');
    expect(sparse?.topics).toEqual(['discretionary-housing-payments', 'housing-benefit']);
    expect(sparse?.entities).toEqual(['dluhc']);
    expect(sparse?.extractionMethod).toBe('unknown');
    expect(sparse?.tableCount).toBe(2);
    expect(sparse?.containsSyntheticIdentifiers).toBe(true);
    expect(corpus.stats.flaggedSources).toBe(1);
    expect(corpus.stats.workbookSources).toBe(1);

    expect(extractSummary('---\nempty: true\n---\n| only | table |', 'Fallback')).toBe('Fallback');
    expect(countValues(['Alpha', 'Alpha', ''])).toEqual({ Alpha: 2, Unknown: 1 });
    expect(toFacetValues({ Beta: 1, Alpha: 1, Gamma: 3 }).map((facet) => facet.value)).toEqual(['Gamma', 'Alpha', 'Beta']);
  });

  it('filters out records across every facet branch', () => {
    const corpus = createCorpus(
      [
        registerEntry({
          source_id: 'DOC-FILTER-001',
          title: 'Filterable Source',
          source_format: 'md',
          department: 'DLUHC',
          status: 'current',
          topics: ['housing-benefit'],
          flags: ['stale-review'],
        }),
      ],
      {
        'wiki/sources/test.md':
          '## Summary\nA filterable source mentioning housing benefit policy, review evidence, and local authority decisions.',
      }
    );
    const sources = corpus.sources;

    expect(filterSources(sources, EMPTY_FILTERS, 'DOC-FILTER-001')).toHaveLength(1);
    expect(filterSources(sources, EMPTY_FILTERS, 'DOC-FILTER-MISSING')).toHaveLength(0);
    expect(filterSources(sources, EMPTY_FILTERS, 'not present')).toHaveLength(0);
    expect(filterSources(sources, { ...EMPTY_FILTERS, departments: ['Other'] }, '')).toHaveLength(0);
    expect(filterSources(sources, { ...EMPTY_FILTERS, statuses: ['draft'] }, '')).toHaveLength(0);
    expect(filterSources(sources, { ...EMPTY_FILTERS, formats: ['pdf'] }, '')).toHaveLength(0);
    expect(filterSources(sources, { ...EMPTY_FILTERS, topics: ['procurement'] }, '')).toHaveLength(0);
    expect(filterSources(sources, { ...EMPTY_FILTERS, flags: ['superseded'] }, '')).toHaveLength(0);
  });

  it('covers saved-query edge cases beyond the demo corpus', () => {
    const corpus = createCorpus(
      [
        registerEntry({
          source_id: 'DOC-CTR-STALE',
          title: 'Council Tax Reduction stale',
          topics: ['council-tax-reduction'],
          status: 'current',
          flags: ['stale-review'],
        }),
        registerEntry({
          source_id: 'DOC-STAFF-RISK',
          title: 'Travel Policy',
          status: 'draft',
          flags: ['past review'],
        }),
        registerEntry({
          source_id: 'DOC-IT-APPROVAL',
          title: 'IT Approval',
        }),
        registerEntry({
          source_id: 'DOC-DHP-TEXT',
          title: 'Payment Text',
        }),
      ],
      {
        'wiki/sources/test.md':
          '## Summary\nStaff policy review evidence. IT hardware requires approval above GBP 5,000. This note also mentions DHPs.',
      }
    );

    expect(runSavedQuery(corpus, 'current-council-tax-reduction')).toHaveLength(0);
    expect(runSavedQuery(corpus, 'staff-policy-risks').map((source) => source.sourceId)).toContain('DOC-STAFF-RISK');
    expect(runSavedQuery(corpus, 'it-hardware-5000').map((source) => source.sourceId)).toContain('DOC-IT-APPROVAL');
    expect(runSavedQuery(corpus, 'dhp-mentions').map((source) => source.sourceId)).toContain('DOC-DHP-TEXT');
    expect(runSavedQuery(corpus, 'unknown-query')).toEqual([]);
  });

  it('builds AI context exports and evidence bundles without redacting synthetic data', async () => {
    const corpus = await loadCorpusFromDisk(challengeRoot);
    const selectedIds = new Set(['UF-STAFF-DIRECTORY-EXTRACT-Q4-2023']);
    const visibleSources = corpus.sources.filter((source) => selectedIds.has(source.sourceId));
    const context = buildContextExport({
      corpus,
      visibleSources,
      selectedIds,
      highlightedIds: new Set(['UF-STAFF-DIRECTORY-EXTRACT-Q4-2023']),
      filters: EMPTY_FILTERS,
      question: 'Who is listed in the staff directory?',
      query: 'staff',
      mode: 'browser-ai',
    });

    expect(context.view.question).toBe('Who is listed in the staff directory?');
    expect(context.sources).toHaveLength(1);
    expect(context.instructions.synthetic_data_notice).toBe(SYNTHETIC_DATA_NOTICE);
    expect(JSON.stringify(context)).toContain('synthetic');
    expect(context.sources[0].selected).toBe(true);
    expect(context.sources[0].highlighted).toBe(true);

    const filteredContext = buildContextExport({
      corpus,
      visibleSources: corpus.sources.filter((source) => source.sourceId === 'DOC-HB-002'),
      selectedIds,
      highlightedIds: new Set(),
      filters: EMPTY_FILTERS,
      question: 'Who is listed in the staff directory?',
      query: 'staff',
      mode: 'browser-ai',
    });

    expect(filteredContext.view.total_in_view).toBe(1);
    expect(filteredContext.sources.map((source) => source.source_id)).toEqual(['UF-STAFF-DIRECTORY-EXTRACT-Q4-2023']);

    const prompt = buildBrowserPrompt(context);
    expect(prompt).toContain('Cite source_id');
    expect(prompt).toContain('Do not redact synthetic');
    expect(prompt).toContain('Who is listed in the staff directory?');

    const markdown = buildEvidenceMarkdown(context);
    expect(markdown).toContain('UF-STAFF-DIRECTORY-EXTRACT-Q4-2023');
    expect(markdown).toContain('Question: Who is listed in the staff directory?');
    expect(markdown).toContain('Synthetic');
  });

  it('exports all visible sources when no context is selected and handles clipboard availability', async () => {
    const corpus = createCorpus(
      [
        registerEntry({
          source_id: 'DOC-EXPORT-001',
          title: 'Export Source',
          flags: [],
        }),
      ],
      {
        'wiki/sources/test.md':
          '## Summary\nAn export source with enough evidence text to become an excerpt about policy evidence and provenance for the context bundle.',
      }
    );
    const context = buildContextExport({
      corpus,
      visibleSources: corpus.sources,
      selectedIds: new Set(),
      highlightedIds: new Set(),
      filters: EMPTY_FILTERS,
      question: '  ',
      query: '',
      mode: 'no-ai',
    });

    expect(context.sources).toHaveLength(1);
    expect(context.view.question).toBe('');
    expect(context.sources[0].selected).toBe(false);
    expect(buildEvidenceMarkdown(context)).not.toContain('Flags:');

    const writeText = vi.fn().mockResolvedValue(undefined);
    vi.stubGlobal('navigator', { clipboard: { writeText } });
    await expect(copyText('context')).resolves.toBe(true);
    expect(writeText).toHaveBeenCalledWith('context');

    vi.stubGlobal('navigator', {});
    await expect(copyText('context')).resolves.toBe(false);
  });

  it('extracts query excerpts, fallback excerpts, and long excerpts', () => {
    const corpus = createCorpus(
      [
        registerEntry({
          source_id: 'DOC-EXCERPT-001',
          title: 'Excerpt Source',
        }),
      ],
      {
        'wiki/sources/test.md': [
          '## Summary',
          'A short summary.',
          '',
          'This paragraph mentions procurement approval evidence and is deliberately long enough to be selected when no direct query is provided.',
          '',
          'This paragraph mentions a very specific retention keyword so query matching can select the right evidence paragraph.',
          '',
          `${'Long evidence '.repeat(120)}tail`,
        ].join('\n'),
      }
    );
    const source = corpus.sources[0];

    expect(extractExcerpts(source, 'retention keyword', 1)[0]).toContain('retention keyword');
    expect(extractExcerpts(source, 'missing keyword', 1)[0]).toContain('procurement approval');
    expect(extractExcerpts(source, 'Long evidence', 1)[0]).toHaveLength(1200);
    expect(extractExcerpts(source, 'Long evidence', 1)[0].endsWith('...')).toBe(true);
  });
});
