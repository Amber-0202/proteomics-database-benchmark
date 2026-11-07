-- Q7: PostgreSQL implementation from the final thesis Appendix A.
-- Query expressions match the supplied Q7.sql.
-- To measure execution, prepend EXPLAIN (ANALYZE, BUFFERS).

SELECT 'PS1' AS "datasetId",
  pr.phosphopeptide_id AS "phosphopeptideId", pr.gene_symbol AS "geneSymbol",
  pr.uniprot_id AS "uniprotId", pr.site AS "site", pr.multiplicity
    AS "multiplicity",
  pr.ptm_localisation AS "ptmLocalisation", COALESCE(
    pr.insulin_regulation_status, 'normal_or_unclassified'
  ) AS "insulinRegulationStatus", pr.defective_model_count AS "defectiveModelCount",
  pr.emergent_model_count AS "emergentModelCount", model_info."defectiveModels",
  model_info."emergentModels", pr.gene_symbol
    || '_'
    || pr.uniprot_id AS "linkedProteinAnalyteId"
FROM "PhosphopeptideRegulation" pr
LEFT JOIN LATERAL (
  SELECT COALESCE(
      JSONB_AGG(
        mr.model
        ORDER BY mr.model_order
      ) FILTER (
        WHERE mr.defective = TRUE
      ), '[]'::jsonb
    ) AS "defectiveModels", COALESCE(
      JSONB_AGG(
        JSONB_BUILD_OBJECT(
          'model', mr.model, 'direction', mr.emergent_direction
        )
        ORDER BY mr.model_order
      ) FILTER (
        WHERE mr.emergent_direction IS NOT NULL
      ), '[]'::jsonb
    ) AS "emergentModels"
  FROM "PhosphopeptideModelRegulation" mr
  WHERE mr.analyte = pr.analyte
) model_info
  ON TRUE
WHERE pr.gene_symbol = 'Pcm1'
ORDER BY pr.defective_model_count DESC,
  pr.emergent_model_count DESC, pr.site ASC, pr.multiplicity ASC;
