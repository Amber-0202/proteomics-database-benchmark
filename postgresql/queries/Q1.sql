-- Q1: PostgreSQL implementation from the final thesis Appendix A.
-- Query expressions match the supplied query1.sql.
-- To measure execution, prepend EXPLAIN (ANALYZE, BUFFERS).

WITH analyte_identity AS (
  SELECT a.id AS analyte_id,
    deu.accession_id AS uniprot_id, COALESCE(
      MIN(NULLIF(ug.gene_name, '')), deu.accession_id
    ) AS gene_or_protein
  FROM "Analyte" a
  JOIN "DescriptorEntryUniProt" deu ON deu.analyte = a.id
  LEFT JOIN "UniProtGene" ug ON ug.uniprot_entry = deu.accession_id
  WHERE a.dataset = 1   -- TP1 only
  GROUP BY a.id,
    deu.accession_id
), sample_condition AS (
  SELECT s.id AS sample_id,
    sg.name AS condition_id, MAX(
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
  WHERE s.dataset = 1   -- TP1 only
  GROUP BY s.id,
    sg.name
)
SELECT sc.condition_id,
  sc.model, sc.insulin_state, ai.gene_or_protein, ai.uniprot_id,
  AVG(q.value) AS average_abundance, COUNT(*) AS measurement_count
FROM "Quantification" q
JOIN sample_condition sc ON sc.sample_id = q.sample
JOIN analyte_identity ai ON ai.analyte_id = q.analyte
WHERE q.dataset = 1
GROUP BY sc.condition_id,
  sc.model, sc.insulin_state, ai.gene_or_protein, ai.uniprot_id
ORDER BY ai.gene_or_protein ASC,
  sc.condition_id ASC
LIMIT 10;
