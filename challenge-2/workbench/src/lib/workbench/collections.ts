import Dexie, { type Table } from 'dexie';
import type { WorkbenchCollection } from './types';

type StoredCollection = WorkbenchCollection & { packKey: string };

class WorkbenchDb extends Dexie {
  collections!: Table<StoredCollection, string>;

  constructor() {
    super('dark-data-workbench');
    this.version(1).stores({
      collections: '&id, packKey, name',
    });
  }
}

const hasIndexedDb = typeof indexedDB !== 'undefined';
const db = hasIndexedDb ? new WorkbenchDb() : null;

export async function loadCollections(packKey: string): Promise<WorkbenchCollection[]> {
  if (!db) return [];
  const rows = await db.collections.where('packKey').equals(packKey).toArray();
  return rows.map(({ packKey: _packKey, ...collection }) => collection);
}

export async function saveCollection(packKey: string, collection: WorkbenchCollection): Promise<void> {
  if (!db) return;
  await db.transaction('rw', db.collections, async () => {
    const duplicateKeys = await db.collections
      .where('packKey')
      .equals(packKey)
      .filter((row) => row.name.toLowerCase() === collection.name.toLowerCase())
      .primaryKeys();
    if (duplicateKeys.length) await db.collections.bulkDelete(duplicateKeys as string[]);
    await db.collections.put({ ...collection, packKey });
  });
}
