<script lang="ts">
  import { onMount } from 'svelte';
  import { loadCollections, saveCollection as persistCollection } from '$lib/workbench/collections';
  import ContextBasket from '$lib/components/ContextBasket.svelte';
  import EvidencePanel from '$lib/components/EvidencePanel.svelte';
  import ModePanel from '$lib/components/ModePanel.svelte';
  import {
    SAVED_QUERIES,
    buildBrowserPrompt,
    buildContextExport,
    buildEvidenceMarkdown,
    copyText,
    filterSources,
    runSavedQuery,
    toggleFilterValue,
  } from '$lib/workbench/model';
  import { renderMarkdownPreview } from '$lib/workbench/markdown';
  import {
    applyFacetHighlights,
    buildCollectionProfile,
    buildHighlightFilters,
    buildLinkSummary,
    buildRollupSummaries,
    countFacetValues,
    fieldDisplayValue,
    mergeCollections,
    orderedFacetValues,
    sortSourcesByFacets,
    type FacetHighlightState,
    type FacetValueOrders,
    type SortDirectionState,
    type SortExclusionState,
    type TileRollup,
  } from '$lib/workbench/seelinks';
  import {
    EMPTY_FILTERS,
    type ContextExport,
    type FilterState,
    type WorkbenchCollection,
    type WorkbenchCorpus,
    type WorkbenchFacet,
    type WorkbenchSource,
  } from '$lib/workbench/types';
  import type { PageData } from './$types';

  export let data: PageData;

  type ViewMode = 'grid' | 'outline' | 'graph' | 'timeline' | 'reader' | 'table' | 'queries';
  type ReaderNoteMode = 'preview' | 'text';
  type DetailTab = 'overview' | 'images';
  type SavedContext = { name: string; sourceIds: string[] };

  const STORAGE_KEY = 'dark-data-workbench-contexts';

  let corpus: WorkbenchCorpus = data.corpus;
  let pack = data.pack ?? 'challenge-2';
  let filters: FilterState = { ...EMPTY_FILTERS };
  let query = '';
  let viewMode: ViewMode = 'grid';
  let aiMode: ContextExport['mode'] = 'no-ai';
  let selectedIds = new Set<string>();
  let highlightedIds = new Set<string>();
  let dismissedIds = new Set<string>();
  let colorFacetId: keyof FilterState | '' = '';
  let draggingFacetId: keyof FilterState | '' = '';
  let dragOverGrid = false;
  let activeSourceId = corpus.sources[0]?.sourceId ?? '';
  let savedContexts: SavedContext[] = [];
  let userQuestion = '';
  let contextName = '';
  let exportStatus = '';
  let savedQueryId = SAVED_QUERIES[0].id;
  let savedQueryResults: WorkbenchSource[] = runSavedQuery(corpus, savedQueryId);
  let hydrated = false;
  let readerNoteMode: ReaderNoteMode = 'preview';
  let detailTab: DetailTab = 'overview';
  let detailSourceId = '';
  let facetOrder: Array<keyof FilterState> = corpus.facets.map((facet) => facet.id);
  let facetOpen = new Set<keyof FilterState>();
  let pinnedFacets = new Set<keyof FilterState>();
  let showMetadataFacets = false;
  let facetValueOrders: FacetValueOrders = {};
  let facetValueReversed: SortDirectionState = {};
  let sortByFacets: Array<keyof FilterState> = [];
  let sortDirections: SortDirectionState = {};
  let sortExclusions: SortExclusionState = {};
  let activeLegendFacet: keyof FilterState | '' = '';
  let facetHighlights: FacetHighlightState = {};
  let viewSourceIds: Set<string> | null = null;
  let viewTitle = 'All sources';
  let viewHistory: Array<{
    label: string;
    sourceIds: string[] | null;
    viewTitle: string;
    highlightedIds: string[];
    facetHighlights: FacetHighlightState;
  }> = [];
  let tileRollups: TileRollup[] = [];
  let tileRollupCollapsed = new Set<string>();
  let draggingFacetValue: { facet: keyof FilterState; value: string } | null = null;
  let dragOverOrder = false;
  let storedCollections: WorkbenchCollection[] = [];
  let collectionName = '';
  let activeCollectionName: string | null = null;
  let showCollectionProfile = false;
  let printStatus = '';
  let importStatus = '';
  let editingField: 'flags' | 'topics' | 'sourceFamilies' = 'flags';
  let editingValue = '';
  let workingSources: WorkbenchSource[] = corpus.sources;
  let tileTitleField = 'title';
  let tileSubtitleField = 'tileSubtitle';
  let showTileIdBadge = true;
  let sidebarWidth = 360;
  let sidebarWidthKey = '';

  const resetForCorpus = (nextCorpus: WorkbenchCorpus, nextPack: string) => {
    corpus = nextCorpus;
    pack = nextPack;
    workingSources = nextCorpus.sources;
    filters = { ...EMPTY_FILTERS };
    query = '';
    viewMode = 'grid';
    selectedIds = new Set();
    highlightedIds = new Set();
    dismissedIds = new Set();
    colorFacetId = '';
    draggingFacetId = '';
    dragOverGrid = false;
    activeSourceId = nextCorpus.sources[0]?.sourceId ?? '';
    detailSourceId = '';
    savedQueryId = SAVED_QUERIES[0].id;
    savedQueryResults = runSavedQuery(nextCorpus, savedQueryId);
    readerNoteMode = 'preview';
    detailTab = 'overview';
    facetOrder = nextCorpus.facets.map((facet) => facet.id);
    facetOpen = new Set();
    pinnedFacets = new Set();
    showMetadataFacets = false;
    facetValueOrders = {};
    facetValueReversed = {};
    sortByFacets = [];
    sortDirections = {};
    sortExclusions = {};
    activeLegendFacet = '';
    facetHighlights = {};
    viewSourceIds = null;
    viewTitle = 'All sources';
    viewHistory = [];
    tileRollups = [];
    tileRollupCollapsed = new Set();
    activeCollectionName = null;
    showCollectionProfile = false;
    editingValue = '';
  };

  $: {
    const nextPack = data.pack ?? 'challenge-2';
    if (data.corpus !== corpus || nextPack !== pack) {
      resetForCorpus(data.corpus, nextPack);
    }
  }

  $: packKey = `${pack}:${corpus.packId ?? corpus.title}`;
  $: sourceUniverse = viewSourceIds ? workingSources.filter((source) => viewSourceIds?.has(source.sourceId)) : workingSources;
  $: filteredBeforeSort = filterSources(sourceUniverse, filters, query);
  $: facetCounts = countFacetValues(filteredBeforeSort, corpus.facets);
  $: visibleFacetOrder = facetOrder.filter((facetId) => corpus.facets.some((facet) => facet.id === facetId));
  $: visibleFacets = visibleFacetOrder
    .map((facetId) => corpus.facets.find((facet) => facet.id === facetId))
    .filter((facet): facet is WorkbenchFacet => Boolean(facet))
    .filter((facet) => showMetadataFacets || !facet.metadata || pinnedFacets.has(facet.id) || sortByFacets.includes(facet.id));
  $: sortFacetOrders = Object.fromEntries(
    corpus.facets.map((facet) => [
      facet.id,
      orderedFacetValues(facet, facetCounts[facet.id] ?? {}, facetValueOrders[facet.id], Boolean(facetValueReversed[facet.id])).map(
        (entry) => entry.value
      ),
    ])
  ) as FacetValueOrders;
  $: filteredSources = sortSourcesByFacets(filteredBeforeSort, sortByFacets, sortFacetOrders, sortDirections, sortExclusions);
  $: facetHighlightedSources = applyFacetHighlights(filteredSources, facetHighlights);
  $: activeFacetHighlightIds = new Set(facetHighlightedSources.map((source) => source.sourceId));
  $: effectiveHighlightedIds = new Set([...highlightedIds, ...activeFacetHighlightIds]);
  $: visibleSources = filteredSources.filter((source) => !dismissedIds.has(source.sourceId));
  $: selectedSources = workingSources.filter((source) => selectedIds.has(source.sourceId));
  $: currentCollectionSources = activeCollectionName
    ? visibleSources.filter((source) => selectedIds.has(source.sourceId))
    : selectedSources;
  $: activeSource =
    workingSources.find((source) => source.sourceId === activeSourceId) ?? visibleSources[0] ?? workingSources[0] ?? null;
  $: detailSource = detailSourceId ? workingSources.find((source) => source.sourceId === detailSourceId) ?? null : null;
  $: detailImages = detailSource
    ? Array.from(new Set([...(detailSource.gallery ?? []), detailSource.thumbnailPath].filter(Boolean) as string[]))
    : [];
  $: collections = mergeCollections(corpus.collections ?? [], storedCollections);
  $: collectionProfile = buildCollectionProfile(currentCollectionSources.length ? currentCollectionSources : selectedSources, corpus.facets);
  $: linkSummary = buildLinkSummary(visibleSources, corpus.facets);
  $: rollupSummaries = buildRollupSummaries(visibleSources, tileRollups);
  $: rolledUpSourceIds = new Set(
    rollupSummaries.filter((rollup) => tileRollupCollapsed.has(rollup.key)).flatMap((rollup) => rollup.sourceIds)
  );
  $: tileSources = visibleSources.filter((source) => !rolledUpSourceIds.has(source.sourceId));
  $: outlineFacet =
    corpus.facets.find((facet) => facet.id === (activeLegendFacet || sortByFacets[0])) ??
    visibleFacets[0] ??
    corpus.facets[0] ??
    null;
  $: outlineGroups = outlineFacet
    ? orderedValuesForFacet(outlineFacet)
        .map((value) => ({
          value: value.value,
          count: value.count,
          sources: visibleSources.filter((source) => sourceFacetValues(source, outlineFacet.id).includes(value.value)),
        }))
        .filter((entry) => entry.sources.length)
    : [{ value: 'Sources', count: visibleSources.length, sources: visibleSources }];
  $: timelineGroups = groupSourcesByLabel(visibleSources, timelineLabelForSource);
  $: contextExport = buildContextExport({
    corpus,
    visibleSources,
    selectedIds,
    highlightedIds: effectiveHighlightedIds,
    filters,
    question: userQuestion,
    query,
    mode: aiMode,
    viewReduction: viewTitle,
    sortBy: sortByFacets,
    activeCollection: activeCollectionName,
    highlightFilters: buildHighlightFilters(facetHighlights),
  });
  $: contextSourceCount = contextExport.sources.length;
  $: graphTopics = corpus.topics.slice(0, 8);
  $: workbookSources = corpus.sources.filter((source) => source.format === 'xlsx');
  $: colorFacet = colorFacetId ? corpus.facets.find((facet) => facet.id === colorFacetId) ?? null : null;
  $: visibleHighlightedCount = visibleSources.filter((source) => effectiveHighlightedIds.has(source.sourceId)).length;
  $: dismissedCount = dismissedIds.size;
  $: isNarrativePack = pack === 'hmrc-narrative';
  $: topbarDescription = isNarrativePack
    ? 'Browse the HMRC talk narrative arc as slide thumbnails, source cards, repo evidence, transcripts, and conversation traces.'
    : 'Build an auditable source context, browse it without AI, or export it for browser AI and MCP clients.';

  onMount(() => {
    hydrated = true;
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      try {
        savedContexts = JSON.parse(stored);
      } catch {
        savedContexts = [];
      }
    }
    void loadCollections(packKey).then((rows) => {
      storedCollections = rows;
    });
  });

  const persistContexts = (contexts: SavedContext[]) => {
    savedContexts = contexts;
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(contexts));
    }
  };

  const prefKey = (name: string) => `dark-data-workbench:${packKey}:${name}`;
  const readJsonPref = <T,>(name: string, fallback: T): T => {
    if (typeof localStorage === 'undefined') return fallback;
    try {
      const raw = localStorage.getItem(prefKey(name));
      return raw ? (JSON.parse(raw) as T) : fallback;
    } catch {
      return fallback;
    }
  };
  const writeJsonPref = (name: string, value: unknown) => {
    if (typeof localStorage === 'undefined') return;
    localStorage.setItem(prefKey(name), JSON.stringify(value));
  };

  $: if (hydrated && packKey !== sidebarWidthKey) {
    sidebarWidthKey = packKey;
    sidebarWidth = readJsonPref('sidebarWidth', sidebarWidth);
    facetOrder = readJsonPref('facetOrder', corpus.facets.map((facet) => facet.id)).filter((facetId) =>
      corpus.facets.some((facet) => facet.id === facetId)
    ) as Array<keyof FilterState>;
    facetValueOrders = readJsonPref('facetValueOrders', {});
    facetValueReversed = readJsonPref('facetValueReversed', {});
    sortByFacets = readJsonPref('sortByFacets', []).filter((facetId) =>
      corpus.facets.some((facet) => facet.id === facetId)
    ) as Array<keyof FilterState>;
    sortDirections = readJsonPref('sortDirections', {});
    sortExclusions = readJsonPref('sortExclusions', {});
    pinnedFacets = new Set(readJsonPref<Array<keyof FilterState>>('pinnedFacets', []));
    showMetadataFacets = readJsonPref('showMetadataFacets', showMetadataFacets);
    tileTitleField = readJsonPref('tileTitleField', tileTitleField);
    tileSubtitleField = readJsonPref('tileSubtitleField', tileSubtitleField);
    showTileIdBadge = readJsonPref('showTileIdBadge', showTileIdBadge);
    void loadCollections(packKey).then((rows) => {
      storedCollections = rows;
    });
  }

  $: if (hydrated) {
    writeJsonPref('sidebarWidth', sidebarWidth);
    writeJsonPref('facetOrder', facetOrder);
    writeJsonPref('facetValueOrders', facetValueOrders);
    writeJsonPref('facetValueReversed', facetValueReversed);
    writeJsonPref('sortByFacets', sortByFacets);
    writeJsonPref('sortDirections', sortDirections);
    writeJsonPref('sortExclusions', sortExclusions);
    writeJsonPref('pinnedFacets', Array.from(pinnedFacets));
    writeJsonPref('showMetadataFacets', showMetadataFacets);
    writeJsonPref('tileTitleField', tileTitleField);
    writeJsonPref('tileSubtitleField', tileSubtitleField);
    writeJsonPref('showTileIdBadge', showTileIdBadge);
  }

  const setStatus = (message: string) => {
    exportStatus = message;
    setTimeout(() => {
      if (exportStatus === message) exportStatus = '';
    }, 2500);
  };

  const toggleSelect = (source: WorkbenchSource) => {
    const next = new Set(selectedIds);
    if (next.has(source.sourceId)) next.delete(source.sourceId);
    else next.add(source.sourceId);
    selectedIds = next;
  };

  const toggleHighlight = (source: WorkbenchSource) => {
    const next = new Set(highlightedIds);
    if (next.has(source.sourceId)) next.delete(source.sourceId);
    else next.add(source.sourceId);
    highlightedIds = next;
  };

  const openSource = (source: WorkbenchSource) => {
    activeSourceId = source.sourceId;
    viewMode = 'reader';
  };

  const openDetail = (source: WorkbenchSource) => {
    detailSourceId = source.sourceId;
    activeSourceId = source.sourceId;
    detailTab = 'overview';
    viewMode = 'grid';
  };

  const saveContext = () => {
    const name = contextName.trim();
    if (!name || selectedIds.size === 0) return;
    const next = savedContexts.filter((context) => context.name !== name);
    next.push({ name, sourceIds: Array.from(selectedIds).sort((a, b) => a.localeCompare(b)) });
    persistContexts(next);
    contextName = '';
    setStatus(`Saved context "${name}".`);
  };

  const openSavedContext = (name: string) => {
    const saved = savedContexts.find((context) => context.name === name);
    if (!saved) return;
    selectedIds = new Set(saved.sourceIds);
    viewMode = 'grid';
  };

  const facetHasActiveState = (facetId: keyof FilterState) =>
    filters[facetId].length > 0 || Boolean(facetHighlights[facetId]?.length);

  const retainedOpenFacets = (openedFacet?: keyof FilterState, omittedFacet?: keyof FilterState) =>
    new Set(
      corpus.facets
        .map((facet) => facet.id)
        .filter(
          (facetId) =>
            facetId !== omittedFacet &&
            (facetId === openedFacet || pinnedFacets.has(facetId) || facetHasActiveState(facetId))
        )
    );

  const toggleFacetOpen = (facetId: keyof FilterState) => {
    if (pinnedFacets.has(facetId)) return;
    if (facetOpen.has(facetId)) {
      facetOpen = retainedOpenFacets(undefined, facetId);
    } else {
      facetOpen = retainedOpenFacets(facetId);
    }
  };

  const togglePinnedFacet = (facetId: keyof FilterState) => {
    const next = new Set(pinnedFacets);
    if (next.has(facetId)) next.delete(facetId);
    else next.add(facetId);
    pinnedFacets = next;
    if (next.has(facetId)) facetOpen = new Set([...facetOpen, facetId]);
  };

  const reorderFacet = (from: keyof FilterState, to: keyof FilterState) => {
    if (from === to) return;
    const next = facetOrder.filter((facetId) => facetId !== from);
    const index = next.indexOf(to);
    next.splice(index < 0 ? next.length : index, 0, from);
    facetOrder = next;
  };

  const addSortFacet = (facetId: keyof FilterState) => {
    if (!sortByFacets.includes(facetId)) sortByFacets = [...sortByFacets, facetId];
    activeLegendFacet = facetId;
  };

  const toggleSortFacet = (facetId: keyof FilterState) => {
    if (sortByFacets.includes(facetId)) {
      sortByFacets = sortByFacets.filter((entry) => entry !== facetId);
      if (activeLegendFacet === facetId) activeLegendFacet = '';
    } else {
      addSortFacet(facetId);
    }
  };

  const reverseFacetOrder = (facetId: keyof FilterState) => {
    facetValueReversed = { ...facetValueReversed, [facetId]: !facetValueReversed[facetId] };
  };

  const toggleSortExclusion = (facetId: keyof FilterState, value: string) => {
    const current = new Set(sortExclusions[facetId] ?? []);
    if (current.has(value)) current.delete(value);
    else current.add(value);
    sortExclusions = { ...sortExclusions, [facetId]: Array.from(current).sort((a, b) => a.localeCompare(b)) };
  };

  const orderedValuesForFacet = (facet: WorkbenchFacet) =>
    orderedFacetValues(
      facet,
      facetCounts[facet.id] ?? {},
      facetValueOrders[facet.id],
      Boolean(facetValueReversed[facet.id])
    );

  const autoOrderFacetValues = (facetId: keyof FilterState) => {
    const facet = corpus.facets.find((entry) => entry.id === facetId);
    if (!facet) return;
    facetValueOrders = { ...facetValueOrders, [facetId]: orderedValuesForFacet(facet).map((entry) => entry.value) };
  };

  const clearFacetValueOrder = (facetId: keyof FilterState) => {
    const next = { ...facetValueOrders };
    delete next[facetId];
    facetValueOrders = next;
  };

  const reorderFacetValue = (facetId: keyof FilterState, from: string, to: string) => {
    if (from === to) return;
    const facet = corpus.facets.find((entry) => entry.id === facetId);
    if (!facet) return;
    const current = (facetValueOrders[facetId] ?? orderedValuesForFacet(facet).map((entry) => entry.value)).filter((value) => value !== from);
    const index = current.indexOf(to);
    current.splice(index < 0 ? current.length : index, 0, from);
    facetValueOrders = { ...facetValueOrders, [facetId]: current };
  };

  const setPrimaryHighlight = (facetId: keyof FilterState, value: string) => {
    facetHighlights = { ...facetHighlights, [facetId]: [value] };
  };

  const adjustHighlight = (facetId: keyof FilterState, value: string) => {
    const current = new Set(facetHighlights[facetId] ?? []);
    if (current.has(value)) current.delete(value);
    else current.add(value);
    facetHighlights = { ...facetHighlights, [facetId]: Array.from(current).sort((a, b) => a.localeCompare(b)) };
  };

  const clearFacetHighlight = (facetId: keyof FilterState) => {
    const next = { ...facetHighlights };
    delete next[facetId];
    facetHighlights = next;
  };

  const pushViewHistory = (label: string, nextSources: WorkbenchSource[]) => {
    viewHistory = [
      ...viewHistory,
      {
        label,
        sourceIds: viewSourceIds ? Array.from(viewSourceIds) : null,
        viewTitle,
        highlightedIds: Array.from(highlightedIds),
        facetHighlights,
      },
    ];
    viewSourceIds = new Set(nextSources.map((source) => source.sourceId));
    viewTitle = `${label} (${nextSources.length} of ${filteredSources.length})`;
    highlightedIds = new Set();
  };

  const chooseHighlighted = () => {
    const marked = visibleSources.filter((source) => effectiveHighlightedIds.has(source.sourceId));
    if (!marked.length) return;
    pushViewHistory('Highlighted', marked);
    facetHighlights = {};
  };

  const chooseUnhighlighted = () => {
    const markedIds = new Set(visibleSources.filter((source) => effectiveHighlightedIds.has(source.sourceId)).map((source) => source.sourceId));
    const unmarked = visibleSources.filter((source) => !markedIds.has(source.sourceId));
    if (!unmarked.length) return;
    pushViewHistory('Unhighlighted', unmarked);
    facetHighlights = {};
  };

  const undoView = () => {
    const previous = viewHistory.at(-1);
    if (!previous) return;
    viewSourceIds = previous.sourceIds ? new Set(previous.sourceIds) : null;
    viewTitle = previous.viewTitle;
    highlightedIds = new Set(previous.highlightedIds);
    facetHighlights = previous.facetHighlights;
    viewHistory = viewHistory.slice(0, -1);
  };

  const resetView = () => {
    filters = { ...EMPTY_FILTERS };
    query = '';
    dismissedIds = new Set();
    highlightedIds = new Set();
    facetHighlights = {};
    viewSourceIds = null;
    viewTitle = 'All sources';
    viewHistory = [];
    tileRollups = [];
    tileRollupCollapsed = new Set();
    activeCollectionName = null;
    showCollectionProfile = false;
  };

  const collectionSourceIds = () => (selectedIds.size ? Array.from(selectedIds) : visibleSources.map((source) => source.sourceId));

  const saveCollection = async () => {
    const name = collectionName.trim();
    const sourceIds = collectionSourceIds();
    if (!name || !sourceIds.length) return;
    const collection: WorkbenchCollection = {
      id: `collection-${name.toLowerCase().replace(/[^a-z0-9]+/g, '-')}-${Date.now()}`,
      name,
      sourceIds,
      createdAt: new Date().toISOString(),
    };
    storedCollections = [...storedCollections.filter((entry) => entry.name.toLowerCase() !== name.toLowerCase()), collection];
    await persistCollection(packKey, collection);
    collectionName = '';
    setStatus(`Saved collection "${name}".`);
  };

  const openCollection = (name: string) => {
    const collection = collections.find((entry) => entry.name === name);
    if (!collection) return;
    selectedIds = new Set(collection.sourceIds);
    viewSourceIds = new Set(collection.sourceIds);
    viewTitle = `Collection: ${name}`;
    activeCollectionName = name;
    viewMode = 'grid';
  };

  const editableValues = (source: WorkbenchSource, field: typeof editingField) => {
    if (field === 'flags') return source.flags;
    if (field === 'topics') return source.topics;
    return source.sourceFamilies ?? [];
  };

  const applyLocalEdit = () => {
    const value = editingValue.trim();
    if (!value || selectedIds.size === 0) return;
    workingSources = workingSources.map((source) => {
      if (!selectedIds.has(source.sourceId)) return source;
      const next = new Set(editableValues(source, editingField));
      next.add(value);
      return {
        ...source,
        [editingField]: Array.from(next).sort((a, b) => a.localeCompare(b)),
        searchText: `${source.searchText} ${value}`.toLowerCase(),
      };
    });
    editingValue = '';
    setStatus('Applied local edit to selected records.');
  };

  const printSelection = () => {
    printStatus = `${selectedIds.size || visibleSources.length} record${(selectedIds.size || visibleSources.length) === 1 ? '' : 's'} sent to print.`;
    if (typeof window !== 'undefined') window.print();
  };

  const titleForSource = (source: WorkbenchSource) => fieldDisplayValue(source, tileTitleField) || source.title;
  const subtitleForSource = (source: WorkbenchSource) =>
    tileSubtitleField === 'none' ? '' : fieldDisplayValue(source, tileSubtitleField) || source.tileSubtitle || source.department;

  const tileFieldOptions = [
    { value: 'title', label: 'Title' },
    { value: 'sourceId', label: 'Source ID' },
    { value: 'tileSubtitle', label: 'Tile subtitle' },
    { value: 'categoryPath', label: 'Category path' },
    { value: 'department', label: 'Department' },
    { value: 'status', label: 'Status' },
    { value: 'format', label: 'Format' },
    { value: 'documentType', label: 'Document type' },
    { value: 'summary', label: 'Summary' },
    { value: 'none', label: 'None' },
  ];

  const download = (filename: string, value: string, type: string) => {
    const blob = new Blob([value], { type });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  };

  const copyJson = async () => {
    const ok = await copyText(JSON.stringify(contextExport, null, 2));
    setStatus(ok ? 'AI context JSON copied.' : 'Clipboard unavailable; use download instead.');
  };

  const downloadJson = () => {
    download('dark-data-context.json', JSON.stringify(contextExport, null, 2), 'application/json');
    setStatus('AI context JSON downloaded.');
  };

  const copyPrompt = async () => {
    const ok = await copyText(buildBrowserPrompt(contextExport));
    setStatus(ok ? 'Browser AI prompt copied.' : 'Clipboard unavailable; use evidence bundle instead.');
  };

  const downloadEvidence = () => {
    download('dark-data-evidence.md', buildEvidenceMarkdown(contextExport), 'text/markdown');
    setStatus('Evidence bundle downloaded.');
  };

  const runQuery = (id: string) => {
    savedQueryId = id;
    savedQueryResults = runSavedQuery(corpus, id);
    userQuestion = SAVED_QUERIES.find((saved) => saved.id === id)?.question ?? userQuestion;
    highlightedIds = new Set(savedQueryResults.map((source) => source.sourceId));
    viewMode = 'queries';
  };

  const addQueryResultsToContext = () => {
    selectedIds = new Set([...selectedIds, ...savedQueryResults.map((source) => source.sourceId)]);
    setStatus('Saved-query results added to context.');
  };

  const markdownTables = (source: WorkbenchSource) =>
    source.noteText
      .split('\n')
      .filter((line) => line.trim().startsWith('|'))
      .slice(0, 40);

  const filterActive = (key: keyof FilterState, value: string) => filters[key].includes(value);
  const activateFacetValue = (facetId: keyof FilterState, value: string) => {
    setPrimaryHighlight(facetId, value);
    filters = toggleFilterValue(filters, facetId, value);
  };
  const sourceNoteHref = (source: WorkbenchSource) => `/api/source-note/${encodeURIComponent(source.sourceId)}`;
  const resolvableLinks = (source: WorkbenchSource) =>
    (source.links ?? []).filter((link) => link.href.startsWith('/api/') || link.href.startsWith('http://') || link.href.startsWith('https://'));
  const sourceFacetValues = (source: WorkbenchSource, facetId: keyof FilterState) => {
    if (facetId === 'departments') return [source.department];
    if (facetId === 'statuses') return [source.status];
    if (facetId === 'formats') return [source.format];
    if (facetId === 'topics') return source.topics;
    if (facetId === 'flags') return source.flags;
    if (facetId === 'sourceFamilies') return source.sourceFamilies ?? [];
    if (facetId === 'stages') return source.stages ?? [];
    if (facetId === 'assetTypes') return source.assetTypes ?? [];
    if (facetId === 'evidenceRoles') return source.evidenceRoles ?? [];
    if (facetId === 'governanceThemes') return source.governanceThemes ?? [];
    if (facetId === 'talkSections') return source.talkSections ?? [];
    if (facetId === 'provenanceModes') return source.provenanceModes ?? [];
    if (facetId === 'topicGroups') return source.topicGroups ?? [];
    if (facetId === 'screenfulls') return source.screenfulls ? [String(source.screenfulls)] : [];
    return [];
  };
  const groupSourcesByLabel = (sources: WorkbenchSource[], labelForSource: (source: WorkbenchSource) => string) => {
    const groups = new Map<string, WorkbenchSource[]>();
    for (const source of sources) {
      const label = labelForSource(source);
      groups.set(label, [...(groups.get(label) ?? []), source]);
    }
    return Array.from(groups.entries()).map(([value, groupedSources]) => ({
      value,
      count: groupedSources.length,
      sources: groupedSources,
    }));
  };
  const timelineLabelForSource = (source: WorkbenchSource) =>
    source.stages?.[0] ?? source.talkSections?.[0] ?? source.publicationDate ?? source.lastUpdated ?? 'Unplaced';
  const pastelPalette = [
    { bg: '#e3f2ef', border: '#2f766d', text: '#102f2a' },
    { bg: '#fff1cf', border: '#9a6b00', text: '#3a2600' },
    { bg: '#e5eefc', border: '#3d6aa6', text: '#132f57' },
    { bg: '#fde7ef', border: '#a44368', text: '#4f1730' },
    { bg: '#efe9fb', border: '#7057a8', text: '#2f2357' },
    { bg: '#f8eadb', border: '#a2602d', text: '#44240e' },
    { bg: '#e4f0fb', border: '#27758c', text: '#0e3946' },
    { bg: '#e9f4dc', border: '#5e7e24', text: '#26360b' },
    { bg: '#f0edf0', border: '#6b6470', text: '#2c2930' },
    { bg: '#f7e4dc', border: '#9b523c', text: '#432016' },
  ];
  const colorForFacetValue = (facet: WorkbenchFacet, value: string) => {
    if (facet.kind === 'measure') {
      const numbers = facet.values.map((entry) => Number(entry.value)).filter((entry) => Number.isFinite(entry));
      const numeric = Number(value);
      if (!numbers.length || !Number.isFinite(numeric)) return pastelPalette[0];
      const min = Math.min(...numbers);
      const max = Math.max(...numbers);
      const ratio = max === min ? 0.45 : (numeric - min) / (max - min);
      const lightness = Math.round(94 - ratio * 22);
      return {
        bg: `hsl(188 55% ${lightness}%)`,
        border: `hsl(188 55% 34%)`,
        text: '#082f35',
      };
    }
    const index = Math.max(0, facet.values.findIndex((entry) => entry.value === value));
    return pastelPalette[index % pastelPalette.length];
  };
  const colorReasonForSource = (source: WorkbenchSource, facet: WorkbenchFacet | null) => {
    if (!facet) return null;
    const values = sourceFacetValues(source, facet.id);
    const ordered = facet.values.map((entry) => entry.value);
    const value = ordered.find((entry) => values.includes(entry)) ?? values[0];
    if (!value) return null;
    return { label: facet.label, value, color: colorForFacetValue(facet, value) };
  };
  const sourceCardStyle = (source: WorkbenchSource, facet: WorkbenchFacet | null) => {
    const reason = colorReasonForSource(source, facet);
    if (!reason) return '';
    return `--source-card-bg:${reason.color.bg}; --source-card-border:${reason.color.border}; --source-card-text:${reason.color.text}; --source-card-muted:${reason.color.text};`;
  };
  const startFacetDrag = (event: DragEvent, facetId: keyof FilterState) => {
    draggingFacetId = facetId;
    if (event.dataTransfer) {
      event.dataTransfer.effectAllowed = 'copy';
      event.dataTransfer.setData('text/plain', facetId);
      event.dataTransfer.setData('application/x-workbench-facet', facetId);
    }
  };
  const startFacetValueDrag = (event: DragEvent, facetId: keyof FilterState, value: string) => {
    draggingFacetValue = { facet: facetId, value };
    if (event.dataTransfer) {
      event.dataTransfer.effectAllowed = 'move';
      event.dataTransfer.setData('text/plain', value);
      event.dataTransfer.setData('application/x-workbench-facet-value', JSON.stringify({ facet: facetId, value }));
    }
  };
  const readFacetValueDrag = (event: DragEvent) => {
    if (draggingFacetValue) return draggingFacetValue;
    const raw = event.dataTransfer?.getData('application/x-workbench-facet-value');
    if (!raw) return null;
    try {
      const parsed = JSON.parse(raw) as { facet?: keyof FilterState; value?: string };
      if (!parsed.facet || !parsed.value) return null;
      return { facet: parsed.facet, value: parsed.value };
    } catch {
      return null;
    }
  };
  const applyFacetColoringFromDrop = (event: DragEvent) => {
    const facetValue = readFacetValueDrag(event);
    if (facetValue) {
      const key = `${facetValue.facet}::${facetValue.value}`;
      if (!tileRollups.some((rollup) => `${rollup.facet}::${rollup.value}` === key)) {
        tileRollups = [...tileRollups, facetValue];
      }
      colorFacetId = facetValue.facet;
      draggingFacetValue = null;
      draggingFacetId = '';
      dragOverGrid = false;
      setStatus(`Added rollup for ${facetValue.value}.`);
      return;
    }
    const facetId = (draggingFacetId || event.dataTransfer?.getData('application/x-workbench-facet') || event.dataTransfer?.getData('text/plain')) as keyof FilterState;
    draggingFacetId = '';
    dragOverGrid = false;
    if (!facetId || !corpus.facets.some((facet) => facet.id === facetId)) return;
    colorFacetId = facetId;
    setStatus(`Card colour set by ${corpus.facets.find((facet) => facet.id === facetId)?.label ?? facetId}.`);
  };
  const markedSourcesForToolbarAction = () => {
    const explicitMarked = visibleSources.filter((source) => highlightedIds.has(source.sourceId));
    if (explicitMarked.length) return explicitMarked;
    return visibleSources.filter((source) => effectiveHighlightedIds.has(source.sourceId));
  };
  const dismissHighlighted = () => {
    const marked = markedSourcesForToolbarAction();
    if (!marked.length) return;
    dismissedIds = new Set([...dismissedIds, ...marked.map((source) => source.sourceId)]);
    highlightedIds = new Set([...highlightedIds].filter((sourceId) => !dismissedIds.has(sourceId)));
    facetHighlights = {};
    setStatus(`Dismissed ${marked.length} marked card${marked.length === 1 ? '' : 's'}.`);
  };
  const keepHighlighted = () => {
    const marked = markedSourcesForToolbarAction();
    if (!marked.length) return;
    const markedIds = new Set(marked.map((source) => source.sourceId));
    const toDismiss = visibleSources.filter((source) => !markedIds.has(source.sourceId)).map((source) => source.sourceId);
    dismissedIds = new Set([...dismissedIds, ...toDismiss]);
    setStatus(`Kept ${marked.length} marked card${marked.length === 1 ? '' : 's'} in view.`);
  };
</script>

<svelte:head>
  <title>Dark Data Workbench</title>
</svelte:head>

<main class="workbench-shell">
  <header class="topbar">
    <div>
      <p class="eyebrow">{isNarrativePack ? 'HMRC narrative' : 'Challenge 2'}</p>
      <h1>{corpus.title}</h1>
      <p>{topbarDescription}</p>
      <nav class="pack-switch" aria-label="Workbench pack">
        <a class:active={!isNarrativePack} href="/">Challenge 2 corpus</a>
        <a class:active={isNarrativePack} href="/?pack=hmrc-narrative">HMRC narrative pack</a>
      </nav>
    </div>
    <div class="stats-grid" aria-label="Corpus statistics">
      <div class:ready={hydrated}><strong>{hydrated ? 'JS' : 'SSR'}</strong><span>{hydrated ? 'ready' : 'loading'}</span></div>
      <div><strong>{corpus.sourceCount}</strong><span>sources</span></div>
      <div><strong>{corpus.stats.flaggedSources}</strong><span>flagged</span></div>
      <div><strong>{corpus.stats.workbookSources}</strong><span>workbooks</span></div>
      <div><strong>{visibleSources.length}</strong><span>visible</span></div>
    </div>
  </header>

  <div class="workspace">
    <aside class="left-rail" style={`--left-rail-width:${sidebarWidth}px; width:${sidebarWidth}px;`}>
      <label class="rail-resizer">
        <span>Rail width</span>
        <input type="range" min="280" max="520" step="10" bind:value={sidebarWidth} aria-label="Left rail width" />
      </label>

      <section class="panel dataset-panel" aria-label="Dataset controls">
        <div class="panel-heading compact">
          <div>
            <h2>Dataset</h2>
            <p>{pack === 'hmrc-narrative' ? 'HMRC narrative pack' : 'Challenge 2 corpus'}</p>
          </div>
        </div>
        <div class="dataset-actions">
          <a class:active={!isNarrativePack} href="/">Challenge 2</a>
          <a class:active={isNarrativePack} href="/?pack=hmrc-narrative">HMRC</a>
        </div>
        <label class="file-import">
          Load JSON/JSONL
          <input
            type="file"
            accept=".json,.jsonl,application/json"
            on:change={() => {
              importStatus = 'Local file import control is present; imported packs stay in browser state and do not write repo files.';
            }}
          />
        </label>
        <p class="muted">{importStatus || 'API, MCP pack, and file import controls are local-only in this repo build.'}</p>
      </section>

      <section class="panel order-panel" aria-label="Order by">
        <div class="panel-heading compact">
          <div>
            <h2>Order by</h2>
            <p>{sortByFacets.length ? `${sortByFacets.length} facet${sortByFacets.length === 1 ? '' : 's'}` : 'Drag facets here'}</p>
          </div>
          <button type="button" class="secondary" on:click={() => (sortByFacets = [])} disabled={!sortByFacets.length}>Clear</button>
        </div>
        <div
          class="order-list"
          class:drag-over={dragOverOrder}
          role="list"
          aria-label="Order by facets"
          on:dragenter|preventDefault={() => (dragOverOrder = true)}
          on:dragover|preventDefault={() => (dragOverOrder = true)}
          on:dragleave={() => (dragOverOrder = false)}
          on:drop|preventDefault={(event) => {
            const facetId = (draggingFacetId || event.dataTransfer?.getData('application/x-workbench-facet') || event.dataTransfer?.getData('text/plain')) as keyof FilterState;
            dragOverOrder = false;
            draggingFacetId = '';
            if (corpus.facets.some((facet) => facet.id === facetId)) addSortFacet(facetId);
          }}
        >
          {#if sortByFacets.length === 0}
            <p class="muted">Drop a facet here or press its sort button.</p>
          {:else}
            {#each sortByFacets as facetId, index}
              {@const facet = corpus.facets.find((entry) => entry.id === facetId)}
              {#if facet}
                <div class="order-chip" role="listitem">
                  <button type="button" class="order-index" on:click={() => reverseFacetOrder(facetId)} aria-label={`Reverse ${facet.label}`}>
                    {index + 1}{facetValueReversed[facetId] ? '↓' : '↑'}
                  </button>
                  <button type="button" class:active={activeLegendFacet === facetId} on:click={() => (activeLegendFacet = activeLegendFacet === facetId ? '' : facetId)}>
                    {facet.label}
                  </button>
                  <button type="button" class="chip-remove" aria-label={`Remove ${facet.label} from order`} on:click={() => (sortByFacets = sortByFacets.filter((entry) => entry !== facetId))}>x</button>
                </div>
              {/if}
            {/each}
          {/if}
        </div>
        {#if activeLegendFacet}
          {@const legendFacet = corpus.facets.find((entry) => entry.id === activeLegendFacet)}
          {#if legendFacet}
            <div class="order-legend" aria-label={`Legend for ${legendFacet.label}`}>
              <strong>{legendFacet.label} legend</strong>
              <div class="facet-values compact-values">
                {#each orderedValuesForFacet(legendFacet) as value}
                  {@const excluded = (sortExclusions[legendFacet.id] ?? []).includes(value.value)}
                  <button type="button" class:excluded class="facet-chip" aria-pressed={excluded ? 'false' : 'true'} on:click={() => toggleSortExclusion(legendFacet.id, value.value)}>
                    <span>{value.value}</span>
                  </button>
                {/each}
              </div>
            </div>
          {/if}
        {/if}
      </section>

      <section class="panel filter-panel" aria-label="Filters">
        <div class="panel-heading">
          <div>
            <h2>Explore</h2>
            <p>{corpus.sourceCount} sources</p>
          </div>
          <button
            type="button"
            class="icon-button"
            title="Clear filters"
            aria-label="Clear filters"
            on:click={() => {
              resetView();
            }}
          >
            x
          </button>
        </div>

        <label class="search-field">
          <span>Search</span>
          <input
            type="search"
            bind:value={query}
            placeholder="Search sources, topics, flags"
            aria-label="Search sources, topics, flags"
          />
        </label>

        <label class="facet-toggle">
          <input type="checkbox" bind:checked={showMetadataFacets} />
          Metadata
        </label>

        {#each visibleFacets as facet}
          <div
            class="facet"
            class:drag-over={draggingFacetId && draggingFacetId !== facet.id}
            role="group"
            aria-label={`Facet ${facet.label}`}
            on:dragenter|preventDefault={() => {}}
            on:dragover|preventDefault={() => {}}
            on:drop|preventDefault={(event) => {
              const from = (draggingFacetId || event.dataTransfer?.getData('application/x-workbench-facet') || event.dataTransfer?.getData('text/plain')) as keyof FilterState;
              if (from) reorderFacet(from, facet.id);
              draggingFacetId = '';
            }}
          >
            <div class="facet-header">
              <button type="button" class="pin" aria-label={pinnedFacets.has(facet.id) ? `Unpin ${facet.label}` : `Pin ${facet.label}`} on:click={() => togglePinnedFacet(facet.id)}>
                {pinnedFacets.has(facet.id) ? 'Unpin' : 'Pin'}
              </button>
              <button type="button" class="sort" aria-pressed={sortByFacets.includes(facet.id) ? 'true' : 'false'} aria-label={sortByFacets.includes(facet.id) ? `Remove ${facet.label} from order-by list` : `Add ${facet.label} to order-by list`} on:click={() => toggleSortFacet(facet.id)}>
                {sortByFacets.includes(facet.id) ? (facetValueReversed[facet.id] ? '↓' : '↑') : '↕'}
              </button>
              <h3>
                <button
                  type="button"
                  draggable="true"
                  class="facet-title"
                  class:colouring={colorFacetId === facet.id}
                  aria-expanded={facetOpen.has(facet.id) || pinnedFacets.has(facet.id) ? 'true' : 'false'}
                  title="Drag this facet name onto the card grid to colour cards by its values"
                  on:click={() => toggleFacetOpen(facet.id)}
                  on:dragstart={(event) => startFacetDrag(event, facet.id)}
                  on:dragend={() => {
                    draggingFacetId = '';
                    dragOverGrid = false;
                  }}
                >
                  {facet.label}
                </button>
              </h3>
              {#if facetHighlights[facet.id]?.length || filters[facet.id].length}
                <button type="button" class="chip-remove" aria-label={`Clear ${facet.label}`} on:click={() => {
                  clearFacetHighlight(facet.id);
                  filters = { ...filters, [facet.id]: [] };
                }}>x</button>
              {/if}
            </div>
            {#if facetOpen.has(facet.id) || pinnedFacets.has(facet.id)}
            <div class="facet-actions">
              <button type="button" class="secondary" on:click={() => autoOrderFacetValues(facet.id)}>Auto order</button>
              <button type="button" class="secondary" on:click={() => clearFacetValueOrder(facet.id)} disabled={!facetValueOrders[facet.id]}>Clear order</button>
            </div>
            <div class="facet-values">
              {#each orderedValuesForFacet(facet).slice(0, facet.id === 'topics' ? 24 : 16) as value}
                <button
                  type="button"
                  class:active={filterActive(facet.id, value.value)}
                  class:highlighted={facetHighlights[facet.id]?.includes(value.value)}
                  class="facet-chip"
                  draggable="true"
                  aria-pressed={filterActive(facet.id, value.value) ? 'true' : 'false'}
                  title="Click to filter and mark, right-click to adjust the mark set, double-click to choose, drag to reorder or roll up"
                  on:click={() => activateFacetValue(facet.id, value.value)}
                  on:contextmenu|preventDefault={() => adjustHighlight(facet.id, value.value)}
                  on:dblclick={() => {
                    setPrimaryHighlight(facet.id, value.value);
                    if (!filters[facet.id].includes(value.value)) {
                      filters = toggleFilterValue(filters, facet.id, value.value);
                    }
                    chooseHighlighted();
                  }}
                  on:dragstart={(event) => startFacetValueDrag(event, facet.id, value.value)}
                  on:drop|preventDefault|stopPropagation={(event) => {
                    const payload = readFacetValueDrag(event);
                    if (payload?.facet === facet.id) reorderFacetValue(facet.id, payload.value, value.value);
                    draggingFacetValue = null;
                  }}
                  on:dragend={() => (draggingFacetValue = null)}
                >
                  <span>{value.value}</span>
                  <small>{value.count}</small>
                </button>
              {/each}
            </div>
            {/if}
          </div>
        {/each}
      </section>

      <section class="panel links-panel" aria-label="Links">
        <h2>Links</h2>
        {#if linkSummary.length === 0}
          <p class="muted">No link data available.</p>
        {:else}
          {#each linkSummary as entry}
            <div class="link-summary">
              <strong>{entry.facet.label}</strong>
              <div class="facet-values compact-values">
                {#each entry.values as value}
                  <button type="button" class="facet-chip" on:click={() => setPrimaryHighlight(entry.facet.id, value.value)}>
                    <span>{value.value}</span>
                    <small>{value.count}</small>
                  </button>
                {/each}
              </div>
            </div>
          {/each}
        {/if}
      </section>

      <section class="panel collections-panel" aria-label="Collections">
        <h2>Collections</h2>
        <label>
          <span>Collection name</span>
          <input type="text" bind:value={collectionName} placeholder="Collection name" aria-label="Collection name" />
        </label>
        <button type="button" on:click={saveCollection} disabled={!collectionName.trim() || (!selectedIds.size && !visibleSources.length)}>Save collection</button>
        {#if collections.length === 0}
          <p class="muted">No collections yet.</p>
        {:else}
          <ul class="collection-list">
            {#each collections as collection}
              <li>
                <span>{collection.name} ({collection.sourceIds.length})</span>
                <button type="button" class="secondary" on:click={() => openCollection(collection.name)}>Open</button>
              </li>
            {/each}
          </ul>
        {/if}
        {#if activeCollectionName}
          <button type="button" class="secondary" on:click={() => (showCollectionProfile = !showCollectionProfile)}>{showCollectionProfile ? 'Hide analysis' : 'Analyze collection'}</button>
          {#if showCollectionProfile}
            <div class="collection-profile">
              {#each collectionProfile as entry}
                <div class="link-summary">
                  <strong>{entry.facet.label}</strong>
                  <div class="chips">
                    {#each entry.values as value}
                      <span class="chip">{value.value} <small>{value.count}</small></span>
                    {/each}
                  </div>
                </div>
              {/each}
            </div>
          {/if}
        {/if}
      </section>

      <section class="panel output-panel" aria-label="Printing and AI export">
        <h2>Printing</h2>
        <p class="muted">Prints selected records, or the current view if nothing is selected.</p>
        <button type="button" on:click={printSelection}>Print selection</button>
        {#if printStatus}<p class="muted">{printStatus}</p>{/if}
        <h2>AI export</h2>
        <p class="muted">Current export contains {contextSourceCount} record{contextSourceCount === 1 ? '' : 's'}.</p>
        <button type="button" class="secondary" on:click={copyJson}>Copy AI context</button>
        <button type="button" class="secondary" on:click={downloadJson}>Download AI context</button>
      </section>

      <section class="panel tile-text-panel" aria-label="Tile Text">
        <h2>Tile Text</h2>
        <label>
          <span>Title</span>
          <select bind:value={tileTitleField} aria-label="Tile title field">
            {#each tileFieldOptions.filter((option) => option.value !== 'none') as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </label>
        <label>
          <span>Subtitle</span>
          <select bind:value={tileSubtitleField} aria-label="Tile subtitle field">
            {#each tileFieldOptions as option}
              <option value={option.value}>{option.label}</option>
            {/each}
          </select>
        </label>
        <label class="facet-toggle">
          <input type="checkbox" bind:checked={showTileIdBadge} />
          Small ID badge
        </label>
      </section>

      <section class="panel editing-panel" aria-label="Editing">
        <h2>Editing</h2>
        <p class="muted">Local browser-only edits; source files and generated packs are not written.</p>
        <label>
          <span>Property</span>
          <select bind:value={editingField} aria-label="Editing property">
            <option value="flags">Flag</option>
            <option value="topics">Topic</option>
            <option value="sourceFamilies">Source family</option>
          </select>
        </label>
        <label>
          <span>Value</span>
          <input type="text" bind:value={editingValue} aria-label="Editing value" />
        </label>
        <button type="button" on:click={applyLocalEdit} disabled={!editingValue.trim() || selectedIds.size === 0}>Apply to selected</button>
      </section>
    </aside>

    <section class="main-stage" aria-label="Workbench results">
      <section class="question-box" aria-label="Question box">
        <div>
          <label for="workbench-question">Question</label>
          <p>{selectedIds.size ? `${selectedIds.size} selected sources in context` : `${visibleSources.length} visible sources available`}</p>
        </div>
        <textarea
          id="workbench-question"
          bind:value={userQuestion}
          rows="3"
          placeholder="Ask the question this evidence set should answer"
          aria-label="Question to answer"
        ></textarea>
        <button type="button" class="secondary" on:click={() => (userQuestion = '')} disabled={!userQuestion.trim()}>Clear</button>
      </section>

      <div class="stage-toolbar">
        <div>
          <h2>{visibleSources.length} visible sources</h2>
          <p>
            {viewTitle},
            {selectedIds.size} in context, {visibleHighlightedCount} marked in view
            {dismissedCount ? `, ${dismissedCount} dismissed` : ''}
            {colorFacet ? `, coloured by ${colorFacet.label}` : ''}
          </p>
        </div>
        <div class="toolbar-actions" aria-label="Marked-card actions">
          <button type="button" on:click={chooseHighlighted} disabled={!visibleHighlightedCount}>Choose highlighted</button>
          <button type="button" on:click={chooseUnhighlighted} disabled={!visibleHighlightedCount}>Choose unhighlighted</button>
          <button type="button" class="secondary" on:click={undoView} disabled={!viewHistory.length}>Undo view</button>
          <button type="button" class="secondary" on:click={resetView}>Reset</button>
          <button type="button" class="secondary" on:click={keepHighlighted} disabled={!visibleHighlightedCount}>Keep marked</button>
          <button type="button" class="secondary" on:click={dismissHighlighted} disabled={!visibleHighlightedCount}>Dismiss marked</button>
          <button type="button" class="secondary" on:click={() => (dismissedIds = new Set())} disabled={!dismissedCount}>Restore</button>
          <button type="button" class="secondary" on:click={() => (colorFacetId = '')} disabled={!colorFacet}>Clear colour</button>
        </div>
        <div class="segmented" aria-label="View mode">
          <button type="button" class:active={viewMode === 'grid'} aria-pressed={viewMode === 'grid' ? 'true' : 'false'} on:click={() => (viewMode = 'grid')}>Grid</button>
          <button type="button" class:active={viewMode === 'outline'} aria-pressed={viewMode === 'outline' ? 'true' : 'false'} on:click={() => (viewMode = 'outline')}>Outline</button>
          <button type="button" class:active={viewMode === 'reader'} aria-pressed={viewMode === 'reader' ? 'true' : 'false'} on:click={() => (viewMode = 'reader')}>Reader</button>
          <button type="button" class:active={viewMode === 'graph'} aria-pressed={viewMode === 'graph' ? 'true' : 'false'} on:click={() => (viewMode = 'graph')}>Graph</button>
          <button type="button" class:active={viewMode === 'timeline'} aria-pressed={viewMode === 'timeline' ? 'true' : 'false'} on:click={() => (viewMode = 'timeline')}>Timeline</button>
          <button type="button" class:active={viewMode === 'table'} aria-pressed={viewMode === 'table' ? 'true' : 'false'} on:click={() => (viewMode = 'table')}>Table</button>
          <button type="button" class:active={viewMode === 'queries'} aria-pressed={viewMode === 'queries' ? 'true' : 'false'} on:click={() => (viewMode = 'queries')}>Checks</button>
        </div>
      </div>
      {#if viewHistory.length}
        <div class="history-bar" aria-label="View history">
          {#each viewHistory as entry, index}
            <button
              type="button"
              class="history-chip"
              on:click={() => {
                viewSourceIds = entry.sourceIds ? new Set(entry.sourceIds) : null;
                viewTitle = entry.viewTitle;
                highlightedIds = new Set(entry.highlightedIds);
                facetHighlights = entry.facetHighlights;
                viewHistory = viewHistory.slice(0, index);
              }}
            >
              {entry.label}
            </button>
          {/each}
        </div>
      {/if}

      {#if viewMode === 'grid'}
        {#if detailSource}
          <section class="detail-dock" aria-label="Detail dock">
            <div class="detail-header">
              <div>
                <span class="source-id">{detailSource.sourceId}</span>
                <h2>{detailSource.title}</h2>
                <p>{detailSource.categoryPath ?? detailSource.documentType}</p>
              </div>
              <div class="detail-nav">
                <button type="button" class="secondary" on:click={() => {
                  const index = visibleSources.findIndex((source) => source.sourceId === detailSource.sourceId);
                  openDetail(visibleSources[Math.max(0, index - 1)] ?? detailSource);
                }}>Previous</button>
                <button type="button" class="secondary" on:click={() => {
                  const index = visibleSources.findIndex((source) => source.sourceId === detailSource.sourceId);
                  openDetail(visibleSources[Math.min(visibleSources.length - 1, index + 1)] ?? detailSource);
                }}>Next</button>
                <button type="button" class="secondary" on:click={() => (detailSourceId = '')}>Close</button>
              </div>
            </div>
            <div class="tile-strip" aria-label="Tile strip">
              {#each visibleSources.slice(0, 12) as source}
                <button type="button" class:active={detailSource.sourceId === source.sourceId} on:click={() => openDetail(source)}>
                  {source.sourceId}
                </button>
              {/each}
            </div>
            <div class="detail-tabs" role="tablist" aria-label="Detail tabs">
              <button type="button" class:active={detailTab === 'overview'} aria-pressed={detailTab === 'overview' ? 'true' : 'false'} on:click={() => (detailTab = 'overview')}>Overview</button>
              <button type="button" class:active={detailTab === 'images'} aria-pressed={detailTab === 'images' ? 'true' : 'false'} on:click={() => (detailTab = 'images')}>Images ({detailImages.length})</button>
            </div>
            {#if detailTab === 'overview'}
              <div class="detail-body">
                {#if detailSource.thumbnailPath}
                  <button type="button" class="detail-media" on:dblclick={() => (detailTab = 'images')} aria-label="Open images">
                    <img src={detailSource.thumbnailPath} alt={`Thumbnail for ${detailSource.title}`} />
                  </button>
                {/if}
                <div>
                  <p>{detailSource.summary}</p>
                  <div class="metadata-table compact">
                    <div><strong>Status</strong><span>{detailSource.status}</span></div>
                    <div><strong>Format</strong><span>{detailSource.format}</span></div>
                    <div><strong>Source</strong><code>{detailSource.sourcePath}</code></div>
                    <div><strong>Note</strong><code>{detailSource.notePath}</code></div>
                  </div>
                  {#if resolvableLinks(detailSource).length}
                    <div class="detail-links">
                      {#each resolvableLinks(detailSource) as link}
                        <a href={link.href} target="_blank" rel="noreferrer">{link.label}</a>
                      {/each}
                    </div>
                  {/if}
                </div>
              </div>
            {:else}
              <div class="detail-gallery">
                {#if detailImages.length}
                  {#each detailImages as image}
                    <figure>
                      <img src={image} alt={`Image for ${detailSource.title}`} />
                      <figcaption>{detailSource.title}</figcaption>
                    </figure>
                  {/each}
                {:else}
                  <p class="muted">No images available for this source.</p>
                {/if}
              </div>
            {/if}
          </section>
        {/if}
        {#if colorFacet}
          <div class="colour-legend" aria-live="polite">
            <strong>{colorFacet.label}</strong>
            {#each colorFacet.values.slice(0, 10) as value}
              {@const colour = colorForFacetValue(colorFacet, value.value)}
              <span style={`background:${colour.bg}; border-color:${colour.border}; color:${colour.text};`}>
                {value.value}
              </span>
            {/each}
          </div>
        {/if}
        <div
          class="source-grid"
          class:drag-over={dragOverGrid}
          role="list"
          aria-label="Source cards"
          on:dragenter|preventDefault={() => {
            if (draggingFacetId || draggingFacetValue) dragOverGrid = true;
          }}
          on:dragover|preventDefault={() => {
            if (draggingFacetId || draggingFacetValue) dragOverGrid = true;
          }}
          on:dragleave={() => {
            dragOverGrid = false;
          }}
          on:drop|preventDefault={applyFacetColoringFromDrop}
        >
          {#each rollupSummaries as rollup}
            <article class="source-card rollup-card" role="listitem" aria-label={`Rollup ${rollup.value}`}>
              <div class="card-top">
                <span class="source-id">{rollup.facet}</span>
                <span>{Math.round(rollup.fraction * 100)}%</span>
              </div>
              <h3>{rollup.value}</h3>
              <p>{rollup.count} of {rollup.total} visible sources.</p>
              <div class="card-actions">
                <button type="button" class="secondary" on:click={() => {
                  const key = `${rollup.facet}::${rollup.value}`;
                  const next = new Set(tileRollupCollapsed);
                  if (next.has(key)) next.delete(key);
                  else next.add(key);
                  tileRollupCollapsed = next;
                }}>{tileRollupCollapsed.has(rollup.key) ? 'Expand' : 'Collapse'}</button>
                <button type="button" class="secondary" on:click={() => (tileRollups = tileRollups.filter((entry) => !(entry.facet === rollup.facet && entry.value === rollup.value)))}>Remove</button>
              </div>
              <div class="rollup-bar"><span style={`width:${Math.max(2, Math.round(rollup.fraction * 100))}%`}></span></div>
            </article>
          {/each}
          {#each tileSources as source}
            {@const colourReason = colorReasonForSource(source, colorFacet)}
            {@const cardTitle = fieldDisplayValue(source, tileTitleField) || source.title}
            {@const cardSubtitle =
              tileSubtitleField === 'none' ? '' : fieldDisplayValue(source, tileSubtitleField) || source.tileSubtitle || source.department}
            <article
              class:selected={selectedIds.has(source.sourceId)}
              class:highlighted={effectiveHighlightedIds.has(source.sourceId)}
              class="source-card"
              style={sourceCardStyle(source, colorFacet)}
              role="listitem"
              aria-label={`Source ${source.sourceId}`}
              on:dblclick={() => openDetail(source)}
            >
              {#if source.thumbnailPath}
                <button type="button" class="thumbnail-button" on:click={() => openSource(source)} aria-label={`Open ${source.title}`}>
                  <img src={source.thumbnailPath} alt={`Thumbnail for ${source.title}`} loading="lazy" />
                </button>
              {/if}
              <div class="card-top">
                {#if showTileIdBadge}<span class="source-id">{source.sourceId}</span>{/if}
                <span class={`status status-${source.status.toLowerCase().replaceAll(' ', '-')}`}>{source.status}</span>
              </div>
              <h3>{cardTitle}</h3>
              {#if cardSubtitle}<small class="tile-subtitle">{cardSubtitle}</small>{/if}
              <p>{source.summary}</p>
              <div class="meta-line">
                <span>{source.talkSections?.[0] ?? source.department}</span>
                <span>{source.stages?.[0] ?? source.documentType}</span>
                <span>{source.format}</span>
                <span>{source.screenfulls ? `${source.screenfulls} screenfulls` : source.extractionQuality}</span>
              </div>
              {#if colourReason}
                <div class="colour-reason">{colourReason.label}: {colourReason.value}</div>
              {/if}
              {#if source.flags.length}
                <div class="chips" aria-label="Source flags">
                  {#each source.flags as flag}
                    <span class="chip warning">{flag}</span>
                  {/each}
                </div>
              {/if}
              <div class="chips" aria-label="Source topics">
                {#each source.topics.slice(0, 4) as topic}
                  <span class="chip">{topic}</span>
                {/each}
              </div>
              <div class="card-actions">
                <button type="button" class="secondary" on:click={() => openSource(source)}>Open</button>
                <button type="button" class="secondary" on:click={() => toggleHighlight(source)}>
                  {highlightedIds.has(source.sourceId) ? 'Unmark' : 'Mark'}
                </button>
                <button type="button" on:click={() => toggleSelect(source)}>
                  {selectedIds.has(source.sourceId) ? 'Remove' : 'Add'}
                </button>
              </div>
            </article>
          {/each}
        </div>
      {:else if viewMode === 'outline'}
        <section class="outline-view" aria-label="Outline view">
          <div class="outline-heading">
            <div>
              <h2>{outlineFacet ? `Outline by ${outlineFacet.label}` : 'Outline'}</h2>
              <p class="muted">{outlineGroups.length} group{outlineGroups.length === 1 ? '' : 's'} in the current view.</p>
            </div>
            {#if outlineFacet}
              <button type="button" class="secondary" on:click={() => addSortFacet(outlineFacet.id)}>Use for order</button>
            {/if}
          </div>
          <div class="outline-groups">
            {#each outlineGroups as group}
              <article class="outline-group">
                <header>
                  <h3>{group.value}</h3>
                  <span>{group.count}</span>
                </header>
                <div class="outline-items">
                  {#each group.sources.slice(0, 18) as source}
                    <button type="button" class:highlighted={effectiveHighlightedIds.has(source.sourceId)} on:click={() => openDetail(source)}>
                      <span>{source.sourceId}</span>
                      <strong>{titleForSource(source)}</strong>
                    </button>
                  {/each}
                </div>
              </article>
            {/each}
          </div>
        </section>
      {:else if viewMode === 'timeline'}
        <section class="timeline-view" aria-label="Timeline view">
          <div class="outline-heading">
            <div>
              <h2>Timeline</h2>
              <p class="muted">Records grouped by narrative stage, talk section, or available date.</p>
            </div>
          </div>
          <div class="timeline-list">
            {#each timelineGroups as group}
              <article class="timeline-group">
                <header>
                  <span class="timeline-dot"></span>
                  <div>
                    <h3>{group.value}</h3>
                    <p>{group.count} source{group.count === 1 ? '' : 's'}</p>
                  </div>
                </header>
                <div class="timeline-items">
                  {#each group.sources as source}
                    <button type="button" class:highlighted={effectiveHighlightedIds.has(source.sourceId)} on:click={() => openDetail(source)}>
                      <span>{source.sourceId}</span>
                      <strong>{titleForSource(source)}</strong>
                      <small>{subtitleForSource(source)}</small>
                    </button>
                  {/each}
                </div>
              </article>
            {/each}
          </div>
        </section>
      {:else if viewMode === 'reader'}
        <article class="reader">
          {#if activeSource}
            <div class="reader-heading">
              <div>
                <span class="source-id">{activeSource.sourceId}</span>
                <h2>{activeSource.title}</h2>
              </div>
              <div class="reader-actions">
                <button type="button" class="secondary" on:click={() => toggleSelect(activeSource)}>
                  {selectedIds.has(activeSource.sourceId) ? 'Remove from context' : 'Add to context'}
                </button>
                <a href={sourceNoteHref(activeSource)} target="_blank" rel="noreferrer">Open note</a>
              </div>
            </div>
            {#if activeSource.thumbnailPath}
              <div class="reader-media">
                <img src={activeSource.thumbnailPath} alt={`Thumbnail for ${activeSource.title}`} />
              </div>
            {/if}
            <div class="metadata-table">
              <div><strong>Status</strong><span>{activeSource.status}</span></div>
              <div><strong>Department</strong><span>{activeSource.department}</span></div>
              <div><strong>Format</strong><span>{activeSource.format}</span></div>
              {#if activeSource.talkSections?.length}
                <div><strong>Talk section</strong><span>{activeSource.talkSections.join(', ')}</span></div>
              {/if}
              {#if activeSource.stages?.length}
                <div><strong>Narrative stage</strong><span>{activeSource.stages.join(', ')}</span></div>
              {/if}
              {#if activeSource.governanceThemes?.length}
                <div><strong>Governance</strong><span>{activeSource.governanceThemes.join(', ')}</span></div>
              {/if}
              <div><strong>Raw source</strong><code>{activeSource.sourcePath}</code></div>
              <div><strong>Wiki note</strong><code>{activeSource.notePath}</code></div>
            </div>
            {#if resolvableLinks(activeSource).length}
              <div class="reader-links" aria-label="Narrative links">
                {#each resolvableLinks(activeSource) as link}
                  <a href={link.href} target="_blank" rel="noreferrer">{link.label}</a>
                {/each}
              </div>
            {/if}
            <div class="note-viewer">
              <div class="note-viewer-toolbar">
                <h3>Source note</h3>
                <div class="segmented" aria-label="Source note view">
                  <button
                    type="button"
                    class:active={readerNoteMode === 'preview'}
                    aria-pressed={readerNoteMode === 'preview' ? 'true' : 'false'}
                    on:click={() => (readerNoteMode = 'preview')}
                  >
                    Preview
                  </button>
                  <button
                    type="button"
                    class:active={readerNoteMode === 'text'}
                    aria-pressed={readerNoteMode === 'text' ? 'true' : 'false'}
                    on:click={() => (readerNoteMode = 'text')}
                  >
                    Text
                  </button>
                </div>
              </div>
              {#if readerNoteMode === 'preview'}
                <div class="note-preview">{@html renderMarkdownPreview(activeSource.noteText)}</div>
              {:else}
                <pre class="note-reader">{activeSource.noteText}</pre>
              {/if}
            </div>
          {/if}
        </article>
      {:else if viewMode === 'graph'}
        <section class="graph-view" aria-label="Topic graph">
          <div class="summary-meta">{graphTopics.length} topic nodes / {visibleSources.length} source nodes</div>
          <svg viewBox="0 0 940 520" role="img" aria-label="Topic to source graph">
            {#each graphTopics as topic, index}
              <g>
                <rect x="40" y={40 + index * 56} width="220" height="36" rx="6" />
                <text x="52" y={63 + index * 56}>{topic.label}</text>
              </g>
            {/each}
            {#each visibleSources.slice(0, 12) as source, index}
              <g>
                <rect class="source-node" x="610" y={32 + index * 38} width="270" height="28" rx="6" />
                <text x="622" y={51 + index * 38}>{source.sourceId}</text>
                {#if graphTopics.some((topic) => source.topics.includes(topic.id))}
                  <line
                    x1="260"
                    y1={58 + graphTopics.findIndex((topic) => source.topics.includes(topic.id)) * 56}
                    x2="610"
                    y2={46 + index * 38}
                  />
                {/if}
              </g>
            {/each}
          </svg>
        </section>
      {:else if viewMode === 'table'}
        <section class="table-view" aria-label="Workbook tables">
          <h2>Workbook Sources</h2>
          <p class="muted">Spreadsheet-derived notes retain tables in Markdown for quick inspection.</p>
          {#each workbookSources as source}
            <article class="table-card">
              <h3>{source.sourceId}: {source.title}</h3>
              <p>{source.summary}</p>
              <pre>{markdownTables(source).join('\n') || 'No Markdown table lines detected.'}</pre>
            </article>
          {/each}
        </section>
      {:else}
        <section class="checks-view" aria-label="Saved checks">
          <div class="checks-layout">
            <div>
              <h2>No-AI Saved Checks</h2>
              <p class="muted">These checks use deterministic filters and source text, then surface evidence for review.</p>
              <div class="query-list">
                {#each SAVED_QUERIES as saved}
                  <button type="button" class:active={savedQueryId === saved.id} aria-pressed={savedQueryId === saved.id ? 'true' : 'false'} on:click={() => runQuery(saved.id)}>
                    <strong>{saved.label}</strong>
                    <span>{saved.question}</span>
                  </button>
                {/each}
              </div>
              <button type="button" on:click={addQueryResultsToContext}>Add results to context</button>
            </div>
            <div class="query-results">
              <h3>{savedQueryResults.length} matching sources</h3>
              {#each savedQueryResults as source}
                <button type="button" class="result-row" on:click={() => openSource(source)}>
                  <span>{source.sourceId}</span>
                  <strong>{source.title}</strong>
                </button>
              {/each}
            </div>
          </div>
        </section>
      {/if}
    </section>

    <aside class="right-rail">
      <ContextBasket
        sources={selectedSources}
        {savedContexts}
        bind:contextName
        changeName={(value) => (contextName = value)}
        removeSource={toggleSelect}
        clearContext={() => (selectedIds = new Set())}
        saveCurrentContext={saveContext}
        openSavedContext={openSavedContext}
      />
      <ModePanel
        mode={aiMode}
        sourceCount={contextSourceCount}
        status={exportStatus}
        changeMode={(value) => (aiMode = value)}
        copyJson={copyJson}
        downloadJson={downloadJson}
        copyPrompt={copyPrompt}
        downloadMarkdown={downloadEvidence}
      />
      <EvidencePanel source={activeSource} {query} />
    </aside>
  </div>
</main>
