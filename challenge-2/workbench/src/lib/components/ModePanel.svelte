<script lang="ts">
  import type { ContextExport } from '$lib/workbench/types';

  export let mode: ContextExport['mode'] = 'no-ai';
  export let sourceCount = 0;
  export let changeMode: (mode: ContextExport['mode']) => void = () => undefined;
  export let copyJson: () => void = () => undefined;
  export let downloadJson: () => void = () => undefined;
  export let copyPrompt: () => void = () => undefined;
  export let downloadMarkdown: () => void = () => undefined;
  export let status = '';
</script>

<section class="panel mode-panel" aria-label="AI mode">
  <h2>AI Options</h2>
  <div class="segmented" role="tablist" aria-label="Workbench mode">
    <button type="button" class:active={mode === 'no-ai'} on:click={() => changeMode('no-ai')}>No AI</button>
    <button type="button" class:active={mode === 'browser-ai'} on:click={() => changeMode('browser-ai')}>Browser AI</button>
    <button type="button" class:active={mode === 'mcp'} on:click={() => changeMode('mcp')}>MCP</button>
  </div>

  {#if mode === 'no-ai'}
    <p class="muted">Use filters, saved checks, source notes, metadata, and evidence bundles without sending anything to an AI system.</p>
  {:else if mode === 'browser-ai'}
    <p class="muted">Export the current context for a browser AI. The export includes {sourceCount} source records and provenance.</p>
    <div class="button-grid">
      <button type="button" on:click={copyJson}>Copy JSON</button>
      <button type="button" class="secondary" on:click={downloadJson}>Download JSON</button>
      <button type="button" class="secondary" on:click={copyPrompt}>Copy Prompt</button>
      <button type="button" class="secondary" on:click={downloadMarkdown}>Evidence MD</button>
    </div>
  {:else}
    <p class="muted">Run the local MCP server to let desktop AI clients pull this corpus on demand.</p>
    <pre class="command">python3 challenge-2/tools/workbench_mcp.py</pre>
    <ul class="compact-list">
      <li>workbench.search_sources</li>
      <li>workbench.read_source</li>
      <li>workbench.build_context</li>
    </ul>
  {/if}

  {#if status}
    <p class="status-message" role="status">{status}</p>
  {/if}
</section>
