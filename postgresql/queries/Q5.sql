-- Q5: PostgreSQL implementation from the final thesis Appendix A.
-- Query expressions match the supplied Q5.sql.
-- To measure execution, prepend EXPLAIN (ANALYZE, BUFFERS).

SELECT s.name AS "sampleId",
  d.name AS "datasetId", regexp_replace(
    s.name, '_[0-9]+$', ''
  ) AS "conditionId", split_part(
    s.name, '_', 1
  ) AS "model", 'INS' AS "insulinState", split_part(
    s.name, '_', 3
  )::integer AS "replicate", 'Akt1' AS "geneSymbol",
  deu.accession_id AS "uniprotId", 'Akt1_' || deu.accession_id
    AS "proteinAnalyteId",
  q.value AS "abundance", 'normalised_intensity' AS "unit"
FROM "DescriptorEntryUniProt" deu
JOIN "Analyte" a ON a.id = deu.analyte
JOIN "Quantification" q ON q.analyte = a.id
 AND q.dataset = a.dataset
JOIN "Sample" s ON s.id = q.sample
 AND s.dataset = q.dataset
JOIN "Dataset" d ON d.id = q.dataset
WHERE deu.accession_id = 'P31750'
  AND q.value IS NOT NULL
  AND (
     s.name LIKE 'CI_INS_%'
    OR s.name LIKE 'DEX_INS_%'
    OR s.name LIKE 'TNF_INS_%'
    OR s.name LIKE 'MPQ_INS_%'
    OR s.name LIKE 'AA_INS_%'
  )
ORDER BY "model",
  "replicate";
