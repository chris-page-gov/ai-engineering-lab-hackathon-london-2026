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
  import { EMPTY_FILTERS, type ContextExport, type FilterState, type WorkbenchCorpus, type WorkbenchSource } from '$lib/workbench/types';
  import type { PageData } from './$types';

  export let data: PageData;

  type ViewMode = 'grid' | 'reader' | 'graph' | 'table' | 'queries';
  type SavedContext = { name: string; sourceIds: string[] };

  const STORAGE_KEY = 'dark-data-workbench-contexts';

  let corpus: WorkbenchCorpus = data.corpus;
  let filters: FilterState = { ...EMPTY_FILTERS };
  let query = '';
  let viewMode: ViewMode = 'grid';
  let aiMode: ContextExport['mode'] = 'no-ai';
  let selectedIds = new Set<string>();
  let highlightedIds = new Set<string>();
  let activeSourceId = corpus.sources[0]?.sourceId ?? '';
  let savedContexts: SavedContext[] = [];
  let contextName = '';
  let exportStatus = '';
  let savedQueryId = SAVED_QUERIES[0].id;
  let savedQueryResults: WorkbenchSource[] = runSavedQuery(corpus, savedQueryId);
  let hydrated = false;

  $: visibleSources = filterSources(corpus.sources, filters, query);
  $: selectedSources = corpus.sources.filter((source) => selectedIds.has(source.sourceId));
  $: activeSource =
    corpus.sources.find((source) => source.sourceId === activeSourceId) ?? visibleSources[0] ?? corpus.sources[0] ?? null;
  $: contextExport = buildContextExport({
    corpus,
    visibleSources,
    selectedIds,
    highlightedIds,
    filters,
    query,
    mode: aiMode,
  });
  $: contextSourceCount = contextExport.sources.length;
  $: graphTopics = corpus.topics.slice(0, 8);
  $: workbookSources = corpus.sources.filter((source) => source.format === 'xlsx');

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
</script>

<svelte:head>
  <title>Dark Data Workbench</title>
</svelte:head>

<main class="workbench-shell">
  <header class="topbar">
    <div>
      <p class="eyebrow">Challenge 2</p>
      <h1>Dark Data Workbench</h1>
      <p>Build an auditable source context, browse it without AI, or export it for browser AI and MCP clients.</p>
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
            <h3>{facet.label}</h3>
            <div class="facet-values">
              {#each facet.values.slice(0, facet.id === 'topics' ? 18 : 12) as value}
                <button
                  type="button"
                  class:active={filterActive(facet.id, value.value)}
                  class="facet-chip"
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
      <div class="stage-toolbar">
        <div>
          <h2>{visibleSources.length} visible sources</h2>
          <p>{selectedIds.size} in context, {highlightedIds.size} marked</p>
        </div>
        <div class="segmented" aria-label="View mode">
          <button type="button" class:active={viewMode === 'grid'} on:click={() => (viewMode = 'grid')}>Grid</button>
          <button type="button" class:active={viewMode === 'reader'} on:click={() => (viewMode = 'reader')}>Reader</button>
          <button type="button" class:active={viewMode === 'graph'} on:click={() => (viewMode = 'graph')}>Graph</button>
          <button type="button" class:active={viewMode === 'table'} on:click={() => (viewMode = 'table')}>Table</button>
          <button type="button" class:active={viewMode === 'queries'} on:click={() => (viewMode = 'queries')}>Checks</button>
        </div>
      </div>

      {#if viewMode === 'grid'}
        <div class="source-grid">
          {#each visibleSources as source}
            <article
              class:selected={selectedIds.has(source.sourceId)}
              class:highlighted={highlightedIds.has(source.sourceId)}
              class="source-card"
              aria-label={`Source ${source.sourceId}`}
            >
              <div class="card-top">
                <span class="source-id">{source.sourceId}</span>
                <span class={`status status-${source.status.toLowerCase().replaceAll(' ', '-')}`}>{source.status}</span>
              </div>
              <h3>{source.title}</h3>
              <p>{source.summary}</p>
              <div class="meta-line">
                <span>{source.department}</span>
                <span>{source.format}</span>
                <span>{source.extractionQuality}</span>
              </div>
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
                <a href={`../${activeSource.notePath}`} target="_blank" rel="noreferrer">Open note</a>
              </div>
            </div>
            <div class="metadata-table">
              <div><strong>Status</strong><span>{activeSource.status}</span></div>
              <div><strong>Department</strong><span>{activeSource.department}</span></div>
              <div><strong>Format</strong><span>{activeSource.format}</span></div>
              <div><strong>Raw source</strong><code>{activeSource.sourcePath}</code></div>
              <div><strong>Wiki note</strong><code>{activeSource.notePath}</code></div>
            </div>
            <pre class="note-reader">{activeSource.noteText}</pre>
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
                  <button type="button" class:active={savedQueryId === saved.id} on:click={() => runQuery(saved.id)}>
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
