-- Q2: PostgreSQL implementation from the final thesis Appendix A.
-- Query expressions match the supplied query2.sql.
-- To measure execution, prepend EXPLAIN (ANALYZE, BUFFERS).

WITH defective_phosphopeptides AS (
  SELECT phosphopeptide_id,
    gene_symbol, uniprot_id, site, insulin_regulation_status, defective_model_count,
    linked_protein_analyte_id
  FROM "PhosphopeptideRegulation"
  WHERE insulin_regulation_status = 'defective'
  ORDER BY phosphopeptide_id COLLATE "C"
  LIMIT 5
), sample_context AS (
  SELECT s.id AS sample_pk,
    s.name AS sample_id, sg.name AS condition_id, MAX(
      CASE
        WHEN ec.variable = 1 THEN ec.name
      END
    ) AS model, MAX(
      CASE
        WHEN ec.variable = 2 THEN ec.name
      END
    ) AS insulin_state
  FROM "Sample" s
  JOIN "SampleGroup" sg ON sg.id = s."group"
  JOIN "GroupCondition" gc ON gc."group" = sg.id
  JOIN "ExperimentalCondition" ec ON ec.id = gc.condition
  WHERE s.dataset = 1
  GROUP BY s.id,
    s.name, sg.name
)
SELECT dp.phosphopeptide_id AS "phosphopeptideId",
  dp.gene_symbol AS "geneSymbol", dp.uniprot_id AS "uniprotId", dp.site AS "site",
  dp.insulin_regulation_status AS "insulinRegulationStatus",
  dp.defective_model_count AS "defectiveModelCount",
  dp.gene_symbol || '_' || dp.uniprot_id AS "linkedProteinAnalyteId", COALESCE(
    measurements.linked_measurements, '[]'::jsonb
  ) AS "linkedProteinMeasurements"
FROM defective_phosphopeptides dp
LEFT JOIN LATERAL (
  SELECT jsonb_agg(
      jsonb_build_object(
        'sampleId', x.sample_id, 'condition', jsonb_build_object(
          'conditionId', x.condition_id, 'model', x.model,
          'insulinState', x.insulin_state
        ), 'abundance', x.abundance
      )
      ORDER BY x.sample_id COLLATE "C"
    ) AS linked_measurements
  FROM (
    SELECT sc.sample_id,
      sc.condition_id, sc.model, sc.insulin_state, q.value AS abundance
    FROM "Quantification" q
    JOIN sample_context sc ON sc.sample_pk = q.sample
    WHERE q.dataset = 1
     AND q.analyte = dp.linked_protein_analyte_id
    ORDER BY sc.sample_id COLLATE "C"
    LIMIT 10
  ) x
) measurements ON TRUE
ORDER BY dp.phosphopeptide_id COLLATE "C";
