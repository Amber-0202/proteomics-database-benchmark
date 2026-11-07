-- ProteHome PostgreSQL schema: prepared from the supplied PostgreSQL 18.6 schema-only export.
-- Original table and constraint expressions retained; ownership and psql dump wrappers omitted.
-- Run once in a new empty database; no DROP or data-modification statements are included.
-- Explicit performance indexes are in 02_indexes.sql.

BEGIN;

CREATE TABLE public."Analyte" (
    id bigint NOT NULL,
    dataset bigint
);

CREATE TABLE public."AnalyteDescriptor" (
    id bigint NOT NULL,
    dataset bigint,
    entry_relationship character varying(3),
    type character(2)
);

CREATE TABLE public."CellLine" (
    id bigint NOT NULL,
    name character varying(100)
);

CREATE TABLE public."ConditionBait" (
    condition bigint,
    dataset bigint,
    uniprot_id character varying(11),
    is_control boolean
);

CREATE TABLE public."ConditionCellType" (
    condition bigint,
    dataset bigint,
    cell_type character varying(50),
    atcc_number character varying(50),
    differentiation_status character varying(100),
    source character varying(8),
    mycoplasma_tested character(1),
    organism bigint
);

CREATE TABLE public."ConditionDiet" (
    condition bigint,
    dataset bigint,
    diet_type character varying(50),
    duration bigint
);

CREATE TABLE public."ConditionExercise" (
    condition bigint,
    dataset bigint,
    exercise_type character varying(2),
    duration bigint,
    duration_unit character varying(3)
);

CREATE TABLE public."ConditionKnockdown" (
    condition bigint,
    dataset bigint,
    gene_symbol character varying(50),
    knockdown_type character varying(20)
);

CREATE TABLE public."ConditionStimulus" (
    condition bigint,
    dataset bigint,
    chembl_id character varying(20),
    molecule_type character varying(20),
    molecule_name character varying(255),
    is_control boolean,
    dose double precision,
    dose_unit character varying(10),
    duration timestamp with time zone,
    duration_unit character varying(4)
);

CREATE TABLE public."ConditionTissue" (
    condition bigint,
    dataset bigint,
    tissue character varying(50),
    subtype character varying(50),
    taxonomy_id bigint,
    strain character varying(50)
);

CREATE TABLE public."ContrastGroup" (
    id bigint NOT NULL,
    de_test bigint,
    sample_group bigint,
    multiplier double precision
);

CREATE TABLE public."DEResult" (
    id bigint NOT NULL,
    contrast bigint,
    analyte bigint,
    test_statistic double precision,
    logfc double precision
);

CREATE TABLE public."DETest" (
    id bigint NOT NULL,
    root_node bigint,
    name text,
    type character(1)
);

CREATE TABLE public."DataSource" (
    id bigint NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    root_node bigint,
    dataset bigint,
    file bigint
);

CREATE TABLE public."Dataset" (
    id bigint NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    project_id bigint,
    name character varying(255),
    description text,
    structure_node bigint
);

CREATE TABLE public."DescriptorEntryPhosphosite" (
    id bigint NOT NULL,
    descriptor bigint,
    analyte bigint,
    accession_id character varying(11),
    variant smallint,
    residue bigint,
    entry_position integer,
    amino_acid character(1)
);

CREATE TABLE public."DescriptorEntryUniProt" (
    id bigint NOT NULL,
    descriptor bigint,
    analyte bigint,
    accession_id character varying(11),
    variant smallint,
    entry_position integer
);

CREATE TABLE public."ExperimentalCondition" (
    id bigint NOT NULL,
    name text,
    variable bigint
);

CREATE TABLE public."ExperimentalVariable" (
    id bigint NOT NULL,
    type character(2),
    divergence_node bigint
);

CREATE TABLE public."File" (
    id bigint NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    upload_record bigint,
    project_id bigint,
    permission_node bigint,
    filename text,
    path text,
    format character(3),
    type character(3),
    uuid uuid
);

CREATE TABLE public."GroupCondition" (
    "group" bigint,
    condition bigint
);

CREATE TABLE public."GroupMembership" (
    "user" bigint NOT NULL,
    "group" bigint NOT NULL,
    role character(2)
);

CREATE TABLE public."InvitationCode" (
    id bigint NOT NULL,
    code text,
    status text,
    used_by bigint
);

CREATE TABLE public."Molecule" (
    chembl_id text NOT NULL,
    type text
);

CREATE TABLE public."MoleculeName" (
    chembl_id text NOT NULL,
    name text NOT NULL,
    type text
);

CREATE TABLE public."Organism" (
    taxonomy_id bigint NOT NULL,
    scientific_name character varying(100),
    common_name character varying(100)
);

CREATE TABLE public."PValue" (
    adjustment_method character(2),
    value double precision,
    de_result bigint
);

CREATE TABLE public."Permission" (
    "group" bigint NOT NULL,
    node bigint NOT NULL,
    level character(2)
);

CREATE TABLE public."PermissionNode" (
    id bigint NOT NULL,
    parent bigint,
    type character(2),
    public_permission character(2)
);

CREATE TABLE public."PhosphopeptideModelRegulation" (
    analyte bigint NOT NULL,
    model character varying(3) NOT NULL,
    model_order smallint NOT NULL,
    defective boolean DEFAULT false NOT NULL,
    emergent_direction character varying(4),
    CONSTRAINT ck_ppmodelreg_emergent CHECK ((((emergent_direction)::text = ANY ((ARRAY['up'::character varying, 'down'::character varying])::text[])) OR (emergent_direction IS NULL))),
    CONSTRAINT ck_ppmodelreg_model CHECK (((model)::text = ANY ((ARRAY['CI'::character varying, 'DEX'::character varying, 'TNF'::character varying, 'MPQ'::character varying, 'AA'::character varying])::text[]))),
    CONSTRAINT ck_ppmodelreg_order CHECK (((model_order >= 1) AND (model_order <= 5)))
);

CREATE TABLE public."PhosphopeptideRegulation" (
    analyte bigint NOT NULL,
    phosphopeptide_id text NOT NULL,
    gene_symbol text,
    uniprot_id character varying(11) NOT NULL,
    site character varying(32) NOT NULL,
    insulin_regulation_status character varying(20),
    defective_model_count integer NOT NULL,
    emergent_model_count integer NOT NULL,
    linked_protein_analyte_id bigint,
    multiplicity smallint,
    ptm_localisation double precision,
    CONSTRAINT ck_phosphopeptideregulation_defectivecount CHECK (((defective_model_count >= 0) AND (defective_model_count <= 5))),
    CONSTRAINT ck_phosphopeptideregulation_emergentcount CHECK (((emergent_model_count >= 0) AND (emergent_model_count <= 5))),
    CONSTRAINT ck_phosphopeptideregulation_notboth CHECK ((NOT ((defective_model_count > 0) AND (emergent_model_count > 0)))),
    CONSTRAINT ck_phosphopeptideregulation_status CHECK ((((insulin_regulation_status)::text = ANY ((ARRAY['defective'::character varying, 'emergent'::character varying])::text[])) OR (insulin_regulation_status IS NULL)))
);

CREATE TABLE public."Phosphosite" (
    id bigint NOT NULL,
    accession_id character varying(11),
    uniprot_entry character varying(11),
    variant smallint,
    residue integer,
    amino_acid character(1),
    phosphosite_group bigint,
    human_analogue bigint,
    mod_rsd_type character(2)
);

CREATE TABLE public."PhosphositeGroup" (
    group_id bigint NOT NULL
);

CREATE TABLE public."Project" (
    id bigint NOT NULL,
    created_at date,
    updated_at date,
    name text,
    description text,
    date_from date,
    date_to date,
    permission_node bigint,
    creator bigint
);

CREATE TABLE public."Quantification" (
    id bigint NOT NULL,
    node bigint,
    analyte bigint,
    sample bigint,
    value double precision,
    dataset bigint
);

CREATE TABLE public."Sample" (
    id bigint NOT NULL,
    name text,
    batch integer,
    dataset bigint,
    "group" bigint
);

CREATE TABLE public."SampleGroup" (
    id bigint NOT NULL,
    name text
);

CREATE TABLE public."UniProtAccession" (
    id character varying(11) NOT NULL,
    current_entry character varying(11)
);

CREATE TABLE public."UniProtEntry" (
    accession_id character varying(11) NOT NULL,
    name text,
    organism bigint,
    human_entry character varying(11)
);

CREATE TABLE public."UniProtGene" (
    uniprot_entry character varying(11),
    gene_name text,
    type character(1)
);

CREATE TABLE public."UniprotAlternativeName" (
    uniprot_entry character varying(11),
    alternative_name text
);

CREATE TABLE public."UploadRecord" (
    id bigint NOT NULL,
    uploader bigint,
    project bigint,
    upload_date timestamp without time zone,
    status text,
    comment text
);

CREATE TABLE public."User" (
    id bigint NOT NULL,
    password text NOT NULL,
    username text NOT NULL,
    first_name text NOT NULL,
    last_name text NOT NULL,
    email text NOT NULL,
    is_staff boolean,
    is_active boolean,
    is_superuser boolean,
    date_joined timestamp without time zone
);

CREATE TABLE public."UserGroup" (
    id bigint NOT NULL,
    name text,
    is_user boolean,
    date_created timestamp without time zone
);

CREATE TABLE public."WorkflowNode" (
    id bigint NOT NULL,
    type character(3),
    is_saved boolean
);

ALTER TABLE ONLY public."AnalyteDescriptor"
    ADD CONSTRAINT "AnalyteDescriptor_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."Analyte"
    ADD CONSTRAINT "Analyte_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."CellLine"
    ADD CONSTRAINT "CellLine_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."ContrastGroup"
    ADD CONSTRAINT "ContrastGroup_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."DEResult"
    ADD CONSTRAINT "DEResult_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."DETest"
    ADD CONSTRAINT "DETest_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."DataSource"
    ADD CONSTRAINT "DataSource_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."Dataset"
    ADD CONSTRAINT "Dataset_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."DescriptorEntryPhosphosite"
    ADD CONSTRAINT "DescriptorEntryPhosphosite_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."DescriptorEntryUniProt"
    ADD CONSTRAINT "DescriptorEntryUniProt_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."ExperimentalCondition"
    ADD CONSTRAINT "ExperimentalCondition_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."ExperimentalVariable"
    ADD CONSTRAINT "ExperimentalVariable_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."File"
    ADD CONSTRAINT "File_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."InvitationCode"
    ADD CONSTRAINT "InvitationCode_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."Molecule"
    ADD CONSTRAINT "Molecule_pkey" PRIMARY KEY (chembl_id);

ALTER TABLE ONLY public."Organism"
    ADD CONSTRAINT "Organism_pkey" PRIMARY KEY (taxonomy_id);

ALTER TABLE ONLY public."PermissionNode"
    ADD CONSTRAINT "PermissionNode_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."PhosphopeptideModelRegulation"
    ADD CONSTRAINT "PhosphopeptideModelRegulation_pkey" PRIMARY KEY (analyte, model);

ALTER TABLE ONLY public."PhosphopeptideRegulation"
    ADD CONSTRAINT "PhosphopeptideRegulation_phosphopeptide_id_key" UNIQUE (phosphopeptide_id);

ALTER TABLE ONLY public."PhosphopeptideRegulation"
    ADD CONSTRAINT "PhosphopeptideRegulation_pkey" PRIMARY KEY (analyte);

ALTER TABLE ONLY public."PhosphositeGroup"
    ADD CONSTRAINT "PhosphositeGroup_pkey" PRIMARY KEY (group_id);

ALTER TABLE ONLY public."Phosphosite"
    ADD CONSTRAINT "Phosphosite_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."Project"
    ADD CONSTRAINT "Project_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."Quantification"
    ADD CONSTRAINT "Quantification_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."SampleGroup"
    ADD CONSTRAINT "SampleGroup_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."Sample"
    ADD CONSTRAINT "Sample_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."UniProtAccession"
    ADD CONSTRAINT "UniProtAccession_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."UniProtEntry"
    ADD CONSTRAINT "UniProtEntry_pkey" PRIMARY KEY (accession_id);

ALTER TABLE ONLY public."UploadRecord"
    ADD CONSTRAINT "UploadRecord_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."UserGroup"
    ADD CONSTRAINT "UserGroup_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."WorkflowNode"
    ADD CONSTRAINT "WorkflowNode_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public."GroupMembership"
    ADD CONSTRAINT pk_groupmembership PRIMARY KEY ("user", "group");

ALTER TABLE ONLY public."MoleculeName"
    ADD CONSTRAINT pk_moleculename PRIMARY KEY (name, chembl_id);

ALTER TABLE ONLY public."Permission"
    ADD CONSTRAINT pk_permission PRIMARY KEY ("group", node);

ALTER TABLE ONLY public."DEResult"
    ADD CONSTRAINT uq_deresult_test_analyte UNIQUE (contrast, analyte);

ALTER TABLE ONLY public."Phosphosite"
    ADD CONSTRAINT uq_phosphosite_accession_residue UNIQUE (accession_id, residue);

ALTER TABLE ONLY public."Analyte"
    ADD CONSTRAINT fk_analyte_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);

ALTER TABLE ONLY public."AnalyteDescriptor"
    ADD CONSTRAINT fk_analytedescriptor_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);

ALTER TABLE ONLY public."ConditionBait"
    ADD CONSTRAINT fk_conditionbait_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);

ALTER TABLE ONLY public."ConditionBait"
    ADD CONSTRAINT fk_conditionbait_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);

ALTER TABLE ONLY public."ConditionCellType"
    ADD CONSTRAINT fk_conditioncelltype_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);

ALTER TABLE ONLY public."ConditionCellType"
    ADD CONSTRAINT fk_conditioncelltype_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);

ALTER TABLE ONLY public."ConditionCellType"
    ADD CONSTRAINT fk_conditioncelltype_organism FOREIGN KEY (organism) REFERENCES public."Organism"(taxonomy_id);

ALTER TABLE ONLY public."ConditionDiet"
    ADD CONSTRAINT fk_conditiondiet_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);

ALTER TABLE ONLY public."ConditionDiet"
    ADD CONSTRAINT fk_conditiondiet_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);

ALTER TABLE ONLY public."ConditionExercise"
    ADD CONSTRAINT fk_conditionexercise_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);

ALTER TABLE ONLY public."ConditionExercise"
    ADD CONSTRAINT fk_conditionexercise_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);

ALTER TABLE ONLY public."ConditionKnockdown"
    ADD CONSTRAINT fk_conditionknockdown_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);

ALTER TABLE ONLY public."ConditionKnockdown"
    ADD CONSTRAINT fk_conditionknockdown_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);

ALTER TABLE ONLY public."ConditionStimulus"
    ADD CONSTRAINT fk_conditionstimulus_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);

ALTER TABLE ONLY public."ConditionStimulus"
    ADD CONSTRAINT fk_conditionstimulus_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);

ALTER TABLE ONLY public."ConditionTissue"
    ADD CONSTRAINT fk_conditiontissue_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);

ALTER TABLE ONLY public."ConditionTissue"
    ADD CONSTRAINT fk_conditiontissue_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);

ALTER TABLE ONLY public."ConditionTissue"
    ADD CONSTRAINT fk_conditiontissue_organism FOREIGN KEY (taxonomy_id) REFERENCES public."Organism"(taxonomy_id);

ALTER TABLE ONLY public."ContrastGroup"
    ADD CONSTRAINT fk_contrastgroup_detest FOREIGN KEY (de_test) REFERENCES public."DETest"(id);

ALTER TABLE ONLY public."ContrastGroup"
    ADD CONSTRAINT fk_contrastgroup_samplegroup FOREIGN KEY (sample_group) REFERENCES public."SampleGroup"(id);

ALTER TABLE ONLY public."Dataset"
    ADD CONSTRAINT fk_dataset_project FOREIGN KEY (project_id) REFERENCES public."Project"(id);

ALTER TABLE ONLY public."Dataset"
    ADD CONSTRAINT fk_dataset_structurenode FOREIGN KEY (structure_node) REFERENCES public."WorkflowNode"(id);

ALTER TABLE ONLY public."DataSource"
    ADD CONSTRAINT fk_datasource_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);

ALTER TABLE ONLY public."DataSource"
    ADD CONSTRAINT fk_datasource_file FOREIGN KEY (file) REFERENCES public."File"(id);

ALTER TABLE ONLY public."DataSource"
    ADD CONSTRAINT fk_datasource_rootnode FOREIGN KEY (root_node) REFERENCES public."WorkflowNode"(id);

ALTER TABLE ONLY public."DEResult"
    ADD CONSTRAINT fk_deresult_analyte FOREIGN KEY (analyte) REFERENCES public."Analyte"(id);

ALTER TABLE ONLY public."DEResult"
    ADD CONSTRAINT fk_deresult_detest FOREIGN KEY (contrast) REFERENCES public."DETest"(id);

ALTER TABLE ONLY public."DescriptorEntryPhosphosite"
    ADD CONSTRAINT fk_descriptorentryphosphosite_analyte FOREIGN KEY (analyte) REFERENCES public."Analyte"(id);

ALTER TABLE ONLY public."DescriptorEntryPhosphosite"
    ADD CONSTRAINT fk_descriptorentryphosphosite_descriptor FOREIGN KEY (descriptor) REFERENCES public."AnalyteDescriptor"(id);

ALTER TABLE ONLY public."DescriptorEntryUniProt"
    ADD CONSTRAINT fk_descriptorentryuniprot_analyte FOREIGN KEY (analyte) REFERENCES public."Analyte"(id);

ALTER TABLE ONLY public."DescriptorEntryUniProt"
    ADD CONSTRAINT fk_descriptorentryuniprot_descriptor FOREIGN KEY (descriptor) REFERENCES public."AnalyteDescriptor"(id);

ALTER TABLE ONLY public."DETest"
    ADD CONSTRAINT fk_detest_rootnode FOREIGN KEY (root_node) REFERENCES public."WorkflowNode"(id);

ALTER TABLE ONLY public."ExperimentalCondition"
    ADD CONSTRAINT fk_experimentalcondition_variable FOREIGN KEY (variable) REFERENCES public."ExperimentalVariable"(id);

ALTER TABLE ONLY public."ExperimentalVariable"
    ADD CONSTRAINT fk_experimentalvariable_divergencenode FOREIGN KEY (divergence_node) REFERENCES public."WorkflowNode"(id);

ALTER TABLE ONLY public."File"
    ADD CONSTRAINT fk_file_permissionnode FOREIGN KEY (permission_node) REFERENCES public."PermissionNode"(id);

ALTER TABLE ONLY public."File"
    ADD CONSTRAINT fk_file_project FOREIGN KEY (project_id) REFERENCES public."Project"(id);

ALTER TABLE ONLY public."File"
    ADD CONSTRAINT fk_file_uploadrecord FOREIGN KEY (upload_record) REFERENCES public."UploadRecord"(id);

ALTER TABLE ONLY public."GroupCondition"
    ADD CONSTRAINT fk_groupcondition_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);

ALTER TABLE ONLY public."GroupCondition"
    ADD CONSTRAINT fk_groupcondition_group FOREIGN KEY ("group") REFERENCES public."SampleGroup"(id);

ALTER TABLE ONLY public."GroupMembership"
    ADD CONSTRAINT fk_groupmembership_group FOREIGN KEY ("group") REFERENCES public."UserGroup"(id);

ALTER TABLE ONLY public."GroupMembership"
    ADD CONSTRAINT fk_groupmembership_user FOREIGN KEY ("user") REFERENCES public."User"(id);

ALTER TABLE ONLY public."InvitationCode"
    ADD CONSTRAINT fk_invitationcode_user FOREIGN KEY (used_by) REFERENCES public."User"(id);

ALTER TABLE ONLY public."MoleculeName"
    ADD CONSTRAINT fk_moleculename_molecule FOREIGN KEY (chembl_id) REFERENCES public."Molecule"(chembl_id);

ALTER TABLE ONLY public."Permission"
    ADD CONSTRAINT fk_permission_group FOREIGN KEY ("group") REFERENCES public."UserGroup"(id);

ALTER TABLE ONLY public."Permission"
    ADD CONSTRAINT fk_permission_node FOREIGN KEY (node) REFERENCES public."PermissionNode"(id);

ALTER TABLE ONLY public."PermissionNode"
    ADD CONSTRAINT fk_permissionnode_parent FOREIGN KEY (parent) REFERENCES public."PermissionNode"(id);

ALTER TABLE ONLY public."PhosphopeptideRegulation"
    ADD CONSTRAINT fk_phosphopeptideregulation_analyte FOREIGN KEY (analyte) REFERENCES public."Analyte"(id);

ALTER TABLE ONLY public."PhosphopeptideRegulation"
    ADD CONSTRAINT fk_phosphopeptideregulation_linkedprotein FOREIGN KEY (linked_protein_analyte_id) REFERENCES public."Analyte"(id);

ALTER TABLE ONLY public."Phosphosite"
    ADD CONSTRAINT fk_phosphosite_group FOREIGN KEY (phosphosite_group) REFERENCES public."PhosphositeGroup"(group_id);

ALTER TABLE ONLY public."Phosphosite"
    ADD CONSTRAINT fk_phosphosite_humananalogue FOREIGN KEY (human_analogue) REFERENCES public."Phosphosite"(id);

ALTER TABLE ONLY public."Phosphosite"
    ADD CONSTRAINT fk_phosphosite_uniprotentry FOREIGN KEY (uniprot_entry) REFERENCES public."UniProtEntry"(accession_id);

ALTER TABLE ONLY public."PhosphopeptideModelRegulation"
    ADD CONSTRAINT fk_ppmodelreg_analyte FOREIGN KEY (analyte) REFERENCES public."Analyte"(id);

ALTER TABLE ONLY public."Project"
    ADD CONSTRAINT fk_project_creator FOREIGN KEY (creator) REFERENCES public."User"(id);

ALTER TABLE ONLY public."Project"
    ADD CONSTRAINT fk_project_permissionnode FOREIGN KEY (permission_node) REFERENCES public."PermissionNode"(id);

ALTER TABLE ONLY public."PValue"
    ADD CONSTRAINT fk_pvalue_deresult FOREIGN KEY (de_result) REFERENCES public."DEResult"(id);

ALTER TABLE ONLY public."Quantification"
    ADD CONSTRAINT fk_quantification_analyte FOREIGN KEY (analyte) REFERENCES public."Analyte"(id);

ALTER TABLE ONLY public."Quantification"
    ADD CONSTRAINT fk_quantification_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);

ALTER TABLE ONLY public."Quantification"
    ADD CONSTRAINT fk_quantification_node FOREIGN KEY (node) REFERENCES public."WorkflowNode"(id);

ALTER TABLE ONLY public."Quantification"
    ADD CONSTRAINT fk_quantification_sample FOREIGN KEY (sample) REFERENCES public."Sample"(id);

ALTER TABLE ONLY public."Sample"
    ADD CONSTRAINT fk_sample_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);

ALTER TABLE ONLY public."Sample"
    ADD CONSTRAINT fk_sample_group FOREIGN KEY ("group") REFERENCES public."SampleGroup"(id);

ALTER TABLE ONLY public."UniProtAccession"
    ADD CONSTRAINT fk_uniprotaccession_currententry FOREIGN KEY (current_entry) REFERENCES public."UniProtEntry"(accession_id);

ALTER TABLE ONLY public."UniprotAlternativeName"
    ADD CONSTRAINT fk_uniprotalternativename_entry FOREIGN KEY (uniprot_entry) REFERENCES public."UniProtEntry"(accession_id);

ALTER TABLE ONLY public."UniProtEntry"
    ADD CONSTRAINT fk_uniprotentry_humanentry FOREIGN KEY (human_entry) REFERENCES public."UniProtEntry"(accession_id);

ALTER TABLE ONLY public."UniProtEntry"
    ADD CONSTRAINT fk_uniprotentry_organism FOREIGN KEY (organism) REFERENCES public."Organism"(taxonomy_id);

ALTER TABLE ONLY public."UniProtGene"
    ADD CONSTRAINT fk_uniprotgene_entry FOREIGN KEY (uniprot_entry) REFERENCES public."UniProtEntry"(accession_id);

ALTER TABLE ONLY public."UploadRecord"
    ADD CONSTRAINT fk_uploadrecord_project FOREIGN KEY (project) REFERENCES public."Project"(id);

ALTER TABLE ONLY public."UploadRecord"
    ADD CONSTRAINT fk_uploadrecord_uploader FOREIGN KEY (uploader) REFERENCES public."User"(id);

COMMIT;
