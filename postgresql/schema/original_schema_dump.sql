--
-- PostgreSQL database dump
--

\restrict iwohjfvOV4OQPerJLl6I9cnWKpNRJHw5pOSXHcCx28uKN1ZATFIRAFNjUANUp3L

-- Dumped from database version 18.6
-- Dumped by pg_dump version 18.6

-- Started on 2026-10-27 23:31:49 AEDT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 233 (class 1259 OID 16572)
-- Name: Analyte; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Analyte" (
    id bigint NOT NULL,
    dataset bigint
);


ALTER TABLE public."Analyte" OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 16583)
-- Name: AnalyteDescriptor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."AnalyteDescriptor" (
    id bigint NOT NULL,
    dataset bigint,
    entry_relationship character varying(3),
    type character(2)
);


ALTER TABLE public."AnalyteDescriptor" OWNER TO postgres;

--
-- TOC entry 248 (class 1259 OID 16765)
-- Name: CellLine; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."CellLine" (
    id bigint NOT NULL,
    name character varying(100)
);


ALTER TABLE public."CellLine" OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 16670)
-- Name: ConditionBait; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ConditionBait" (
    condition bigint,
    dataset bigint,
    uniprot_id character varying(11),
    is_control boolean
);


ALTER TABLE public."ConditionBait" OWNER TO postgres;

--
-- TOC entry 243 (class 1259 OID 16690)
-- Name: ConditionCellType; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public."ConditionCellType" OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 16721)
-- Name: ConditionDiet; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ConditionDiet" (
    condition bigint,
    dataset bigint,
    diet_type character varying(50),
    duration bigint
);


ALTER TABLE public."ConditionDiet" OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 16734)
-- Name: ConditionExercise; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ConditionExercise" (
    condition bigint,
    dataset bigint,
    exercise_type character varying(2),
    duration bigint,
    duration_unit character varying(3)
);


ALTER TABLE public."ConditionExercise" OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 16708)
-- Name: ConditionKnockdown; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ConditionKnockdown" (
    condition bigint,
    dataset bigint,
    gene_symbol character varying(50),
    knockdown_type character varying(20)
);


ALTER TABLE public."ConditionKnockdown" OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 16657)
-- Name: ConditionStimulus; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public."ConditionStimulus" OWNER TO postgres;

--
-- TOC entry 247 (class 1259 OID 16747)
-- Name: ConditionTissue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ConditionTissue" (
    condition bigint,
    dataset bigint,
    tissue character varying(50),
    subtype character varying(50),
    taxonomy_id bigint,
    strain character varying(50)
);


ALTER TABLE public."ConditionTissue" OWNER TO postgres;

--
-- TOC entry 251 (class 1259 OID 16810)
-- Name: ContrastGroup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ContrastGroup" (
    id bigint NOT NULL,
    de_test bigint,
    sample_group bigint,
    multiplier double precision
);


ALTER TABLE public."ContrastGroup" OWNER TO postgres;

--
-- TOC entry 252 (class 1259 OID 16826)
-- Name: DEResult; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."DEResult" (
    id bigint NOT NULL,
    contrast bigint,
    analyte bigint,
    test_statistic double precision,
    logfc double precision
);


ALTER TABLE public."DEResult" OWNER TO postgres;

--
-- TOC entry 250 (class 1259 OID 16797)
-- Name: DETest; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."DETest" (
    id bigint NOT NULL,
    root_node bigint,
    name text,
    type character(1)
);


ALTER TABLE public."DETest" OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 16551)
-- Name: DataSource; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."DataSource" (
    id bigint NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    root_node bigint,
    dataset bigint,
    file bigint
);


ALTER TABLE public."DataSource" OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16492)
-- Name: Dataset; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Dataset" (
    id bigint NOT NULL,
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    project_id bigint,
    name character varying(255),
    description text,
    structure_node bigint
);


ALTER TABLE public."Dataset" OWNER TO postgres;

--
-- TOC entry 261 (class 1259 OID 16944)
-- Name: DescriptorEntryPhosphosite; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public."DescriptorEntryPhosphosite" OWNER TO postgres;

--
-- TOC entry 258 (class 1259 OID 16899)
-- Name: DescriptorEntryUniProt; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."DescriptorEntryUniProt" (
    id bigint NOT NULL,
    descriptor bigint,
    analyte bigint,
    accession_id character varying(11),
    variant smallint,
    entry_position integer
);


ALTER TABLE public."DescriptorEntryUniProt" OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 16605)
-- Name: ExperimentalCondition; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ExperimentalCondition" (
    id bigint NOT NULL,
    name text,
    variable bigint
);


ALTER TABLE public."ExperimentalCondition" OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 16594)
-- Name: ExperimentalVariable; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."ExperimentalVariable" (
    id bigint NOT NULL,
    type character(2),
    divergence_node bigint
);


ALTER TABLE public."ExperimentalVariable" OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 16528)
-- Name: File; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public."File" OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 16626)
-- Name: GroupCondition; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."GroupCondition" (
    "group" bigint,
    condition bigint
);


ALTER TABLE public."GroupCondition" OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 16423)
-- Name: GroupMembership; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."GroupMembership" (
    "user" bigint NOT NULL,
    "group" bigint NOT NULL,
    role character(2)
);


ALTER TABLE public."GroupMembership" OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 16397)
-- Name: InvitationCode; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."InvitationCode" (
    id bigint NOT NULL,
    code text,
    status text,
    used_by bigint
);


ALTER TABLE public."InvitationCode" OWNER TO postgres;

--
-- TOC entry 262 (class 1259 OID 16960)
-- Name: Molecule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Molecule" (
    chembl_id text NOT NULL,
    type text
);


ALTER TABLE public."Molecule" OWNER TO postgres;

--
-- TOC entry 263 (class 1259 OID 16968)
-- Name: MoleculeName; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."MoleculeName" (
    chembl_id text NOT NULL,
    name text NOT NULL,
    type text
);


ALTER TABLE public."MoleculeName" OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 16683)
-- Name: Organism; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Organism" (
    taxonomy_id bigint NOT NULL,
    scientific_name character varying(100),
    common_name character varying(100)
);


ALTER TABLE public."Organism" OWNER TO postgres;

--
-- TOC entry 253 (class 1259 OID 16842)
-- Name: PValue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PValue" (
    adjustment_method character(2),
    value double precision,
    de_result bigint
);


ALTER TABLE public."PValue" OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 16451)
-- Name: Permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Permission" (
    "group" bigint NOT NULL,
    node bigint NOT NULL,
    level character(2)
);


ALTER TABLE public."Permission" OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16440)
-- Name: PermissionNode; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PermissionNode" (
    id bigint NOT NULL,
    parent bigint,
    type character(2),
    public_permission character(2)
);


ALTER TABLE public."PermissionNode" OWNER TO postgres;

--
-- TOC entry 265 (class 1259 OID 17038)
-- Name: PhosphopeptideModelRegulation; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public."PhosphopeptideModelRegulation" OWNER TO postgres;

--
-- TOC entry 264 (class 1259 OID 17008)
-- Name: PhosphopeptideRegulation; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public."PhosphopeptideRegulation" OWNER TO postgres;

--
-- TOC entry 260 (class 1259 OID 16921)
-- Name: Phosphosite; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public."Phosphosite" OWNER TO postgres;

--
-- TOC entry 259 (class 1259 OID 16915)
-- Name: PhosphositeGroup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."PhosphositeGroup" (
    group_id bigint NOT NULL
);


ALTER TABLE public."PhosphositeGroup" OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16468)
-- Name: Project; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public."Project" OWNER TO postgres;

--
-- TOC entry 249 (class 1259 OID 16771)
-- Name: Quantification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Quantification" (
    id bigint NOT NULL,
    node bigint,
    analyte bigint,
    sample bigint,
    value double precision,
    dataset bigint
);


ALTER TABLE public."Quantification" OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 16639)
-- Name: Sample; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."Sample" (
    id bigint NOT NULL,
    name text,
    batch integer,
    dataset bigint,
    "group" bigint
);


ALTER TABLE public."Sample" OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 16618)
-- Name: SampleGroup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."SampleGroup" (
    id bigint NOT NULL,
    name text
);


ALTER TABLE public."SampleGroup" OWNER TO postgres;

--
-- TOC entry 257 (class 1259 OID 16888)
-- Name: UniProtAccession; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."UniProtAccession" (
    id character varying(11) NOT NULL,
    current_entry character varying(11)
);


ALTER TABLE public."UniProtAccession" OWNER TO postgres;

--
-- TOC entry 254 (class 1259 OID 16850)
-- Name: UniProtEntry; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."UniProtEntry" (
    accession_id character varying(11) NOT NULL,
    name text,
    organism bigint,
    human_entry character varying(11)
);


ALTER TABLE public."UniProtEntry" OWNER TO postgres;

--
-- TOC entry 255 (class 1259 OID 16868)
-- Name: UniProtGene; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."UniProtGene" (
    uniprot_entry character varying(11),
    gene_name text,
    type character(1)
);


ALTER TABLE public."UniProtGene" OWNER TO postgres;

--
-- TOC entry 256 (class 1259 OID 16878)
-- Name: UniprotAlternativeName; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."UniprotAlternativeName" (
    uniprot_entry character varying(11),
    alternative_name text
);


ALTER TABLE public."UniprotAlternativeName" OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 16510)
-- Name: UploadRecord; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."UploadRecord" (
    id bigint NOT NULL,
    uploader bigint,
    project bigint,
    upload_date timestamp without time zone,
    status text,
    comment text
);


ALTER TABLE public."UploadRecord" OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16389)
-- Name: User; Type: TABLE; Schema: public; Owner: postgres
--

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


ALTER TABLE public."User" OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16410)
-- Name: UserGroup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."UserGroup" (
    id bigint NOT NULL,
    name text,
    is_user boolean,
    date_created timestamp without time zone
);


ALTER TABLE public."UserGroup" OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 16486)
-- Name: WorkflowNode; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."WorkflowNode" (
    id bigint NOT NULL,
    type character(3),
    is_saved boolean
);


ALTER TABLE public."WorkflowNode" OWNER TO postgres;

--
-- TOC entry 3882 (class 2606 OID 16588)
-- Name: AnalyteDescriptor AnalyteDescriptor_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AnalyteDescriptor"
    ADD CONSTRAINT "AnalyteDescriptor_pkey" PRIMARY KEY (id);


--
-- TOC entry 3880 (class 2606 OID 16577)
-- Name: Analyte Analyte_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Analyte"
    ADD CONSTRAINT "Analyte_pkey" PRIMARY KEY (id);


--
-- TOC entry 3898 (class 2606 OID 16770)
-- Name: CellLine CellLine_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."CellLine"
    ADD CONSTRAINT "CellLine_pkey" PRIMARY KEY (id);


--
-- TOC entry 3908 (class 2606 OID 16815)
-- Name: ContrastGroup ContrastGroup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ContrastGroup"
    ADD CONSTRAINT "ContrastGroup_pkey" PRIMARY KEY (id);


--
-- TOC entry 3912 (class 2606 OID 16831)
-- Name: DEResult DEResult_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DEResult"
    ADD CONSTRAINT "DEResult_pkey" PRIMARY KEY (id);


--
-- TOC entry 3906 (class 2606 OID 16804)
-- Name: DETest DETest_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DETest"
    ADD CONSTRAINT "DETest_pkey" PRIMARY KEY (id);


--
-- TOC entry 3878 (class 2606 OID 16556)
-- Name: DataSource DataSource_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DataSource"
    ADD CONSTRAINT "DataSource_pkey" PRIMARY KEY (id);


--
-- TOC entry 3872 (class 2606 OID 16499)
-- Name: Dataset Dataset_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Dataset"
    ADD CONSTRAINT "Dataset_pkey" PRIMARY KEY (id);


--
-- TOC entry 3935 (class 2606 OID 16949)
-- Name: DescriptorEntryPhosphosite DescriptorEntryPhosphosite_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DescriptorEntryPhosphosite"
    ADD CONSTRAINT "DescriptorEntryPhosphosite_pkey" PRIMARY KEY (id);


--
-- TOC entry 3925 (class 2606 OID 16904)
-- Name: DescriptorEntryUniProt DescriptorEntryUniProt_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DescriptorEntryUniProt"
    ADD CONSTRAINT "DescriptorEntryUniProt_pkey" PRIMARY KEY (id);


--
-- TOC entry 3886 (class 2606 OID 16612)
-- Name: ExperimentalCondition ExperimentalCondition_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ExperimentalCondition"
    ADD CONSTRAINT "ExperimentalCondition_pkey" PRIMARY KEY (id);


--
-- TOC entry 3884 (class 2606 OID 16599)
-- Name: ExperimentalVariable ExperimentalVariable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ExperimentalVariable"
    ADD CONSTRAINT "ExperimentalVariable_pkey" PRIMARY KEY (id);


--
-- TOC entry 3876 (class 2606 OID 16535)
-- Name: File File_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."File"
    ADD CONSTRAINT "File_pkey" PRIMARY KEY (id);


--
-- TOC entry 3858 (class 2606 OID 16404)
-- Name: InvitationCode InvitationCode_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."InvitationCode"
    ADD CONSTRAINT "InvitationCode_pkey" PRIMARY KEY (id);


--
-- TOC entry 3939 (class 2606 OID 16967)
-- Name: Molecule Molecule_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Molecule"
    ADD CONSTRAINT "Molecule_pkey" PRIMARY KEY (chembl_id);


--
-- TOC entry 3896 (class 2606 OID 16688)
-- Name: Organism Organism_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Organism"
    ADD CONSTRAINT "Organism_pkey" PRIMARY KEY (taxonomy_id);


--
-- TOC entry 3864 (class 2606 OID 16445)
-- Name: PermissionNode PermissionNode_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PermissionNode"
    ADD CONSTRAINT "PermissionNode_pkey" PRIMARY KEY (id);


--
-- TOC entry 3948 (class 2606 OID 17050)
-- Name: PhosphopeptideModelRegulation PhosphopeptideModelRegulation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PhosphopeptideModelRegulation"
    ADD CONSTRAINT "PhosphopeptideModelRegulation_pkey" PRIMARY KEY (analyte, model);


--
-- TOC entry 3943 (class 2606 OID 17026)
-- Name: PhosphopeptideRegulation PhosphopeptideRegulation_phosphopeptide_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PhosphopeptideRegulation"
    ADD CONSTRAINT "PhosphopeptideRegulation_phosphopeptide_id_key" UNIQUE (phosphopeptide_id);


--
-- TOC entry 3945 (class 2606 OID 17024)
-- Name: PhosphopeptideRegulation PhosphopeptideRegulation_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PhosphopeptideRegulation"
    ADD CONSTRAINT "PhosphopeptideRegulation_pkey" PRIMARY KEY (analyte);


--
-- TOC entry 3929 (class 2606 OID 16920)
-- Name: PhosphositeGroup PhosphositeGroup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PhosphositeGroup"
    ADD CONSTRAINT "PhosphositeGroup_pkey" PRIMARY KEY (group_id);


--
-- TOC entry 3931 (class 2606 OID 16926)
-- Name: Phosphosite Phosphosite_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Phosphosite"
    ADD CONSTRAINT "Phosphosite_pkey" PRIMARY KEY (id);


--
-- TOC entry 3868 (class 2606 OID 16475)
-- Name: Project Project_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Project"
    ADD CONSTRAINT "Project_pkey" PRIMARY KEY (id);


--
-- TOC entry 3900 (class 2606 OID 16776)
-- Name: Quantification Quantification_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Quantification"
    ADD CONSTRAINT "Quantification_pkey" PRIMARY KEY (id);


--
-- TOC entry 3889 (class 2606 OID 16625)
-- Name: SampleGroup SampleGroup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."SampleGroup"
    ADD CONSTRAINT "SampleGroup_pkey" PRIMARY KEY (id);


--
-- TOC entry 3893 (class 2606 OID 16646)
-- Name: Sample Sample_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Sample"
    ADD CONSTRAINT "Sample_pkey" PRIMARY KEY (id);


--
-- TOC entry 3923 (class 2606 OID 16893)
-- Name: UniProtAccession UniProtAccession_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."UniProtAccession"
    ADD CONSTRAINT "UniProtAccession_pkey" PRIMARY KEY (id);


--
-- TOC entry 3919 (class 2606 OID 16857)
-- Name: UniProtEntry UniProtEntry_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."UniProtEntry"
    ADD CONSTRAINT "UniProtEntry_pkey" PRIMARY KEY (accession_id);


--
-- TOC entry 3874 (class 2606 OID 16517)
-- Name: UploadRecord UploadRecord_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."UploadRecord"
    ADD CONSTRAINT "UploadRecord_pkey" PRIMARY KEY (id);


--
-- TOC entry 3860 (class 2606 OID 16417)
-- Name: UserGroup UserGroup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."UserGroup"
    ADD CONSTRAINT "UserGroup_pkey" PRIMARY KEY (id);


--
-- TOC entry 3856 (class 2606 OID 16396)
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- TOC entry 3870 (class 2606 OID 16491)
-- Name: WorkflowNode WorkflowNode_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."WorkflowNode"
    ADD CONSTRAINT "WorkflowNode_pkey" PRIMARY KEY (id);


--
-- TOC entry 3862 (class 2606 OID 16429)
-- Name: GroupMembership pk_groupmembership; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."GroupMembership"
    ADD CONSTRAINT pk_groupmembership PRIMARY KEY ("user", "group");


--
-- TOC entry 3941 (class 2606 OID 16976)
-- Name: MoleculeName pk_moleculename; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MoleculeName"
    ADD CONSTRAINT pk_moleculename PRIMARY KEY (name, chembl_id);


--
-- TOC entry 3866 (class 2606 OID 16457)
-- Name: Permission pk_permission; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Permission"
    ADD CONSTRAINT pk_permission PRIMARY KEY ("group", node);


--
-- TOC entry 3915 (class 2606 OID 16988)
-- Name: DEResult uq_deresult_test_analyte; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DEResult"
    ADD CONSTRAINT uq_deresult_test_analyte UNIQUE (contrast, analyte);


--
-- TOC entry 3933 (class 2606 OID 16928)
-- Name: Phosphosite uq_phosphosite_accession_residue; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Phosphosite"
    ADD CONSTRAINT uq_phosphosite_accession_residue UNIQUE (accession_id, residue);


--
-- TOC entry 3909 (class 1259 OID 17006)
-- Name: idx_contrastgroup_detest; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_contrastgroup_detest ON public."ContrastGroup" USING btree (de_test);


--
-- TOC entry 3910 (class 1259 OID 17007)
-- Name: idx_contrastgroup_samplegroup; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_contrastgroup_samplegroup ON public."ContrastGroup" USING btree (sample_group);


--
-- TOC entry 3913 (class 1259 OID 17003)
-- Name: idx_deresult_analyte; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_deresult_analyte ON public."DEResult" USING btree (analyte);


--
-- TOC entry 3936 (class 1259 OID 17002)
-- Name: idx_descriptorentryphosphosite_accession_residue; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_descriptorentryphosphosite_accession_residue ON public."DescriptorEntryPhosphosite" USING btree (accession_id, residue);


--
-- TOC entry 3937 (class 1259 OID 17001)
-- Name: idx_descriptorentryphosphosite_analyte; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_descriptorentryphosphosite_analyte ON public."DescriptorEntryPhosphosite" USING btree (analyte);


--
-- TOC entry 3926 (class 1259 OID 16998)
-- Name: idx_descriptorentryuniprot_accession; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_descriptorentryuniprot_accession ON public."DescriptorEntryUniProt" USING btree (accession_id);


--
-- TOC entry 3927 (class 1259 OID 16997)
-- Name: idx_descriptorentryuniprot_analyte; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_descriptorentryuniprot_analyte ON public."DescriptorEntryUniProt" USING btree (analyte);


--
-- TOC entry 3887 (class 1259 OID 16996)
-- Name: idx_experimentalcondition_variable; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_experimentalcondition_variable ON public."ExperimentalCondition" USING btree (variable);


--
-- TOC entry 3890 (class 1259 OID 16995)
-- Name: idx_groupcondition_condition; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_groupcondition_condition ON public."GroupCondition" USING btree (condition);


--
-- TOC entry 3891 (class 1259 OID 16994)
-- Name: idx_groupcondition_group; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_groupcondition_group ON public."GroupCondition" USING btree ("group");


--
-- TOC entry 3946 (class 1259 OID 17065)
-- Name: idx_ppreg_gene_symbol; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_ppreg_gene_symbol ON public."PhosphopeptideRegulation" USING btree (gene_symbol);


--
-- TOC entry 3916 (class 1259 OID 17004)
-- Name: idx_pvalue_deresult; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_pvalue_deresult ON public."PValue" USING btree (de_result);


--
-- TOC entry 3917 (class 1259 OID 17005)
-- Name: idx_pvalue_method; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_pvalue_method ON public."PValue" USING btree (adjustment_method);


--
-- TOC entry 3901 (class 1259 OID 16990)
-- Name: idx_quantification_analyte; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_quantification_analyte ON public."Quantification" USING btree (analyte);


--
-- TOC entry 3902 (class 1259 OID 16992)
-- Name: idx_quantification_dataset_analyte; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_quantification_dataset_analyte ON public."Quantification" USING btree (dataset, analyte);


--
-- TOC entry 3903 (class 1259 OID 16991)
-- Name: idx_quantification_dataset_sample; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_quantification_dataset_sample ON public."Quantification" USING btree (dataset, sample);


--
-- TOC entry 3904 (class 1259 OID 16989)
-- Name: idx_quantification_sample; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_quantification_sample ON public."Quantification" USING btree (sample);


--
-- TOC entry 3894 (class 1259 OID 16993)
-- Name: idx_sample_dataset_group; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_sample_dataset_group ON public."Sample" USING btree (dataset, "group");


--
-- TOC entry 3920 (class 1259 OID 16999)
-- Name: idx_uniprotgene_entry; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_uniprotgene_entry ON public."UniProtGene" USING btree (uniprot_entry);


--
-- TOC entry 3921 (class 1259 OID 17000)
-- Name: idx_uniprotgene_gene; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_uniprotgene_gene ON public."UniProtGene" USING btree (gene_name);


--
-- TOC entry 3967 (class 2606 OID 16578)
-- Name: Analyte fk_analyte_dataset; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Analyte"
    ADD CONSTRAINT fk_analyte_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);


--
-- TOC entry 3968 (class 2606 OID 16589)
-- Name: AnalyteDescriptor fk_analytedescriptor_dataset; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."AnalyteDescriptor"
    ADD CONSTRAINT fk_analytedescriptor_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);


--
-- TOC entry 3977 (class 2606 OID 16673)
-- Name: ConditionBait fk_conditionbait_condition; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionBait"
    ADD CONSTRAINT fk_conditionbait_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);


--
-- TOC entry 3978 (class 2606 OID 16678)
-- Name: ConditionBait fk_conditionbait_dataset; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionBait"
    ADD CONSTRAINT fk_conditionbait_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);


--
-- TOC entry 3979 (class 2606 OID 16693)
-- Name: ConditionCellType fk_conditioncelltype_condition; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionCellType"
    ADD CONSTRAINT fk_conditioncelltype_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);


--
-- TOC entry 3980 (class 2606 OID 16698)
-- Name: ConditionCellType fk_conditioncelltype_dataset; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionCellType"
    ADD CONSTRAINT fk_conditioncelltype_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);


--
-- TOC entry 3981 (class 2606 OID 16703)
-- Name: ConditionCellType fk_conditioncelltype_organism; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionCellType"
    ADD CONSTRAINT fk_conditioncelltype_organism FOREIGN KEY (organism) REFERENCES public."Organism"(taxonomy_id);


--
-- TOC entry 3984 (class 2606 OID 16724)
-- Name: ConditionDiet fk_conditiondiet_condition; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionDiet"
    ADD CONSTRAINT fk_conditiondiet_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);


--
-- TOC entry 3985 (class 2606 OID 16729)
-- Name: ConditionDiet fk_conditiondiet_dataset; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionDiet"
    ADD CONSTRAINT fk_conditiondiet_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);


--
-- TOC entry 3986 (class 2606 OID 16737)
-- Name: ConditionExercise fk_conditionexercise_condition; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionExercise"
    ADD CONSTRAINT fk_conditionexercise_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);


--
-- TOC entry 3987 (class 2606 OID 16742)
-- Name: ConditionExercise fk_conditionexercise_dataset; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionExercise"
    ADD CONSTRAINT fk_conditionexercise_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);


--
-- TOC entry 3982 (class 2606 OID 16711)
-- Name: ConditionKnockdown fk_conditionknockdown_condition; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionKnockdown"
    ADD CONSTRAINT fk_conditionknockdown_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);


--
-- TOC entry 3983 (class 2606 OID 16716)
-- Name: ConditionKnockdown fk_conditionknockdown_dataset; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionKnockdown"
    ADD CONSTRAINT fk_conditionknockdown_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);


--
-- TOC entry 3975 (class 2606 OID 16660)
-- Name: ConditionStimulus fk_conditionstimulus_condition; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionStimulus"
    ADD CONSTRAINT fk_conditionstimulus_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);


--
-- TOC entry 3976 (class 2606 OID 16665)
-- Name: ConditionStimulus fk_conditionstimulus_dataset; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionStimulus"
    ADD CONSTRAINT fk_conditionstimulus_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);


--
-- TOC entry 3988 (class 2606 OID 16750)
-- Name: ConditionTissue fk_conditiontissue_condition; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionTissue"
    ADD CONSTRAINT fk_conditiontissue_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);


--
-- TOC entry 3989 (class 2606 OID 16755)
-- Name: ConditionTissue fk_conditiontissue_dataset; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionTissue"
    ADD CONSTRAINT fk_conditiontissue_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);


--
-- TOC entry 3990 (class 2606 OID 16760)
-- Name: ConditionTissue fk_conditiontissue_organism; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ConditionTissue"
    ADD CONSTRAINT fk_conditiontissue_organism FOREIGN KEY (taxonomy_id) REFERENCES public."Organism"(taxonomy_id);


--
-- TOC entry 3996 (class 2606 OID 16816)
-- Name: ContrastGroup fk_contrastgroup_detest; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ContrastGroup"
    ADD CONSTRAINT fk_contrastgroup_detest FOREIGN KEY (de_test) REFERENCES public."DETest"(id);


--
-- TOC entry 3997 (class 2606 OID 16821)
-- Name: ContrastGroup fk_contrastgroup_samplegroup; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ContrastGroup"
    ADD CONSTRAINT fk_contrastgroup_samplegroup FOREIGN KEY (sample_group) REFERENCES public."SampleGroup"(id);


--
-- TOC entry 3957 (class 2606 OID 16500)
-- Name: Dataset fk_dataset_project; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Dataset"
    ADD CONSTRAINT fk_dataset_project FOREIGN KEY (project_id) REFERENCES public."Project"(id);


--
-- TOC entry 3958 (class 2606 OID 16505)
-- Name: Dataset fk_dataset_structurenode; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Dataset"
    ADD CONSTRAINT fk_dataset_structurenode FOREIGN KEY (structure_node) REFERENCES public."WorkflowNode"(id);


--
-- TOC entry 3964 (class 2606 OID 16562)
-- Name: DataSource fk_datasource_dataset; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DataSource"
    ADD CONSTRAINT fk_datasource_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);


--
-- TOC entry 3965 (class 2606 OID 16567)
-- Name: DataSource fk_datasource_file; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DataSource"
    ADD CONSTRAINT fk_datasource_file FOREIGN KEY (file) REFERENCES public."File"(id);


--
-- TOC entry 3966 (class 2606 OID 16557)
-- Name: DataSource fk_datasource_rootnode; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DataSource"
    ADD CONSTRAINT fk_datasource_rootnode FOREIGN KEY (root_node) REFERENCES public."WorkflowNode"(id);


--
-- TOC entry 3998 (class 2606 OID 16837)
-- Name: DEResult fk_deresult_analyte; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DEResult"
    ADD CONSTRAINT fk_deresult_analyte FOREIGN KEY (analyte) REFERENCES public."Analyte"(id);


--
-- TOC entry 3999 (class 2606 OID 16982)
-- Name: DEResult fk_deresult_detest; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DEResult"
    ADD CONSTRAINT fk_deresult_detest FOREIGN KEY (contrast) REFERENCES public."DETest"(id);


--
-- TOC entry 4011 (class 2606 OID 16955)
-- Name: DescriptorEntryPhosphosite fk_descriptorentryphosphosite_analyte; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DescriptorEntryPhosphosite"
    ADD CONSTRAINT fk_descriptorentryphosphosite_analyte FOREIGN KEY (analyte) REFERENCES public."Analyte"(id);


--
-- TOC entry 4012 (class 2606 OID 16950)
-- Name: DescriptorEntryPhosphosite fk_descriptorentryphosphosite_descriptor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DescriptorEntryPhosphosite"
    ADD CONSTRAINT fk_descriptorentryphosphosite_descriptor FOREIGN KEY (descriptor) REFERENCES public."AnalyteDescriptor"(id);


--
-- TOC entry 4006 (class 2606 OID 16910)
-- Name: DescriptorEntryUniProt fk_descriptorentryuniprot_analyte; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DescriptorEntryUniProt"
    ADD CONSTRAINT fk_descriptorentryuniprot_analyte FOREIGN KEY (analyte) REFERENCES public."Analyte"(id);


--
-- TOC entry 4007 (class 2606 OID 16905)
-- Name: DescriptorEntryUniProt fk_descriptorentryuniprot_descriptor; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DescriptorEntryUniProt"
    ADD CONSTRAINT fk_descriptorentryuniprot_descriptor FOREIGN KEY (descriptor) REFERENCES public."AnalyteDescriptor"(id);


--
-- TOC entry 3995 (class 2606 OID 16805)
-- Name: DETest fk_detest_rootnode; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."DETest"
    ADD CONSTRAINT fk_detest_rootnode FOREIGN KEY (root_node) REFERENCES public."WorkflowNode"(id);


--
-- TOC entry 3970 (class 2606 OID 16613)
-- Name: ExperimentalCondition fk_experimentalcondition_variable; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ExperimentalCondition"
    ADD CONSTRAINT fk_experimentalcondition_variable FOREIGN KEY (variable) REFERENCES public."ExperimentalVariable"(id);


--
-- TOC entry 3969 (class 2606 OID 16600)
-- Name: ExperimentalVariable fk_experimentalvariable_divergencenode; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."ExperimentalVariable"
    ADD CONSTRAINT fk_experimentalvariable_divergencenode FOREIGN KEY (divergence_node) REFERENCES public."WorkflowNode"(id);


--
-- TOC entry 3961 (class 2606 OID 16546)
-- Name: File fk_file_permissionnode; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."File"
    ADD CONSTRAINT fk_file_permissionnode FOREIGN KEY (permission_node) REFERENCES public."PermissionNode"(id);


--
-- TOC entry 3962 (class 2606 OID 16541)
-- Name: File fk_file_project; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."File"
    ADD CONSTRAINT fk_file_project FOREIGN KEY (project_id) REFERENCES public."Project"(id);


--
-- TOC entry 3963 (class 2606 OID 16536)
-- Name: File fk_file_uploadrecord; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."File"
    ADD CONSTRAINT fk_file_uploadrecord FOREIGN KEY (upload_record) REFERENCES public."UploadRecord"(id);


--
-- TOC entry 3971 (class 2606 OID 16634)
-- Name: GroupCondition fk_groupcondition_condition; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."GroupCondition"
    ADD CONSTRAINT fk_groupcondition_condition FOREIGN KEY (condition) REFERENCES public."ExperimentalCondition"(id);


--
-- TOC entry 3972 (class 2606 OID 16629)
-- Name: GroupCondition fk_groupcondition_group; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."GroupCondition"
    ADD CONSTRAINT fk_groupcondition_group FOREIGN KEY ("group") REFERENCES public."SampleGroup"(id);


--
-- TOC entry 3950 (class 2606 OID 16435)
-- Name: GroupMembership fk_groupmembership_group; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."GroupMembership"
    ADD CONSTRAINT fk_groupmembership_group FOREIGN KEY ("group") REFERENCES public."UserGroup"(id);


--
-- TOC entry 3951 (class 2606 OID 16430)
-- Name: GroupMembership fk_groupmembership_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."GroupMembership"
    ADD CONSTRAINT fk_groupmembership_user FOREIGN KEY ("user") REFERENCES public."User"(id);


--
-- TOC entry 3949 (class 2606 OID 16405)
-- Name: InvitationCode fk_invitationcode_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."InvitationCode"
    ADD CONSTRAINT fk_invitationcode_user FOREIGN KEY (used_by) REFERENCES public."User"(id);


--
-- TOC entry 4013 (class 2606 OID 16977)
-- Name: MoleculeName fk_moleculename_molecule; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."MoleculeName"
    ADD CONSTRAINT fk_moleculename_molecule FOREIGN KEY (chembl_id) REFERENCES public."Molecule"(chembl_id);


--
-- TOC entry 3953 (class 2606 OID 16458)
-- Name: Permission fk_permission_group; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Permission"
    ADD CONSTRAINT fk_permission_group FOREIGN KEY ("group") REFERENCES public."UserGroup"(id);


--
-- TOC entry 3954 (class 2606 OID 16463)
-- Name: Permission fk_permission_node; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Permission"
    ADD CONSTRAINT fk_permission_node FOREIGN KEY (node) REFERENCES public."PermissionNode"(id);


--
-- TOC entry 3952 (class 2606 OID 16446)
-- Name: PermissionNode fk_permissionnode_parent; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PermissionNode"
    ADD CONSTRAINT fk_permissionnode_parent FOREIGN KEY (parent) REFERENCES public."PermissionNode"(id);


--
-- TOC entry 4014 (class 2606 OID 17027)
-- Name: PhosphopeptideRegulation fk_phosphopeptideregulation_analyte; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PhosphopeptideRegulation"
    ADD CONSTRAINT fk_phosphopeptideregulation_analyte FOREIGN KEY (analyte) REFERENCES public."Analyte"(id);


--
-- TOC entry 4015 (class 2606 OID 17032)
-- Name: PhosphopeptideRegulation fk_phosphopeptideregulation_linkedprotein; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PhosphopeptideRegulation"
    ADD CONSTRAINT fk_phosphopeptideregulation_linkedprotein FOREIGN KEY (linked_protein_analyte_id) REFERENCES public."Analyte"(id);


--
-- TOC entry 4008 (class 2606 OID 16934)
-- Name: Phosphosite fk_phosphosite_group; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Phosphosite"
    ADD CONSTRAINT fk_phosphosite_group FOREIGN KEY (phosphosite_group) REFERENCES public."PhosphositeGroup"(group_id);


--
-- TOC entry 4009 (class 2606 OID 16939)
-- Name: Phosphosite fk_phosphosite_humananalogue; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Phosphosite"
    ADD CONSTRAINT fk_phosphosite_humananalogue FOREIGN KEY (human_analogue) REFERENCES public."Phosphosite"(id);


--
-- TOC entry 4010 (class 2606 OID 16929)
-- Name: Phosphosite fk_phosphosite_uniprotentry; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Phosphosite"
    ADD CONSTRAINT fk_phosphosite_uniprotentry FOREIGN KEY (uniprot_entry) REFERENCES public."UniProtEntry"(accession_id);


--
-- TOC entry 4016 (class 2606 OID 17051)
-- Name: PhosphopeptideModelRegulation fk_ppmodelreg_analyte; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PhosphopeptideModelRegulation"
    ADD CONSTRAINT fk_ppmodelreg_analyte FOREIGN KEY (analyte) REFERENCES public."Analyte"(id);


--
-- TOC entry 3955 (class 2606 OID 16481)
-- Name: Project fk_project_creator; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Project"
    ADD CONSTRAINT fk_project_creator FOREIGN KEY (creator) REFERENCES public."User"(id);


--
-- TOC entry 3956 (class 2606 OID 16476)
-- Name: Project fk_project_permissionnode; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Project"
    ADD CONSTRAINT fk_project_permissionnode FOREIGN KEY (permission_node) REFERENCES public."PermissionNode"(id);


--
-- TOC entry 4000 (class 2606 OID 16845)
-- Name: PValue fk_pvalue_deresult; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."PValue"
    ADD CONSTRAINT fk_pvalue_deresult FOREIGN KEY (de_result) REFERENCES public."DEResult"(id);


--
-- TOC entry 3991 (class 2606 OID 16782)
-- Name: Quantification fk_quantification_analyte; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Quantification"
    ADD CONSTRAINT fk_quantification_analyte FOREIGN KEY (analyte) REFERENCES public."Analyte"(id);


--
-- TOC entry 3992 (class 2606 OID 16792)
-- Name: Quantification fk_quantification_dataset; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Quantification"
    ADD CONSTRAINT fk_quantification_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);


--
-- TOC entry 3993 (class 2606 OID 16777)
-- Name: Quantification fk_quantification_node; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Quantification"
    ADD CONSTRAINT fk_quantification_node FOREIGN KEY (node) REFERENCES public."WorkflowNode"(id);


--
-- TOC entry 3994 (class 2606 OID 16787)
-- Name: Quantification fk_quantification_sample; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Quantification"
    ADD CONSTRAINT fk_quantification_sample FOREIGN KEY (sample) REFERENCES public."Sample"(id);


--
-- TOC entry 3973 (class 2606 OID 16647)
-- Name: Sample fk_sample_dataset; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Sample"
    ADD CONSTRAINT fk_sample_dataset FOREIGN KEY (dataset) REFERENCES public."Dataset"(id);


--
-- TOC entry 3974 (class 2606 OID 16652)
-- Name: Sample fk_sample_group; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."Sample"
    ADD CONSTRAINT fk_sample_group FOREIGN KEY ("group") REFERENCES public."SampleGroup"(id);


--
-- TOC entry 4005 (class 2606 OID 16894)
-- Name: UniProtAccession fk_uniprotaccession_currententry; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."UniProtAccession"
    ADD CONSTRAINT fk_uniprotaccession_currententry FOREIGN KEY (current_entry) REFERENCES public."UniProtEntry"(accession_id);


--
-- TOC entry 4004 (class 2606 OID 16883)
-- Name: UniprotAlternativeName fk_uniprotalternativename_entry; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."UniprotAlternativeName"
    ADD CONSTRAINT fk_uniprotalternativename_entry FOREIGN KEY (uniprot_entry) REFERENCES public."UniProtEntry"(accession_id);


--
-- TOC entry 4001 (class 2606 OID 16863)
-- Name: UniProtEntry fk_uniprotentry_humanentry; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."UniProtEntry"
    ADD CONSTRAINT fk_uniprotentry_humanentry FOREIGN KEY (human_entry) REFERENCES public."UniProtEntry"(accession_id);


--
-- TOC entry 4002 (class 2606 OID 16858)
-- Name: UniProtEntry fk_uniprotentry_organism; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."UniProtEntry"
    ADD CONSTRAINT fk_uniprotentry_organism FOREIGN KEY (organism) REFERENCES public."Organism"(taxonomy_id);


--
-- TOC entry 4003 (class 2606 OID 16873)
-- Name: UniProtGene fk_uniprotgene_entry; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."UniProtGene"
    ADD CONSTRAINT fk_uniprotgene_entry FOREIGN KEY (uniprot_entry) REFERENCES public."UniProtEntry"(accession_id);


--
-- TOC entry 3959 (class 2606 OID 16523)
-- Name: UploadRecord fk_uploadrecord_project; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."UploadRecord"
    ADD CONSTRAINT fk_uploadrecord_project FOREIGN KEY (project) REFERENCES public."Project"(id);


--
-- TOC entry 3960 (class 2606 OID 16518)
-- Name: UploadRecord fk_uploadrecord_uploader; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."UploadRecord"
    ADD CONSTRAINT fk_uploadrecord_uploader FOREIGN KEY (uploader) REFERENCES public."User"(id);


-- Completed on 2026-10-27 23:31:52 AEDT

--
-- PostgreSQL database dump complete
--

\unrestrict iwohjfvOV4OQPerJLl6I9cnWKpNRJHw5pOSXHcCx28uKN1ZATFIRAFNjUANUp3L

