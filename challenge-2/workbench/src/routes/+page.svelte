<script lang="ts">
  import { onMount } from 'svelte';
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
  import { EMPTY_FILTERS, type ContextExport, type FilterState, type WorkbenchCorpus, type WorkbenchFacet, type WorkbenchSource } from '$lib/workbench/types';
  import type { PageData } from './$types';

  export let data: PageData;

  type ViewMode = 'grid' | 'reader' | 'graph' | 'table' | 'queries';
  type ReaderNoteMode = 'preview' | 'text';
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

  const resetForCorpus = (nextCorpus: WorkbenchCorpus, nextPack: string) => {
    corpus = nextCorpus;
    pack = nextPack;
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
    savedQueryId = SAVED_QUERIES[0].id;
    savedQueryResults = runSavedQuery(nextCorpus, savedQueryId);
    readerNoteMode = 'preview';
  };

  $: {
    const nextPack = data.pack ?? 'challenge-2';
    if (data.corpus !== corpus || nextPack !== pack) {
      resetForCorpus(data.corpus, nextPack);
    }
  }

  $: filteredSources = filterSources(corpus.sources, filters, query);
  $: visibleSources = filteredSources.filter((source) => !dismissedIds.has(source.sourceId));
  $: selectedSources = corpus.sources.filter((source) => selectedIds.has(source.sourceId));
  $: activeSource =
    corpus.sources.find((source) => source.sourceId === activeSourceId) ?? visibleSources[0] ?? corpus.sources[0] ?? null;
  $: contextExport = buildContextExport({
    corpus,
    visibleSources,
    selectedIds,
    highlightedIds,
    filters,
    question: userQuestion,
    query,
    mode: aiMode,
  });
  $: contextSourceCount = contextExport.sources.length;
  $: graphTopics = corpus.topics.slice(0, 8);
  $: workbookSources = corpus.sources.filter((source) => source.format === 'xlsx');
  $: colorFacet = colorFacetId ? corpus.facets.find((facet) => facet.id === colorFacetId) ?? null : null;
  $: visibleHighlightedCount = visibleSources.filter((source) => highlightedIds.has(source.sourceId)).length;
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
  });

  const persistContexts = (contexts: SavedContext[]) => {
    savedContexts = contexts;
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(contexts));
    }
  };

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
  const applyFacetColoringFromDrop = (event: DragEvent) => {
    const facetId = (draggingFacetId || event.dataTransfer?.getData('application/x-workbench-facet') || event.dataTransfer?.getData('text/plain')) as keyof FilterState;
    draggingFacetId = '';
    dragOverGrid = false;
    if (!facetId || !corpus.facets.some((facet) => facet.id === facetId)) return;
    colorFacetId = facetId;
    setStatus(`Card colour set by ${corpus.facets.find((facet) => facet.id === facetId)?.label ?? facetId}.`);
  };
  const dismissHighlighted = () => {
    const marked = visibleSources.filter((source) => highlightedIds.has(source.sourceId));
    if (!marked.length) return;
    dismissedIds = new Set([...dismissedIds, ...marked.map((source) => source.sourceId)]);
    highlightedIds = new Set([...highlightedIds].filter((sourceId) => !dismissedIds.has(sourceId)));
    setStatus(`Dismissed ${marked.length} marked card${marked.length === 1 ? '' : 's'}.`);
  };
  const keepHighlighted = () => {
    const marked = visibleSources.filter((source) => highlightedIds.has(source.sourceId));
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
    <aside class="left-rail">
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
              filters = { ...EMPTY_FILTERS };
              query = '';
              dismissedIds = new Set();
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

        {#each corpus.facets as facet}
          <div class="facet" role="group" aria-label={`Facet ${facet.label}`}>
            <h3
              draggable="true"
              class:colouring={colorFacetId === facet.id}
              title="Drag this facet name onto the card grid to colour cards by its values"
              on:dragstart={(event) => startFacetDrag(event, facet.id)}
              on:dragend={() => {
                draggingFacetId = '';
                dragOverGrid = false;
              }}
            >
              {facet.label}
            </h3>
            <div class="facet-values">
              {#each facet.values.slice(0, facet.id === 'topics' ? 18 : 12) as value}
                <button
                  type="button"
                  class:active={filterActive(facet.id, value.value)}
                  class="facet-chip"
                  aria-pressed={filterActive(facet.id, value.value) ? 'true' : 'false'}
                  on:click={() => (filters = toggleFilterValue(filters, facet.id, value.value))}
                >
                  <span>{value.value}</span>
                  <small>{value.count}</small>
                </button>
              {/each}
            </div>
          </div>
        {/each}
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
            {selectedIds.size} in context, {visibleHighlightedCount} marked in view
            {dismissedCount ? `, ${dismissedCount} dismissed` : ''}
            {colorFacet ? `, coloured by ${colorFacet.label}` : ''}
          </p>
        </div>
        <div class="toolbar-actions" aria-label="Marked-card actions">
          <button type="button" class="secondary" on:click={keepHighlighted} disabled={!visibleHighlightedCount}>Keep marked</button>
          <button type="button" class="secondary" on:click={dismissHighlighted} disabled={!visibleHighlightedCount}>Dismiss marked</button>
          <button type="button" class="secondary" on:click={() => (dismissedIds = new Set())} disabled={!dismissedCount}>Restore</button>
          <button type="button" class="secondary" on:click={() => (colorFacetId = '')} disabled={!colorFacet}>Clear colour</button>
        </div>
        <div class="segmented" aria-label="View mode">
          <button type="button" class:active={viewMode === 'grid'} aria-pressed={viewMode === 'grid' ? 'true' : 'false'} on:click={() => (viewMode = 'grid')}>Grid</button>
          <button type="button" class:active={viewMode === 'reader'} aria-pressed={viewMode === 'reader' ? 'true' : 'false'} on:click={() => (viewMode = 'reader')}>Reader</button>
          <button type="button" class:active={viewMode === 'graph'} aria-pressed={viewMode === 'graph' ? 'true' : 'false'} on:click={() => (viewMode = 'graph')}>Graph</button>
          <button type="button" class:active={viewMode === 'table'} aria-pressed={viewMode === 'table' ? 'true' : 'false'} on:click={() => (viewMode = 'table')}>Table</button>
          <button type="button" class:active={viewMode === 'queries'} aria-pressed={viewMode === 'queries' ? 'true' : 'false'} on:click={() => (viewMode = 'queries')}>Checks</button>
        </div>
      </div>

      {#if viewMode === 'grid'}
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
            if (draggingFacetId) dragOverGrid = true;
          }}
          on:dragover|preventDefault={() => {
            if (draggingFacetId) dragOverGrid = true;
          }}
          on:dragleave={() => {
            dragOverGrid = false;
          }}
          on:drop|preventDefault={applyFacetColoringFromDrop}
        >
          {#each visibleSources as source}
            {@const colourReason = colorReasonForSource(source, colorFacet)}
            <article
              class:selected={selectedIds.has(source.sourceId)}
              class:highlighted={highlightedIds.has(source.sourceId)}
              class="source-card"
              style={sourceCardStyle(source, colorFacet)}
              role="listitem"
              aria-label={`Source ${source.sourceId}`}
            >
              {#if source.thumbnailPath}
                <button type="button" class="thumbnail-button" on:click={() => openSource(source)} aria-label={`Open ${source.title}`}>
                  <img src={source.thumbnailPath} alt={`Thumbnail for ${source.title}`} loading="lazy" />
                </button>
              {/if}
              <div class="card-top">
                <span class="source-id">{source.sourceId}</span>
                <span class={`status status-${source.status.toLowerCase().replaceAll(' ', '-')}`}>{source.status}</span>
              </div>
              <h3>{source.title}</h3>
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
