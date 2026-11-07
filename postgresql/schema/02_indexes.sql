-- Twenty explicit indexes from the supplied schema export, in their original order.
-- Primary-key and unique-constraint indexes are already created by 01_schema.sql.

BEGIN;

CREATE INDEX idx_contrastgroup_detest ON public."ContrastGroup" USING btree (de_test);
CREATE INDEX idx_contrastgroup_samplegroup ON public."ContrastGroup" USING btree (sample_group);
CREATE INDEX idx_deresult_analyte ON public."DEResult" USING btree (analyte);
CREATE INDEX idx_descriptorentryphosphosite_accession_residue ON public."DescriptorEntryPhosphosite" USING btree (accession_id, residue);
CREATE INDEX idx_descriptorentryphosphosite_analyte ON public."DescriptorEntryPhosphosite" USING btree (analyte);
CREATE INDEX idx_descriptorentryuniprot_accession ON public."DescriptorEntryUniProt" USING btree (accession_id);
CREATE INDEX idx_descriptorentryuniprot_analyte ON public."DescriptorEntryUniProt" USING btree (analyte);
CREATE INDEX idx_experimentalcondition_variable ON public."ExperimentalCondition" USING btree (variable);
CREATE INDEX idx_groupcondition_condition ON public."GroupCondition" USING btree (condition);
CREATE INDEX idx_groupcondition_group ON public."GroupCondition" USING btree ("group");
CREATE INDEX idx_ppreg_gene_symbol ON public."PhosphopeptideRegulation" USING btree (gene_symbol);
CREATE INDEX idx_pvalue_deresult ON public."PValue" USING btree (de_result);
CREATE INDEX idx_pvalue_method ON public."PValue" USING btree (adjustment_method);
CREATE INDEX idx_quantification_analyte ON public."Quantification" USING btree (analyte);
CREATE INDEX idx_quantification_dataset_analyte ON public."Quantification" USING btree (dataset, analyte);
CREATE INDEX idx_quantification_dataset_sample ON public."Quantification" USING btree (dataset, sample);
CREATE INDEX idx_quantification_sample ON public."Quantification" USING btree (sample);
CREATE INDEX idx_sample_dataset_group ON public."Sample" USING btree (dataset, "group");
CREATE INDEX idx_uniprotgene_entry ON public."UniProtGene" USING btree (uniprot_entry);
CREATE INDEX idx_uniprotgene_gene ON public."UniProtGene" USING btree (gene_name);

COMMIT;
