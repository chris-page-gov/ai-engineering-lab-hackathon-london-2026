const escapeHtml = (value: string) =>
  value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');

const stripPreviewPreamble = (value: string) =>
  value
    .replace(/^\s*(?:<!--[\s\S]*?-->\s*)+/, '')
    .replace(/^\s*---\s*[\s\S]*?\n---\s*/, '')
    .trim();

const normalizeLocalAssetHref = (href: string) => {
  const trimmed = href.trim();
  if (/^[a-z][a-z0-9+.-]*:/i.test(trimmed) || trimmed.startsWith('//')) return trimmed;
  const normalized = trimmed.replaceAll('\\', '/');
  const assetIndex = normalized.indexOf('assets/');
  return assetIndex >= 0 ? `/api/narrative-asset/${normalized.slice(assetIndex)}` : trimmed;
};

const safeHref = (href: string) => {
  const trimmed = normalizeLocalAssetHref(href);
  if (!trimmed || trimmed.startsWith('//') || /[\u0000-\u001F\s]/.test(trimmed)) return null;
  const protocol = trimmed.match(/^([a-z][a-z0-9+.-]*):/i)?.[1].toLowerCase();
  if (protocol && !['http', 'https', 'mailto'].includes(protocol)) return null;
  return trimmed;
};

const isBlockStart = (line: string) =>
  /^(#{1,6})\s+/.test(line) ||
  /^```/.test(line) ||
  /^\s*[-*]\s+/.test(line) ||
  /^\s*\d+\.\s+/.test(line) ||
  /^\s*>\s?/.test(line) ||
  /^\s*\|/.test(line) ||
  /^-{3,}\s*$/.test(line);

const withInlineFormatting = (text: string) => {
  const codeSpans: string[] = [];
  const protectedText = text.replace(/`([^`]+)`/g, (_, code: string) => {
    const token = `@@CODE${codeSpans.length}@@`;
    codeSpans.push(`<code>${escapeHtml(code)}</code>`);
    return token;
  });
  const linkPattern = /(!?)\[([^\]\n]+)\]\(([^)\n]+)\)/g;
  let output = '';
  let cursor = 0;
  for (const match of protectedText.matchAll(linkPattern)) {
    output += formatTextSpan(protectedText.slice(cursor, match.index), codeSpans);
    const href = safeHref(match[3]);
    if (!href) {
      output += formatTextSpan(match[2], codeSpans);
    } else if (match[1] === '!') {
      output += `<img src="${escapeHtml(href)}" alt="${escapeHtml(match[2])}" loading="lazy">`;
    } else {
      output += `<a href="${escapeHtml(href)}" target="_blank" rel="noreferrer">${formatTextSpan(match[2], codeSpans)}</a>`;
    }
    cursor = (match.index ?? 0) + match[0].length;
  }
  output += formatTextSpan(protectedText.slice(cursor), codeSpans);
  return output;
};

const formatTextSpan = (text: string, codeSpans: string[]) => {
  let formatted = escapeHtml(text)
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\*([^*]+)\*/g, '<em>$1</em>');
  codeSpans.forEach((span, index) => {
    formatted = formatted.replaceAll(`@@CODE${index}@@`, span);
  });
  return formatted;
};

const tableCells = (line: string) =>
  line
    .trim()
    .replace(/^\|/, '')
    .replace(/\|$/, '')
    .split('|')
    .map((cell) => cell.trim());

const renderTable = (lines: string[]) => {
  const hasHeader = lines.length > 1 && /^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/.test(lines[1]);
  const header = hasHeader ? tableCells(lines[0]) : [];
  const rows = lines.slice(hasHeader ? 2 : 0).map(tableCells);
  return [
    '<div class="markdown-table-wrap"><table>',
    header.length ? `<thead><tr>${header.map((cell) => `<th>${withInlineFormatting(cell)}</th>`).join('')}</tr></thead>` : '',
    `<tbody>${rows
      .map((row) => `<tr>${row.map((cell) => `<td>${withInlineFormatting(cell)}</td>`).join('')}</tr>`)
      .join('')}</tbody>`,
    '</table></div>',
  ].join('');
};

export const renderMarkdownPreview = (value: string) => {
  const lines = stripPreviewPreamble(value).split(/\r?\n/);
  const blocks: string[] = [];
  let index = 0;

  while (index < lines.length) {
    const line = lines[index];
    const trimmed = line.trim();
    if (!trimmed) {
      index += 1;
      continue;
    }

    const fence = trimmed.match(/^```([A-Za-z0-9_-]+)?/);
    if (fence) {
      const codeLines: string[] = [];
      index += 1;
      while (index < lines.length && !lines[index].trim().startsWith('```')) {
        codeLines.push(lines[index]);
        index += 1;
      }
      if (index < lines.length) index += 1;
      const language = fence[1] ? ` class="language-${escapeHtml(fence[1])}"` : '';
      blocks.push(`<pre><code${language}>${escapeHtml(codeLines.join('\n'))}</code></pre>`);
      continue;
    }

    const heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      const level = heading[1].length;
      blocks.push(`<h${level}>${withInlineFormatting(heading[2].trim())}</h${level}>`);
      index += 1;
      continue;
    }

    if (/^-{3,}\s*$/.test(trimmed)) {
      blocks.push('<hr>');
      index += 1;
      continue;
    }

    if (/^\s*\|/.test(line)) {
      const tableLines: string[] = [];
      while (index < lines.length && /^\s*\|/.test(lines[index])) {
        tableLines.push(lines[index]);
        index += 1;
      }
      blocks.push(renderTable(tableLines));
      continue;
    }

    if (/^\s*[-*]\s+/.test(line)) {
      const items: string[] = [];
      while (index < lines.length && /^\s*[-*]\s+/.test(lines[index])) {
        items.push(lines[index].replace(/^\s*[-*]\s+/, '').trim());
        index += 1;
      }
      blocks.push(`<ul>${items.map((item) => `<li>${withInlineFormatting(item)}</li>`).join('')}</ul>`);
      continue;
    }

    if (/^\s*\d+\.\s+/.test(line)) {
      const items: string[] = [];
      while (index < lines.length && /^\s*\d+\.\s+/.test(lines[index])) {
        items.push(lines[index].replace(/^\s*\d+\.\s+/, '').trim());
        index += 1;
      }
      blocks.push(`<ol>${items.map((item) => `<li>${withInlineFormatting(item)}</li>`).join('')}</ol>`);
      continue;
    }

    if (/^\s*>\s?/.test(line)) {
      const quoteLines: string[] = [];
      while (index < lines.length && /^\s*>\s?/.test(lines[index])) {
        quoteLines.push(lines[index].replace(/^\s*>\s?/, '').trim());
        index += 1;
      }
      blocks.push(`<blockquote>${withInlineFormatting(quoteLines.join(' '))}</blockquote>`);
      continue;
    }

    const paragraphLines: string[] = [];
    while (index < lines.length && lines[index].trim() && !isBlockStart(lines[index])) {
      paragraphLines.push(lines[index].trim());
      index += 1;
    }
    blocks.push(`<p>${withInlineFormatting(paragraphLines.join(' '))}</p>`);
  }

  return blocks.join('\n') || '<p class="muted">No Markdown content available.</p>';
};
