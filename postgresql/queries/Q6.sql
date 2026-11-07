-- Q6: PostgreSQL implementation from the final thesis Appendix A.
-- Query expressions match the supplied Q6.sql.
-- To measure execution, prepend EXPLAIN (ANALYZE, BUFFERS).

WITH akt1_measurements AS (
  SELECT d.name AS dataset_id,
    split_part(
      s.name, '_', 1
    ) AS model, split_part(
      s.name, '_', 2
    ) AS insulin_state, q.value AS abundance
  FROM "DescriptorEntryUniProt" deu
  JOIN "Analyte" a ON a.id = deu.analyte
  JOIN "Quantification" q ON q.analyte = a.id
   AND q.dataset = a.dataset
  JOIN "Sample" s ON s.id = q.sample
   AND s.dataset = q.dataset
  JOIN "Dataset" d ON d.id = q.dataset
  WHERE deu.accession_id = 'P31750'
    AND q.value IS NOT NULL
    AND split_part(
      s.name, '_', 1
    ) IN (
      'CTRL', 'CI', 'DEX', 'TNF', 'MPQ', 'AA'
    )
    AND split_part(
      s.name, '_', 2
    ) IN (
      'BASAL', 'INS'
    )
)
SELECT dataset_id AS "datasetId",
  model AS "model", AVG(abundance)
    FILTER (
      WHERE insulin_state = 'BASAL'
    ) AS "basalMean",
  AVG(abundance)
    FILTER (
      WHERE insulin_state = 'INS'
    ) AS "insulinMean",
  COUNT(*)
    FILTER (
      WHERE insulin_state = 'BASAL'
    ) AS "basalN",
  COUNT(*)
    FILTER (
      WHERE insulin_state = 'INS'
    ) AS "insulinN",
  (
    AVG(abundance)
      FILTER (
        WHERE insulin_state = 'INS'
      )
    -
    AVG(abundance)
      FILTER (
        WHERE insulin_state = 'BASAL'
      )
  ) AS "insulinMinusBasal"
FROM akt1_measurements
GROUP BY dataset_id,
  model
HAVING
  COUNT(*)
    FILTER (
      WHERE insulin_state = 'BASAL'
    ) > 0
  AND
  COUNT(*)
    FILTER (
      WHERE insulin_state = 'INS'
    ) > 0
ORDER BY "insulinMinusBasal" DESC;
