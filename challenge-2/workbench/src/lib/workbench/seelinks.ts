import type { FilterState, WorkbenchCollection, WorkbenchFacet, WorkbenchSource } from './types';

export type FacetHighlightState = Partial<Record<keyof FilterState, string[]>>;
export type FacetValueOrders = Partial<Record<keyof FilterState, string[]>>;
export type SortDirectionState = Partial<Record<keyof FilterState, boolean>>;
export type SortExclusionState = Partial<Record<keyof FilterState, string[]>>;
export type TileRollup = { facet: keyof FilterState; value: string };
export type TileRollupSummary = TileRollup & {
  key: string;
  count: number;
  total: number;
  fraction: number;
  sourceIds: string[];
};

export const facetValuesForSource = (source: WorkbenchSource, facetId: keyof FilterState): string[] => {
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

export const countFacetValues = (sources: WorkbenchSource[], facets: WorkbenchFacet[]) => {
  const counts: Partial<Record<keyof FilterState, Record<string, number>>> = {};
  for (const facet of facets) {
    const values: Record<string, number> = {};
    for (const source of sources) {
      for (const value of facetValuesForSource(source, facet.id)) {
        const key = value.trim() || 'Unknown';
        values[key] = (values[key] ?? 0) + 1;
      }
    }
    counts[facet.id] = values;
  }
  return counts;
};

export const orderedFacetValues = (
  facet: WorkbenchFacet,
  counts: Record<string, number>,
  customOrder?: string[],
  reversed = false
) => {
  const values = Object.keys(counts);
  const order = customOrder?.length
    ? [...customOrder.filter((value) => values.includes(value)), ...values.filter((value) => !customOrder.includes(value))]
    : values.sort((a, b) => counts[b] - counts[a] || a.localeCompare(b));
  const finalOrder = reversed ? [...order].reverse() : order;
  return finalOrder.map((value) => ({ value, count: counts[value] ?? 0, facet }));
};

export const pickFacetValue = (values: string[], order: string[]) => {
  if (!values.length) return '';
  return order.find((value) => values.includes(value)) ?? values[0];
};

export const sortSourcesByFacets = (
  sources: WorkbenchSource[],
  sortBy: Array<keyof FilterState>,
  facetOrders: FacetValueOrders = {},
  directions: SortDirectionState = {},
  exclusions: SortExclusionState = {}
) => {
  if (!sortBy.length) return sources;
  return [...sources].sort((a, b) => {
    for (const facet of sortBy) {
      const order = facetOrders[facet] ?? [];
      const aValue = pickFacetValue(facetValuesForSource(a, facet), order);
      const bValue = pickFacetValue(facetValuesForSource(b, facet), order);
      const excluded = new Set(exclusions[facet] ?? []);
      const aExcluded = excluded.has(aValue);
      const bExcluded = excluded.has(bValue);
      if (aExcluded !== bExcluded) return aExcluded ? 1 : -1;
      const aIndex = order.includes(aValue) ? order.indexOf(aValue) : Number.MAX_SAFE_INTEGER;
      const bIndex = order.includes(bValue) ? order.indexOf(bValue) : Number.MAX_SAFE_INTEGER;
      const cmp = aIndex !== bIndex ? aIndex - bIndex : aValue.localeCompare(bValue);
      if (cmp !== 0) return directions[facet] ? -cmp : cmp;
    }
    return a.title.localeCompare(b.title);
  });
};

export const applyFacetHighlights = (sources: WorkbenchSource[], highlights: FacetHighlightState) => {
  const active = Object.entries(highlights).filter(([, values]) => values?.length) as Array<[keyof FilterState, string[]]>;
  if (!active.length) return [];
  return sources.filter((source) =>
    active.every(([facet, values]) => {
      const sourceValues = facetValuesForSource(source, facet);
      return values.some((value) => sourceValues.includes(value));
    })
  );
};

export const buildHighlightFilters = (highlights: FacetHighlightState) =>
  Object.fromEntries(
    Object.entries(highlights)
      .filter(([, values]) => values?.length)
      .map(([facet, values]) => [facet, [...(values ?? [])].sort((a, b) => a.localeCompare(b))])
  );

export const buildLinkSummary = (sources: WorkbenchSource[], facets: WorkbenchFacet[], limit = 4) => {
  const counts = countFacetValues(sources, facets);
  return facets
    .filter((facet) => !facet.metadata)
    .map((facet) => ({
      facet,
      values: Object.entries(counts[facet.id] ?? {})
        .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
        .slice(0, limit)
        .map(([value, count]) => ({ value, count })),
    }))
    .filter((entry) => entry.values.length)
    .slice(0, 4);
};

export const buildCollectionProfile = (sources: WorkbenchSource[], facets: WorkbenchFacet[]) => buildLinkSummary(sources, facets, 8);

export const buildRollupSummaries = (sources: WorkbenchSource[], rollups: TileRollup[]): TileRollupSummary[] =>
  rollups.map((rollup) => {
    const matched = sources.filter((source) => facetValuesForSource(source, rollup.facet).includes(rollup.value));
    const key = `${rollup.facet}::${rollup.value}`;
    return {
      ...rollup,
      key,
      count: matched.length,
      total: sources.length,
      fraction: sources.length ? matched.length / sources.length : 0,
      sourceIds: matched.map((source) => source.sourceId),
    };
  });

export const mergeCollections = (base: WorkbenchCollection[] = [], stored: WorkbenchCollection[] = []) => {
  const map = new Map<string, WorkbenchCollection>();
  for (const collection of base) map.set(collection.name.toLowerCase(), collection);
  for (const collection of stored) map.set(collection.name.toLowerCase(), collection);
  return Array.from(map.values()).sort((a, b) => a.name.localeCompare(b.name));
};

export const fieldDisplayValue = (source: WorkbenchSource, field: string) => {
  if (field === 'sourceId') return source.sourceId;
  if (field === 'title') return source.title;
  if (field === 'department') return source.department;
  if (field === 'status') return source.status;
  if (field === 'format') return source.format;
  if (field === 'documentType') return source.documentType;
  if (field === 'categoryPath') return source.categoryPath ?? '';
  if (field === 'tileSubtitle') return source.tileSubtitle ?? '';
  if (field === 'summary') return source.summary;
  const prop = source.properties?.[field];
  if (Array.isArray(prop)) return prop.join(', ');
  return prop === null || prop === undefined ? '' : String(prop);
};
