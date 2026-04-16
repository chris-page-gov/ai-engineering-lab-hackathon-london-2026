<script lang="ts">
  import type { WorkbenchSource } from '$lib/workbench/types';

  export let source: WorkbenchSource;
  export let selected = false;
  export let highlighted = false;
  export let openSource: (source: WorkbenchSource) => void = () => undefined;
  export let selectSource: (source: WorkbenchSource) => void = () => undefined;
  export let highlightSource: (source: WorkbenchSource) => void = () => undefined;
</script>

<article class:selected class:highlighted class="source-card" aria-label={`Source ${source.sourceId}`}>
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
    <button type="button" class="secondary" on:click={() => highlightSource(source)}>
      {highlighted ? 'Unmark' : 'Mark'}
    </button>
    <button type="button" on:click={() => selectSource(source)}>
      {selected ? 'Remove' : 'Add'}
    </button>
  </div>
</article>
