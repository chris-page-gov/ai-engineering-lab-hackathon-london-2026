import { fireEvent, render, screen } from '@testing-library/svelte';
import { describe, expect, it, vi } from 'vitest';
import ContextBasket from './ContextBasket.svelte';
import EvidencePanel from './EvidencePanel.svelte';
import FilterPanel from './FilterPanel.svelte';
import ModePanel from './ModePanel.svelte';
import SourceCard from './SourceCard.svelte';
import type { WorkbenchCorpus, WorkbenchSource } from '$lib/workbench/types';
import { EMPTY_FILTERS } from '$lib/workbench/types';

const source: WorkbenchSource = {
  sourceId: 'DOC-HB-002',
  title: 'Discretionary Housing Payments',
  sourcePath: 'structured_files/DOC-HB-002.md',
  notePath: 'wiki/sources/doc-hb-002.md',
  format: 'md',
  documentType: 'guidance',
  department: 'DLUHC',
  status: 'current',
  version: null,
  publicationDate: null,
  lastUpdated: null,
  audience: [],
  topics: ['housing-benefit', 'discretionary-housing-payments'],
  entities: ['dluhc'],
  supersedes: [],
  relatedSources: [],
  flags: ['important'],
  dataOrigin: 'synthetic_fixture',
  syntheticDataNotice: 'Synthetic fixture',
  extractionMethod: 'markdown',
  extractionQuality: 'high',
  extractionWarnings: [],
  tableCount: 0,
  containsRealPersonalData: false,
  containsSyntheticIdentifiers: false,
  classification: null,
  sizeBytes: 100,
  sha256: 'abc',
  summary: 'A source summary about discretionary housing payments.',
  noteText:
    '## Summary\n\nA source summary about discretionary housing payments.\n\nMore evidence text for testing housing decisions, provenance, metadata, source links, and quoted policy material in the evidence panel.',
  searchText: 'doc-hb-002 discretionary housing payments',
};

const corpus: WorkbenchCorpus = {
  generatedAt: '2026-04-16T00:00:00Z',
  title: 'Dark Data Workbench',
  sourceCount: 1,
  syntheticData: true,
  syntheticDataNotice: 'Synthetic fixture',
  sources: [source],
  topics: [{ id: 'housing-benefit', label: 'Housing Benefit', count: 1 }],
  entities: [{ id: 'dluhc', label: 'DLUHC', count: 1 }],
  facets: [
    { id: 'departments', label: 'Department', values: [{ value: 'DLUHC', count: 1 }] },
    { id: 'statuses', label: 'Status', values: [{ value: 'current', count: 1 }] },
  ],
  stats: {
    formats: { md: 1 },
    statuses: { current: 1 },
    departments: { DLUHC: 1 },
    flaggedSources: 1,
    workbookSources: 0,
  },
};

describe('workbench components', () => {
  it('renders source cards and emits actions', async () => {
    const openSource = vi.fn();
    const selectSource = vi.fn();
    render(SourceCard, { source, selected: false, highlighted: false, openSource, selectSource });

    expect(screen.getByText('DOC-HB-002')).toBeInTheDocument();
    expect(screen.getByText('important')).toBeInTheDocument();

    await fireEvent.click(screen.getByRole('button', { name: 'Open' }));
    await fireEvent.click(screen.getByRole('button', { name: 'Add' }));

    expect(openSource).toHaveBeenCalledWith(source);
    expect(selectSource).toHaveBeenCalledWith(source);
  });

  it('renders filters and emits query and facet changes', async () => {
    const onToggleFilter = vi.fn();
    render(FilterPanel, {
      corpus,
      filters: EMPTY_FILTERS,
      query: '',
      toggleFilter: onToggleFilter,
      clearFilters: vi.fn(),
    });

    const search = screen.getByRole('searchbox') as HTMLInputElement;
    await fireEvent.input(search, { target: { value: 'housing' } });
    await fireEvent.click(screen.getByRole('button', { name: /DLUHC 1/i }));

    expect(search.value).toBe('housing');
    expect(onToggleFilter).toHaveBeenCalledWith('departments', 'DLUHC');
  });

  it('renders context basket save controls', async () => {
    const onSave = vi.fn();
    const onNameChange = vi.fn();
    render(ContextBasket, {
      sources: [source],
      savedContexts: [{ name: 'Housing', sourceIds: ['DOC-HB-002'] }],
      contextName: '',
      changeName: onNameChange,
      saveCurrentContext: onSave,
    });

    await fireEvent.input(screen.getByLabelText('Context name'), { target: { value: 'DHP' } });
    expect(onNameChange).toHaveBeenCalledWith('DHP');
    expect(screen.getByText('Housing (1)')).toBeInTheDocument();
  });

  it('renders mode panel browser AI actions and MCP tools', async () => {
    const onCopyJson = vi.fn();
    const { rerender } = render(ModePanel, {
      mode: 'browser-ai',
      sourceCount: 1,
      copyJson: onCopyJson,
    });

    await fireEvent.click(screen.getByRole('button', { name: 'Copy JSON' }));
    expect(onCopyJson).toHaveBeenCalled();

    await rerender({ mode: 'mcp', sourceCount: 1 });
    expect(screen.getByText('workbench.search_sources')).toBeInTheDocument();
  });

  it('renders evidence metadata and excerpts', () => {
    render(EvidencePanel, { source, query: 'housing' });

    expect(screen.getByText('DOC-HB-002')).toBeInTheDocument();
    expect(screen.getByText('structured_files/DOC-HB-002.md')).toBeInTheDocument();
    expect(screen.getByText(/More evidence text/)).toBeInTheDocument();
  });
});
