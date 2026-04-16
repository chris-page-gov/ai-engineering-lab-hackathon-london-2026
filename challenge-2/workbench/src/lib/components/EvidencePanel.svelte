<script lang="ts">
  import type { WorkbenchSource } from '$lib/workbench/types';
  import { extractExcerpts } from '$lib/workbench/model';

  export let source: WorkbenchSource | null = null;
  export let query = '';
</script>

<section class="panel evidence-panel" aria-label="Evidence">
  <h2>Evidence</h2>
  {#if !source}
    <p class="muted">Open a source to inspect metadata, excerpts, provenance, and source links.</p>
  {:else}
    <div class="evidence-title">
      <span class="source-id">{source.sourceId}</span>
      <strong>{source.title}</strong>
    </div>
    <dl>
      <div><dt>Status</dt><dd>{source.status}</dd></div>
      <div><dt>Department</dt><dd>{source.department}</dd></div>
      <div><dt>Format</dt><dd>{source.format}</dd></div>
      <div><dt>Extraction</dt><dd>{source.extractionMethod} / {source.extractionQuality}</dd></div>
      <div><dt>Raw source</dt><dd><code>{source.sourcePath}</code></dd></div>
      <div><dt>Wiki note</dt><dd><code>{source.notePath}</code></dd></div>
    </dl>
    {#if source.flags.length}
      <h3>Flags</h3>
      <div class="chips">
        {#each source.flags as flag}
          <span class="chip warning">{flag}</span>
        {/each}
      </div>
    {/if}
    <h3>Excerpts</h3>
    {#each extractExcerpts(source, query) as excerpt}
      <blockquote>{excerpt}</blockquote>
    {/each}
  {/if}
</section>
