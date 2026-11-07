// Equivalent reconstruction, NOT the recovered historical migration script.
// Source: the supplied migration record, Section 6, and thesis Appendix D.3.
// The packaging below adds source/empty-target checks and script-file execution.
// It writes P2; use a separate reconstruction instance, not the populated benchmark instance.
// No source documents, databases or existing target documents are deleted.
(() => {
  const sourceName = "proteomics_pattern1";
  const targetName = "proteomics_pattern2";
  if (sourceName === targetName) throw new Error("Source and target databases must differ.");
  const sourceDb = db.getSiblingDB(sourceName);
  const targetDb = db.getSiblingDB(targetName);
  const required = ["datasets", "samples", "phosphopeptide_summaries"];
  const sourceCollections = sourceDb.getCollectionNames();
  for (const name of required) {
    if (!sourceCollections.includes(name) || sourceDb.getCollection(name).countDocuments({}) === 0) {
      throw new Error("Missing or empty P1 source collection: " + name);
    }
  }
  const sampleCount = sourceDb.getCollection("samples").countDocuments({});
  const arraySampleCount = sourceDb.getCollection("samples").countDocuments({
    totalProteomeMeasurements: { $type: "array" }
  });
  if (sampleCount !== arraySampleCount) {
    throw new Error("Every source sample must contain a totalProteomeMeasurements array.");
  }
  // Preflight before the first write. Empty collections created by index setup are allowed.
  for (const name of targetDb.getCollectionNames()) {
    if (targetDb.getCollection(name).countDocuments({}) > 0) {
      throw new Error("Target is populated; migration refused: " + targetName + "." + name);
    }
  }
  const steps = [
  {
    "sourceCollection": "datasets",
    "pipeline": [
      {
        "$merge": {
          "into": {
            "db": "proteomics_pattern2",
            "coll": "datasets"
          },
          "on": "_id",
          "whenMatched": "replace",
          "whenNotMatched": "insert"
        }
      }
    ]
  },
  {
    "sourceCollection": "phosphopeptide_summaries",
    "pipeline": [
      {
        "$merge": {
          "into": {
            "db": "proteomics_pattern2",
            "coll": "phosphopeptide_summaries"
          },
          "on": "_id",
          "whenMatched": "replace",
          "whenNotMatched": "insert"
        }
      }
    ]
  },
  {
    "sourceCollection": "samples",
    "pipeline": [
      {
        "$project": {
          "totalProteomeMeasurements": 0
        }
      },
      {
        "$merge": {
          "into": {
            "db": "proteomics_pattern2",
            "coll": "samples"
          },
          "on": "_id",
          "whenMatched": "replace",
          "whenNotMatched": "insert"
        }
      }
    ]
  },
  {
    "sourceCollection": "samples",
    "pipeline": [
      {
        "$unwind": {
          "path": "$totalProteomeMeasurements",
          "includeArrayIndex": "measurementIndex"
        }
      },
      {
        "$project": {
          "_id": {
            "$concat": [
              {
                "$toString": "$_id"
              },
              "_",
              {
                "$toString": "$measurementIndex"
              }
            ]
          },
          "sampleObjectId": "$_id",
          "sampleId": 1,
          "datasetId": 1,
          "condition": 1,
          "assayType": "$sampleMetadata.assayType",
          "omicsLayer": "$sampleMetadata.omicsLayer",
          "proteinAnalyteId": "$totalProteomeMeasurements.proteinAnalyteId",
          "geneSymbol": "$totalProteomeMeasurements.geneSymbol",
          "uniprotId": "$totalProteomeMeasurements.uniprotId",
          "abundance": "$totalProteomeMeasurements.abundance",
          "unit": "$totalProteomeMeasurements.unit",
          "missing": "$totalProteomeMeasurements.missing"
        }
      },
      {
        "$merge": {
          "into": {
            "db": "proteomics_pattern2",
            "coll": "protein_measurements"
          },
          "on": "_id",
          "whenMatched": "replace",
          "whenNotMatched": "insert"
        }
      }
    ]
  }
];
  for (const step of steps) {
    // Default target equals the appendix; this assignment also keeps edits to targetName consistent.
    step.pipeline[step.pipeline.length - 1].$merge.into.db = targetName;
    sourceDb.getCollection(step.sourceCollection).aggregate(step.pipeline).toArray();
    print("Completed: " + step.sourceCollection + " -> " + step.pipeline[step.pipeline.length - 1].$merge.into.coll);
  }
  print("Reconstructed transformation completed. Run check_migration_counts.js, then apply the recorded P2 indexes.");
})();
