-- Q8: PostgreSQL implementation from the final thesis Appendix A.
-- Query expressions match the supplied Q8.sql.
-- To measure execution, prepend EXPLAIN (ANALYZE, BUFFERS).

WITH selected_model_regulation AS (
  SELECT pr.phosphopeptide_id,
    pr.gene_symbol, pr.uniprot_id, pr.site, pr.multiplicity, pr.ptm_localisation,
    pr.insulin_regulation_status, pr.defective_model_count, pr.emergent_model_count,
    COALESCE(mr.defective, FALSE) AS is_defective, UPPER(
      COALESCE(mr.emergent_direction, 'FALSE')
    ) <> 'FALSE' AS is_emergent, mr.emergent_direction,
    COALESCE(pr.defective_model_count, 0)
      + COALESCE(pr.emergent_model_count, 0) AS total_dysregulated_model_count
  FROM "PhosphopeptideRegulation" pr
  JOIN "PhosphopeptideModelRegulation" mr ON mr.analyte = pr.analyte
  WHERE mr.model = 'DEX'
   AND (
     mr.defective IS TRUE
     OR UPPER(
       COALESCE(mr.emergent_direction, 'FALSE')
     ) <> 'FALSE'
   )
)
SELECT 'DEX'::text AS "selectedModel",
  'PS1'::text AS "datasetId", phosphopeptide_id AS "phosphopeptideId",
  gene_symbol AS "geneSymbol", uniprot_id AS "uniprotId", site AS "site",
  multiplicity AS "multiplicity", ptm_localisation AS "ptmLocalisation",
  insulin_regulation_status AS "insulinRegulationStatus", CASE
    WHEN is_defective AND is_emergent
      THEN 'defective_and_emergent'
    WHEN is_defective
      THEN 'defective'
    WHEN is_emergent
      THEN 'emergent'
    ELSE 'none'
  END AS "dysregulationType", CASE
    WHEN is_emergent THEN emergent_direction
    ELSE NULL
  END AS "emergentDirectionInSelectedModel",
  defective_model_count AS "defectiveModelCount",
  emergent_model_count AS "emergentModelCount", total_dysregulated_model_count
    AS "totalDysregulatedModelCount",
  gene_symbol || '_' || uniprot_id AS "linkedProteinAnalyteId"
FROM selected_model_regulation
ORDER BY total_dysregulated_model_count DESC,
  defective_model_count DESC NULLS LAST, emergent_model_count DESC NULLS LAST,
  gene_symbol COLLATE "C" ASC NULLS FIRST, site COLLATE "C" ASC NULLS FIRST,
  phosphopeptide_id COLLATE "C" ASC NULLS FIRST
LIMIT 50;
