<script lang="ts">
  import type { FilterState, WorkbenchCorpus } from '$lib/workbench/types';

  export let corpus: WorkbenchCorpus;
  export let filters: FilterState;
  export let query = '';
  export let toggleFilter: (key: keyof FilterState, value: string) => void = () => undefined;
  export let clearFilters: () => void = () => undefined;

  const active = (key: keyof FilterState, value: string) => filters[key].includes(value);
</script>

<section class="panel filter-panel" aria-label="Filters">
  <div class="panel-heading">
    <div>
      <h2>Explore</h2>
      <p>{corpus.sourceCount} sources</p>
    </div>
    <button type="button" class="icon-button" title="Clear filters" aria-label="Clear filters" on:click={clearFilters}>x</button>
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
            class:active={active(facet.id, value.value)}
            class="facet-chip"
            on:click={() => toggleFilter(facet.id, value.value)}
          >
            <span>{value.value}</span>
            <small>{value.count}</small>
          </button>
        {/each}
      </div>
    </div>
  {/each}
</section>
