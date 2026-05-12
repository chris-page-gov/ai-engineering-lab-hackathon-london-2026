import { describe, expect, it } from 'vitest';
import { renderMarkdownPreview } from './markdown';

describe('markdown preview rendering', () => {
  it('renders common Markdown blocks after hiding source frontmatter', () => {
    const html = renderMarkdownPreview(`<!-- generated -->
---
source_id: DOC-TEST
---
# Test Note

## Summary

- **First** point
- Second \`point\`

| Field | Value |
| --- | --- |
| Source ID | DOC-TEST |
`);

    expect(html).not.toContain('source_id: DOC-TEST');
    expect(html).toContain('<h1>Test Note</h1>');
    expect(html).toContain('<strong>First</strong>');
    expect(html).toContain('<code>point</code>');
    expect(html).toContain('<table>');
    expect(html).toContain('<th>Field</th>');
  });

  it('normalizes local narrative asset image links for the workbench route', () => {
    const html = renderMarkdownPreview('![Slide](../../assets/visuals/demo/slide-01.jpg)');

    expect(html).toContain('src="/api/narrative-asset/assets/visuals/demo/slide-01.jpg"');
    expect(html).toContain('alt="Slide"');
  });

  it('escapes source HTML and refuses unsafe Markdown links', () => {
    const html = renderMarkdownPreview('## Safe\n\n<script>alert(1)</script>\n\n[bad](javascript:alert(1)) [good](https://example.com)');

    expect(html).toContain('&lt;script&gt;alert(1)&lt;/script&gt;');
    expect(html).not.toContain('<script>');
    expect(html).not.toContain('javascript:alert');
    expect(html).toContain('href="https://example.com"');
  });
});
