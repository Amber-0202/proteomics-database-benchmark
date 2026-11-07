-- Q4: PostgreSQL implementation from the final thesis Appendix A.
-- Query expressions match the supplied Q4.sql.
-- To measure execution, prepend EXPLAIN (ANALYZE, BUFFERS).

WITH sample_context AS (
  SELECT s.id AS sample_pk,
    s.name AS sample_id, s.dataset, sg.name AS condition_id, MAX(
      CASE
        WHEN ec.variable = 1
        THEN ec.name
      END
    ) AS model, MAX(
      CASE
        WHEN ec.variable = 2
        THEN ec.name
      END
    ) AS insulin_state
  FROM "Sample" s
  JOIN "SampleGroup" sg ON sg.id = s."group"
  JOIN "GroupCondition" gc ON gc."group" = sg.id
  JOIN "ExperimentalCondition" ec ON ec.id = gc.condition
  WHERE s.dataset = 1
  GROUP BY s.id,
    s.name, s.dataset, sg.name
), akt1_measurements AS (
  SELECT q.dataset,
    q.sample, deu.accession_id AS uniprot_id
  FROM "Quantification" q
  JOIN "DescriptorEntryUniProt" deu ON deu.analyte = q.analyte
  WHERE q.dataset = 1
   AND EXISTS (
     SELECT 1
     FROM "UniProtGene" ug
     WHERE ug.uniprot_entry = deu.accession_id
      AND ug.gene_name = 'Akt1'
   )
)
SELECT CASE am.dataset
    WHEN 1 THEN 'TP1'
    WHEN 2 THEN 'PS1'
    ELSE am.dataset::text
  END AS "datasetId", 'Akt1' AS "geneSymbol", JSONB_AGG(
    DISTINCT am.uniprot_id
  ) AS "uniprotIds", JSONB_AGG(
    DISTINCT JSONB_BUILD_OBJECT(
      'conditionId', sc.condition_id, 'model', sc.model,
      'insulinState', sc.insulin_state
    )
  ) AS "conditions", COUNT(
    DISTINCT sc.sample_id
  ) AS "sampleCount"
FROM akt1_measurements am
JOIN sample_context sc ON sc.sample_pk = am.sample
GROUP BY am.dataset;
