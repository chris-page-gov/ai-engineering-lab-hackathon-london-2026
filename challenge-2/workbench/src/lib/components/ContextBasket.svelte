<script lang="ts">
  import type { WorkbenchSource } from '$lib/workbench/types';

  export let sources: WorkbenchSource[] = [];
  export let savedContexts: Array<{ name: string; sourceIds: string[] }> = [];
  export let contextName = '';
  export let changeName: (name: string) => void = () => undefined;
  export let removeSource: (source: WorkbenchSource) => void = () => undefined;
  export let clearContext: () => void = () => undefined;
  export let saveCurrentContext: () => void = () => undefined;
  export let openSavedContext: (name: string) => void = () => undefined;
</script>

<section class="panel context-panel" aria-label="Context set">
  <div class="panel-heading">
    <div>
      <h2>Context Set</h2>
      <p>{sources.length} selected</p>
    </div>
    <button type="button" class="icon-button" title="Clear context" aria-label="Clear context" on:click={clearContext}>x</button>
  </div>

  {#if sources.length === 0}
    <p class="muted">No sources selected. Browser AI export will use the current visible set.</p>
  {:else}
    <ul class="compact-list">
      {#each sources as source}
        <li>
          <span>{source.sourceId}</span>
          <button type="button" class="link-button" on:click={() => removeSource(source)}>Remove</button>
        </li>
      {/each}
    </ul>
  {/if}

  <div class="save-row">
    <input
      type="text"
      bind:value={contextName}
      placeholder="Context name"
      aria-label="Context name"
      on:input={() => changeName(contextName)}
    />
    <button type="button" class="secondary" on:click={saveCurrentContext} disabled={sources.length === 0 || !contextName.trim()}>
      Save
    </button>
  </div>

  {#if savedContexts.length}
    <h3>Saved</h3>
    <ul class="compact-list">
      {#each savedContexts as saved}
        <li>
          <span>{saved.name} ({saved.sourceIds.length})</span>
          <button type="button" class="link-button" on:click={() => openSavedContext(saved.name)}>Open</button>
        </li>
      {/each}
    </ul>
  {/if}
</section>
