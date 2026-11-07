// Recorded MongoDB index snapshot, transcribed from final_indexes.md.
// Run with mongosh against a local reproduction instance.
// This does not reconstruct undocumented historical index states or delete extra indexes.
// Default _id_ indexes are created by MongoDB, not explicitly duplicated here.
(() => {
  const benchmarkDb = db.getSiblingDB("proteomics_pattern1");
  const collections = ["datasets", "phosphopeptide_summaries", "samples"];
  const existing = benchmarkDb.getCollectionNames();
  for (const name of collections) {
    if (!existing.includes(name)) benchmarkDb.createCollection(name);
  }
  const definitions = [
  {
    "collection": "phosphopeptide_summaries",
    "key": {
      "geneSymbol": 1
    },
    "name": "geneSymbol_1"
  },
  {
    "collection": "phosphopeptide_summaries",
    "key": {
      "uniprotId": 1
    },
    "name": "uniprotId_1"
  },
  {
    "collection": "phosphopeptide_summaries",
    "key": {
      "insulinRegulationStatus": 1
    },
    "name": "insulinRegulationStatus_1"
  },
  {
    "collection": "phosphopeptide_summaries",
    "key": {
      "defectiveModelCount": 1
    },
    "name": "defectiveModelCount_1"
  },
  {
    "collection": "phosphopeptide_summaries",
    "key": {
      "emergentModelCount": 1
    },
    "name": "emergentModelCount_1"
  },
  {
    "collection": "phosphopeptide_summaries",
    "key": {
      "defects.DEX": 1
    },
    "name": "defects.DEX_1"
  },
  {
    "collection": "phosphopeptide_summaries",
    "key": {
      "emergent.DEX": 1
    },
    "name": "emergent.DEX_1"
  },
  {
    "collection": "samples",
    "key": {
      "sampleId": 1
    },
    "name": "sampleId_1"
  },
  {
    "collection": "samples",
    "key": {
      "datasetId": 1
    },
    "name": "datasetId_1"
  },
  {
    "collection": "samples",
    "key": {
      "condition.conditionId": 1
    },
    "name": "condition.conditionId_1"
  },
  {
    "collection": "samples",
    "key": {
      "condition.model": 1
    },
    "name": "condition.model_1"
  },
  {
    "collection": "samples",
    "key": {
      "totalProteomeMeasurements.geneSymbol": 1
    },
    "name": "totalProteomeMeasurements.geneSymbol_1"
  },
  {
    "collection": "samples",
    "key": {
      "totalProteomeMeasurements.uniprotId": 1
    },
    "name": "totalProteomeMeasurements.uniprotId_1"
  },
  {
    "collection": "samples",
    "key": {
      "totalProteomeMeasurements.proteinAnalyteId": 1
    },
    "name": "totalProteomeMeasurements.proteinAnalyteId_1"
  }
];
  for (const item of definitions) {
    benchmarkDb.getCollection(item.collection).createIndex(item.key, { name: item.name });
  }
  print("Recorded index definitions applied to " + benchmarkDb.getName());
})();
