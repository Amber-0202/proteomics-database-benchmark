// Read-only commands equivalent to the count checks documented in Appendix D.4.
// Values below are historical reference counts, NOT results of a new run.
// This script prints current observations when a user executes it.
// It does not perform field-by-field comparison or validate all query outputs.
(() => {
  const sourceDb = db.getSiblingDB("proteomics_pattern1");
  const targetDb = db.getSiblingDB("proteomics_pattern2");
  const sampleId = "CTRL_BASAL_1";
  const totals = sourceDb.getCollection("samples").aggregate([
    { $unwind: "$totalProteomeMeasurements" },
    { $count: "totalMeasurements" }
  ]).toArray();
  const sourceTotal = totals.length ? Number(totals[0].totalMeasurements) : 0;
  const targetTotal = Number(targetDb.getCollection("protein_measurements").countDocuments({}));
  const sampleRows = sourceDb.getCollection("samples").aggregate([
    { $match: { sampleId: sampleId } },
    { $project: { _id: 0, sampleId: 1, measurementCount: { $size: "$totalProteomeMeasurements" } } }
  ]).toArray();
  const sourceSample = sampleRows.length === 1 ? Number(sampleRows[0].measurementCount) : null;
  const targetSample = Number(targetDb.getCollection("protein_measurements").countDocuments({ sampleId: sampleId }));
  const checks = [
    {
      check: "Total protein measurements", p1: sourceTotal, p2: targetTotal,
      recordedReference: 304911,
      countsAgree: sourceTotal === targetTotal,
      matchesRecordedReference: sourceTotal === 304911 && targetTotal === 304911
    },
    {
      check: sampleId, p1: sourceSample, p2: targetSample,
      sourceSampleDocuments: sampleRows.length, recordedReference: 6376,
      countsAgree: sourceSample !== null && sourceSample === targetSample,
      matchesRecordedReference: sourceSample === 6376 && targetSample === 6376
    }
  ];
  const passed = checks.every(x => x.countsAgree && x.matchesRecordedReference);
  printjson({ checkType: "counts_only", passed: passed, checks: checks });
  if (!passed) throw new Error("Migration count checks do not match the recorded prototype. Inspect the printed observations.");
})();
