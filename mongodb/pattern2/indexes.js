// Recorded MongoDB index snapshot, transcribed from final_indexes.md.
// Run with mongosh against a local reproduction instance.
// This does not reconstruct undocumented historical index states or delete extra indexes.
// Default _id_ indexes are created by MongoDB, not explicitly duplicated here.
(() => {
  const benchmarkDb = db.getSiblingDB("proteomics_pattern2");
  const collections = ["datasets", "phosphopeptide_summaries", "protein_measurements", "samples"];
  const existing = benchmarkDb.getCollectionNames();
  for (const name of collections) {
    if (!existing.includes(name)) benchmarkDb.createCollection(name);
  }
  const definitions = [
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
      "geneSymbol": 1
    },
    "name": "geneSymbol_1"
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
    "collection": "protein_measurements",
    "key": {
      "geneSymbol": 1
    },
    "name": "geneSymbol_1"
  },
  {
    "collection": "protein_measurements",
    "key": {
      "proteinAnalyteId": 1
    },
    "name": "proteinAnalyteId_1"
  },
  {
    "collection": "protein_measurements",
    "key": {
      "condition.conditionId": 1,
      "condition.model": 1,
      "condition.insulinState": 1,
      "geneSymbol": 1,
      "uniprotId": 1,
      "abundance": 1
    },
    "name": "condition.conditionId_1_condition.model_1_condition.insulinState_1_geneSymbol_1_uniprotId_1_abundance_1"
  }
];
  for (const item of definitions) {
    benchmarkDb.getCollection(item.collection).createIndex(item.key, { name: item.name });
  }
  print("Recorded index definitions applied to " + benchmarkDb.getName());
})();
