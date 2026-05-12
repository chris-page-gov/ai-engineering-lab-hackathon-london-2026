import { describe, expect, it } from 'vitest';
import {
  applyFacetHighlights,
  buildLinkSummary,
  buildRollupSummaries,
  fieldDisplayValue,
  sortSourcesByFacets,
  type FacetValueOrders,
} from './seelinks';
import type { WorkbenchFacet, WorkbenchSource } from './types';

const source = (id: string, overrides: Partial<WorkbenchSource>): WorkbenchSource => ({
  sourceId: id,
  title: id,
  sourcePath: `${id}.md`,
  notePath: `${id}.md`,
  format: 'md',
  documentType: 'note',
  department: 'Unknown',
  status: 'current',
  version: null,
  publicationDate: null,
  lastUpdated: null,
  audience: [],
  topics: [],
  entities: [],
  supersedes: [],
  relatedSources: [],
  flags: [],
  dataOrigin: 'test',
  syntheticDataNotice: 'test',
  extractionMethod: 'test',
  extractionQuality: 'test',
  extractionWarnings: [],
  tableCount: 0,
  containsRealPersonalData: false,
  containsSyntheticIdentifiers: false,
  classification: null,
  sizeBytes: null,
  sha256: null,
  summary: '',
  noteText: '',
  searchText: '',
  ...overrides,
});

const facets: WorkbenchFacet[] = [
  {
    id: 'sourceFamilies',
    label: 'Source Family',
    values: [],
  },
  {
    id: 'talkSections',
    label: 'Talk Section',
    values: [],
  },
];

describe('SeeLinks-style workbench helpers', () => {
  const sources = [
    source('a', { title: 'A', sourceFamilies: ['Slides'], talkSections: ['Demo'], tileSubtitle: 'Slides | Demo' }),
    source('b', { title: 'B', sourceFamilies: ['Notes'], talkSections: ['Evidence'] }),
    source('c', { title: 'C', sourceFamilies: ['Slides'], talkSections: ['Evidence'] }),
  ];

  it('sorts sources by a multi-facet order stack', () => {
    const orders: FacetValueOrders = {
      sourceFamilies: ['Slides', 'Notes'],
      talkSections: ['Evidence', 'Demo'],
    };

    const sorted = sortSourcesByFacets(sources, ['sourceFamilies', 'talkSections'], orders);

    expect(sorted.map((entry) => entry.sourceId)).toEqual(['c', 'a', 'b']);
  });

  it('filters highlight sets across facets and builds rollups', () => {
    const highlighted = applyFacetHighlights(sources, {
      sourceFamilies: ['Slides'],
      talkSections: ['Evidence'],
    });
    const rollups = buildRollupSummaries(sources, [{ facet: 'talkSections', value: 'Evidence' }]);

    expect(highlighted.map((entry) => entry.sourceId)).toEqual(['c']);
    expect(rollups[0]).toMatchObject({ count: 2, total: 3, sourceIds: ['b', 'c'] });
  });

  it('summarises linkable facet values and tile text fields', () => {
    const summary = buildLinkSummary(sources, facets);

    expect(summary[0].facet.label).toBe('Source Family');
    expect(summary[0].values[0]).toEqual({ value: 'Slides', count: 2 });
    expect(fieldDisplayValue(sources[0], 'tileSubtitle')).toBe('Slides | Demo');
  });
});
