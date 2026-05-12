export type SourceRegisterEntry = {
  source_id: string;
  title: string;
  source_path: string;
  note_path: string;
  source_format: string;
  document_type?: string | null;
  department?: string | null;
  status?: string | null;
  version?: string | null;
  publication_date?: string | null;
  last_updated?: string | null;
  audience?: string[];
  topics?: string[];
  matched_topics?: string[];
  matched_entities?: string[];
  supersedes?: string[];
  related_sources?: string[];
  flags?: string[];
  data_origin?: string;
  synthetic_data_notice?: string;
  extraction?: {
    method?: string;
    quality?: string;
    warnings?: string[];
    table_count?: number;
    links?: unknown[];
  };
  sensitivity?: {
    contains_real_personal_data?: boolean;
    contains_synthetic_identifiers?: boolean;
    classification?: string | null;
  };
  technical_metadata?: {
    size_bytes?: number;
    sha256?: string;
  };
  raw_metadata?: Record<string, unknown>;
};

export type WorkbenchSource = {
  sourceId: string;
  title: string;
  sourcePath: string;
  notePath: string;
  format: string;
  documentType: string;
  department: string;
  status: string;
  version: string | null;
  publicationDate: string | null;
  lastUpdated: string | null;
  audience: string[];
  topics: string[];
  entities: string[];
  supersedes: string[];
  relatedSources: string[];
  flags: string[];
  dataOrigin: string;
  syntheticDataNotice: string;
  extractionMethod: string;
  extractionQuality: string;
  extractionWarnings: string[];
  tableCount: number;
  containsRealPersonalData: boolean;
  containsSyntheticIdentifiers: boolean;
  classification: string | null;
  sizeBytes: number | null;
  sha256: string | null;
  summary: string;
  noteText: string;
  searchText: string;
  categoryPath?: string | null;
  tileSubtitle?: string | null;
  properties?: Record<string, unknown>;
  gallery?: string[];
  thumbnailPath?: string | null;
  sourceFamilies?: string[];
  stages?: string[];
  assetTypes?: string[];
  evidenceRoles?: string[];
  governanceThemes?: string[];
  talkSections?: string[];
  provenanceModes?: string[];
  topicGroups?: string[];
  screenfulls?: number | null;
  links?: WorkbenchLink[];
};

export type WorkbenchFacet = {
  id: keyof FilterState;
  label: string;
  values: Array<{ value: string; count: number }>;
  kind?: 'category' | 'measure';
  metadata?: boolean;
};

export type WorkbenchCollection = {
  id: string;
  name: string;
  sourceIds: string[];
  createdAt: string;
};

export type WorkbenchGraph = {
  nodes: Array<{ id: string; label: string; kind: string; count?: number }>;
  edges: Array<{ source: string; target: string; kind: string; count?: number }>;
};

export type WorkbenchCorpus = {
  generatedAt: string;
  title: string;
  packId?: string;
  packKind?: string;
  version?: string;
  packMeta?: Record<string, unknown>;
  sourceCount: number;
  syntheticData: boolean;
  syntheticDataNotice: string;
  sources: WorkbenchSource[];
  topics: Array<{ id: string; label: string; count: number }>;
  entities: Array<{ id: string; label: string; count: number }>;
  facets: WorkbenchFacet[];
  collections?: WorkbenchCollection[];
  graph?: WorkbenchGraph;
  stats: {
    formats: Record<string, number>;
    statuses: Record<string, number>;
    departments: Record<string, number>;
    flaggedSources: number;
    workbookSources: number;
  };
};

export type FilterState = {
  departments: string[];
  statuses: string[];
  formats: string[];
  topics: string[];
  flags: string[];
  sourceFamilies: string[];
  stages: string[];
  assetTypes: string[];
  evidenceRoles: string[];
  governanceThemes: string[];
  talkSections: string[];
  provenanceModes: string[];
  topicGroups: string[];
  screenfulls: string[];
};

export type WorkbenchLink = {
  label: string;
  href: string;
  kind?: string;
};

export type SavedQuery = {
  id: string;
  label: string;
  question: string;
  rationale: string;
};

export type ContextExportSource = {
  source_id: string;
  title: string;
  status: string;
  format: string;
  department: string;
  topics: string[];
  flags: string[];
  note_path: string;
  source_path: string;
  summary: string;
  excerpts: string[];
  selected: boolean;
  highlighted: boolean;
  thumbnail_path?: string | null;
  source_families?: string[];
  narrative_stages?: string[];
  talk_sections?: string[];
  evidence_roles?: string[];
  governance_themes?: string[];
  links?: WorkbenchLink[];
};

export type ContextExport = {
  exported_at: string;
  mode: 'browser-ai' | 'mcp' | 'no-ai';
  corpus: {
    title: string;
    source_count: number;
    synthetic_data: boolean;
    synthetic_data_notice: string;
  };
  view: {
    question: string;
    query: string;
    filters: FilterState;
    selected_source_ids: string[];
    highlighted_source_ids: string[];
    view_reduction?: string;
    sort_by?: string[];
    active_collection?: string | null;
    highlight_filters?: Record<string, string[]>;
    total_in_view: number;
    total_in_corpus: number;
  };
  instructions: {
    answer_policy: string;
    citation_policy: string;
    synthetic_data_notice: string;
  };
  sources: ContextExportSource[];
};

export const EMPTY_FILTERS: FilterState = {
  departments: [],
  statuses: [],
  formats: [],
  topics: [],
  flags: [],
  sourceFamilies: [],
  stages: [],
  assetTypes: [],
  evidenceRoles: [],
  governanceThemes: [],
  talkSections: [],
  provenanceModes: [],
  topicGroups: [],
  screenfulls: [],
};
