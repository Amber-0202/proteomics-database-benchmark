-- Q3: PostgreSQL implementation from the final thesis Appendix A.
-- Query expressions match the supplied query3.sql.
-- To measure execution, prepend EXPLAIN (ANALYZE, BUFFERS).

SELECT gene_symbol AS "geneSymbol",
  COUNT(*) FILTER (
    WHERE insulin_regulation_status = 'defective'
  ) AS "defectiveSites", COUNT(*) FILTER (
    WHERE insulin_regulation_status = 'emergent'
  ) AS "emergentSites", COUNT(*) AS "totalDysregulatedSites"
FROM "PhosphopeptideRegulation"
WHERE insulin_regulation_status IN (
  'defective', 'emergent'
)
GROUP BY gene_symbol
ORDER BY "totalDysregulatedSites" DESC,
  gene_symbol COLLATE "C" ASC
LIMIT 20;
