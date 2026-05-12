import type {
  ContextExport,
  ContextExportSource,
  FilterState,
  SavedQuery,
  SourceRegisterEntry,
  WorkbenchCorpus,
  WorkbenchSource,
} from './types';
import { EMPTY_FILTERS } from './types';

export const SYNTHETIC_DATA_NOTICE =
  'Challenge 2 corpus data is synthetic hackathon fixture data. Synthetic names and contact-like values are retained for demo fidelity and should not be redacted.';

export const SAVED_QUERIES: SavedQuery[] = [
  {
    id: 'current-council-tax-reduction',
    label: 'Current CTR guidance',
    question: 'Which Council Tax Reduction guidance is current?',
    rationale: 'Find current Council Tax Reduction sources while excluding stale/conflicted records.',
  },
  {
    id: 'self-employed-housing-benefit',
    label: 'Self-employed HB',
    question: 'Can a self-employed person claim Housing Benefit?',
    rationale: 'Collect Housing Benefit and self-employment guidance needed to answer the eligibility question.',
  },
  {
    id: 'staff-policy-risks',
    label: 'Staff policy risks',
    question: 'Which staff policies are draft, stale, or past review?',
    rationale: 'Surface people-policy records with review, draft, stale, or supersession risk flags.',
  },
  {
    id: 'it-hardware-5000',
    label: 'IT hardware over GBP 5,000',
    question: 'What approvals are needed for IT hardware over GBP 5,000?',
    rationale: 'Collect procurement threshold and spending-control sources that mention IT hardware approvals.',
  },
  {
    id: 'dhp-mentions',
    label: 'DHP mentions',
    question: 'Which documents mention Discretionary Housing Payments?',
    rationale: 'Search topics and extracted note text for Discretionary Housing Payments and DHP references.',
  },
];

const humanize = (value: string) =>
  value
    .split(/[-_]/)
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');

const uniqueSorted = (values: Array<string | null | undefined>) =>
  Array.from(new Set(values.map((value) => String(value ?? '').trim()).filter(Boolean))).sort((a, b) =>
    a.localeCompare(b)
  );

const firstText = (value: unknown, fallback: string) => {
  const text = String(value ?? '').trim();
  return text || fallback;
};

const stripFrontmatter = (text: string) => text.replace(/^---[\s\S]*?---\s*/, '');

export const extractSummary = (noteText: string, fallback: string) => {
  const body = stripFrontmatter(noteText);
  const summaryMatch = body.match(/## Summary\s+([\s\S]*?)(?:\n## |\n# |\s*$)/i);
  const raw = summaryMatch?.[1] ?? body;
  const lines = raw
    .split('\n')
    .map((line) => line.replace(/^[-*]\s*/, '').trim())
    .filter((line) => line && !line.startsWith('|') && !line.startsWith('---'));
  const summary = lines.join(' ').replace(/\s+/g, ' ').trim();
  return summary.slice(0, 700) || fallback;
};

export const extractExcerpts = (source: WorkbenchSource, query = '', max = 3) => {
  const body = stripFrontmatter(source.noteText);
  const paragraphs = body
    .split(/\n{2,}/)
    .map((paragraph) => paragraph.replace(/\s+/g, ' ').trim())
    .filter((paragraph) => paragraph.length > 80 && !paragraph.startsWith('|'));
  const needle = query.trim().toLowerCase();
  const matches = needle
    ? paragraphs.filter((paragraph) => paragraph.toLowerCase().includes(needle))
    : paragraphs.filter((paragraph) => /source:|extract:|eligib|approval|payment|policy|review/i.test(paragraph));
  const selected = (matches.length ? matches : paragraphs).slice(0, max);
  return selected.map((excerpt) => (excerpt.length > 1200 ? `${excerpt.slice(0, 1197)}...` : excerpt));
};

export const createCorpus = (
  register: SourceRegisterEntry[],
  noteTexts: Record<string, string>,
  generatedAt = new Date().toISOString()
): WorkbenchCorpus => {
  const sources = register.map((entry) => {
    const topics = uniqueSorted([...(entry.topics ?? []), ...(entry.matched_topics ?? [])]);
    const entities = uniqueSorted(entry.matched_entities ?? []);
    const noteText = noteTexts[entry.note_path] ?? '';
    const source: WorkbenchSource = {
      sourceId: entry.source_id,
      title: entry.title,
      sourcePath: entry.source_path,
      notePath: entry.note_path,
      format: firstText(entry.source_format, 'unknown'),
      documentType: firstText(entry.document_type, 'unknown'),
      department: firstText(entry.department, 'Unknown'),
      status: firstText(entry.status, 'unknown'),
      version: entry.version ?? null,
      publicationDate: entry.publication_date ?? null,
      lastUpdated: entry.last_updated ?? null,
      audience: uniqueSorted(entry.audience ?? []),
      topics,
      entities,
      supersedes: uniqueSorted(entry.supersedes ?? []),
      relatedSources: uniqueSorted(entry.related_sources ?? []),
      flags: uniqueSorted(entry.flags ?? []),
      dataOrigin: firstText(entry.data_origin, 'synthetic_fixture'),
      syntheticDataNotice: firstText(entry.synthetic_data_notice, SYNTHETIC_DATA_NOTICE),
      extractionMethod: firstText(entry.extraction?.method, 'unknown'),
      extractionQuality: firstText(entry.extraction?.quality, 'unknown'),
      extractionWarnings: uniqueSorted(entry.extraction?.warnings ?? []),
      tableCount: Number(entry.extraction?.table_count ?? 0),
      containsRealPersonalData: Boolean(entry.sensitivity?.contains_real_personal_data),
      containsSyntheticIdentifiers: Boolean(entry.sensitivity?.contains_synthetic_identifiers),
      classification: entry.sensitivity?.classification ?? null,
      sizeBytes: typeof entry.technical_metadata?.size_bytes === 'number' ? entry.technical_metadata.size_bytes : null,
      sha256: entry.technical_metadata?.sha256 ?? null,
      summary: '',
      noteText,
      searchText: '',
    };
    source.summary = extractSummary(noteText, entry.title);
    source.searchText = [
      source.sourceId,
      source.title,
      source.department,
      source.status,
      source.format,
      source.documentType,
      ...source.topics,
      ...source.entities,
      ...source.flags,
      source.noteText,
    ]
      .join(' ')
      .toLowerCase();
    return source;
  });

  const stats = {
    formats: countValues(sources.map((source) => source.format)),
    statuses: countValues(sources.map((source) => source.status)),
    departments: countValues(sources.map((source) => source.department)),
    flaggedSources: sources.filter((source) => source.flags.length || source.status === 'draft' || source.status === 'superseded')
      .length,
    workbookSources: sources.filter((source) => source.format === 'xlsx').length,
  };

  const topicCounts = countValues(sources.flatMap((source) => source.topics));
  const entityCounts = countValues(sources.flatMap((source) => source.entities));

  return {
    generatedAt,
    title: 'Dark Data Workbench',
    sourceCount: sources.length,
    syntheticData: true,
    syntheticDataNotice: SYNTHETIC_DATA_NOTICE,
    sources,
    topics: Object.entries(topicCounts).map(([id, count]) => ({ id, label: humanize(id), count })),
    entities: Object.entries(entityCounts).map(([id, count]) => ({ id, label: humanize(id), count })),
    facets: [
      { id: 'departments', label: 'Department', values: toFacetValues(stats.departments) },
      { id: 'statuses', label: 'Status', values: toFacetValues(stats.statuses) },
      { id: 'formats', label: 'Format', values: toFacetValues(stats.formats) },
      { id: 'topics', label: 'Topic', values: toFacetValues(topicCounts) },
      { id: 'flags', label: 'Flag', values: toFacetValues(countValues(sources.flatMap((source) => source.flags))) },
    ],
    stats,
  };
};

export const countValues = (values: string[]) =>
  values.reduce<Record<string, number>>((acc, value) => {
    const key = value.trim() || 'Unknown';
    acc[key] = (acc[key] ?? 0) + 1;
    return acc;
  }, {});

export const toFacetValues = (counts: Record<string, number>) =>
  Object.entries(counts)
    .map(([value, count]) => ({ value, count }))
    .sort((a, b) => b.count - a.count || a.value.localeCompare(b.value));

const intersects = (selected: string[], values: string[]) => selected.length === 0 || values.some((value) => selected.includes(value));

export const filterSources = (sources: WorkbenchSource[], filters: FilterState = EMPTY_FILTERS, query = '') => {
  const search = query.trim().toLowerCase();
  const exactSourceIdSearch = /^(doc|uf)-[a-z0-9-]+$/i.test(query.trim());
  return sources.filter((source) => {
    if (search && exactSourceIdSearch && source.sourceId.toLowerCase() !== search) return false;
    if (search && !exactSourceIdSearch && !source.searchText.includes(search)) return false;
    if (!intersects(filters.departments, [source.department])) return false;
    if (!intersects(filters.statuses, [source.status])) return false;
    if (!intersects(filters.formats, [source.format])) return false;
    if (!intersects(filters.topics, source.topics)) return false;
    if (!intersects(filters.flags, source.flags)) return false;
    if (!intersects(filters.sourceFamilies, source.sourceFamilies ?? [])) return false;
    if (!intersects(filters.stages, source.stages ?? [])) return false;
    if (!intersects(filters.assetTypes, source.assetTypes ?? [])) return false;
    if (!intersects(filters.evidenceRoles, source.evidenceRoles ?? [])) return false;
    if (!intersects(filters.governanceThemes, source.governanceThemes ?? [])) return false;
    if (!intersects(filters.talkSections, source.talkSections ?? [])) return false;
    if (!intersects(filters.provenanceModes, source.provenanceModes ?? [])) return false;
    if (!intersects(filters.topicGroups, source.topicGroups ?? [])) return false;
    if (!intersects(filters.screenfulls, source.screenfulls ? [String(source.screenfulls)] : [])) return false;
    return true;
  });
};

export const toggleFilterValue = (filters: FilterState, key: keyof FilterState, value: string): FilterState => {
  const current = new Set(filters[key]);
  if (current.has(value)) {
    current.delete(value);
  } else {
    current.add(value);
  }
  return { ...filters, [key]: Array.from(current).sort((a, b) => a.localeCompare(b)) };
};

export const runSavedQuery = (corpus: WorkbenchCorpus, queryId: string) => {
  const sources = corpus.sources;
  if (queryId === 'current-council-tax-reduction') {
    return sources.filter(
      (source) =>
        source.topics.includes('council-tax-reduction') &&
        source.status === 'current' &&
        !source.flags.some((flag) => /stale|conflict|superseded/i.test(flag))
    );
  }
  if (queryId === 'self-employed-housing-benefit') {
    const wanted = new Set(['DOC-SB-006', 'DOC-HB-001', 'DOC-SB-002']);
    return sources.filter((source) => wanted.has(source.sourceId));
  }
  if (queryId === 'staff-policy-risks') {
    return sources.filter((source) => {
      const riskText = [source.status, ...source.flags, source.title].join(' ');
      return /draft|stale|superseded|past review|review/i.test(riskText) && /policy|staff|people|security|travel/i.test(source.searchText);
    });
  }
  if (queryId === 'it-hardware-5000') {
    return sources.filter(
      (source) =>
        source.sourceId === 'UF-SPENDING-CONTROLS-GUIDANCE' ||
        source.sourceId === 'UF-PROCUREMENT-THRESHOLDS-2024-25' ||
        (/it hardware/i.test(source.noteText) && /5,?000|GBP 5,?000|£5,?000/i.test(source.noteText))
    );
  }
  if (queryId === 'dhp-mentions') {
    return sources.filter(
      (source) =>
        source.topics.includes('discretionary-housing-payments') ||
        /Discretionary Housing Payments|\bDHPs?\b/i.test(source.noteText)
    );
  }
  return [];
};

export const buildContextExport = ({
  corpus,
  visibleSources,
  selectedIds,
  highlightedIds,
  filters,
  question,
  query,
  mode,
}: {
  corpus: WorkbenchCorpus;
  visibleSources: WorkbenchSource[];
  selectedIds: Set<string>;
  highlightedIds: Set<string>;
  filters: FilterState;
  question?: string;
  query: string;
  mode: ContextExport['mode'];
}): ContextExport => {
  const contextSources = selectedIds.size
    ? corpus.sources.filter((source) => selectedIds.has(source.sourceId))
    : visibleSources;
  return {
    exported_at: new Date().toISOString(),
    mode,
    corpus: {
      title: corpus.title,
      source_count: corpus.sourceCount,
      synthetic_data: corpus.syntheticData,
      synthetic_data_notice: corpus.syntheticDataNotice,
    },
    view: {
      question: question?.trim() ?? '',
      query,
      filters,
      selected_source_ids: Array.from(selectedIds).sort((a, b) => a.localeCompare(b)),
      highlighted_source_ids: Array.from(highlightedIds).sort((a, b) => a.localeCompare(b)),
      total_in_view: visibleSources.length,
      total_in_corpus: corpus.sourceCount,
    },
    instructions: {
      answer_policy: 'Use only the supplied context. If the evidence is missing or ambiguous, say so.',
      citation_policy: 'Cite source_id for every factual claim.',
      synthetic_data_notice: SYNTHETIC_DATA_NOTICE,
    },
    sources: contextSources.map((source): ContextExportSource => ({
      source_id: source.sourceId,
      title: source.title,
      status: source.status,
      format: source.format,
      department: source.department,
      topics: source.topics,
      flags: source.flags,
      note_path: source.notePath,
      source_path: source.sourcePath,
      summary: source.summary,
      excerpts: extractExcerpts(source, query),
      selected: selectedIds.has(source.sourceId),
      highlighted: highlightedIds.has(source.sourceId),
      thumbnail_path: source.thumbnailPath ?? null,
      source_families: source.sourceFamilies ?? [],
      narrative_stages: source.stages ?? [],
      talk_sections: source.talkSections ?? [],
      evidence_roles: source.evidenceRoles ?? [],
      governance_themes: source.governanceThemes ?? [],
      links: source.links ?? [],
    })),
  };
};

export const buildBrowserPrompt = (context: ContextExport) => `You are answering questions about the ${context.corpus.title} context.

Rules:
- Use only the supplied context JSON.
- Cite source_id for every factual claim.
- If the context does not contain enough evidence, say what is missing.
${context.corpus.synthetic_data ? '- The corpus is synthetic hackathon fixture data. Do not redact synthetic names, emails, roles, or contact-like values.' : '- Treat imported claims as talk-preparation evidence, not as production assurance.'}

Question: ${context.view.question || 'Use the question supplied by the user alongside this prompt.'}

Current context contains ${context.sources.length} source(s): ${context.sources.map((source) => source.source_id).join(', ')}.`;

export const buildEvidenceMarkdown = (context: ContextExport) => {
  const lines = [
    `# ${context.corpus.title} Evidence Bundle`,
    '',
    `Exported: ${context.exported_at}`,
    `Sources: ${context.sources.length}`,
    `Question: ${context.view.question || 'Not specified'}`,
    '',
    '## Instructions',
    '',
    `- ${context.instructions.answer_policy}`,
    `- ${context.instructions.citation_policy}`,
    `- ${context.instructions.synthetic_data_notice}`,
    '',
    '## Sources',
    '',
  ];
  for (const source of context.sources) {
    lines.push(`### ${source.source_id}: ${source.title}`);
    lines.push('');
    lines.push(`- Status: ${source.status}`);
    lines.push(`- Format: ${source.format}`);
    lines.push(`- Department: ${source.department}`);
    lines.push(`- Note: ${source.note_path}`);
    lines.push(`- Raw source: ${source.source_path}`);
    if (source.flags.length) lines.push(`- Flags: ${source.flags.join(', ')}`);
    lines.push('');
    lines.push(source.summary);
    lines.push('');
    for (const excerpt of source.excerpts) {
      lines.push(`> ${excerpt}`);
      lines.push('');
    }
  }
  return lines.join('\n');
};

export const copyText = async (value: string) => {
  if (typeof navigator !== 'undefined' && navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(value);
    return true;
  }
  return false;
};
