-- 00_base_metadata.sql
-- Base PostgreSQL metadata exported from the thesis benchmark database.
-- Generated from the actual Project, Dataset, experimental-structure, and Sample rows
-- used for the TP1/PS1 benchmark.
--
-- Run after creating the PostgreSQL schema and before the Python import scripts.

BEGIN;

-- Project: 1 row(s)
INSERT INTO public."Project" ("id", "created_at", "updated_at", "name", "description", "date_from", "date_to", "permission_node", "creator") VALUES
    (1, '2026-08-18', '2026-08-18', 'Fazakerley 2023 Insulin Resistance Proteomics', '3T3-L1 adipocyte insulin resistance study containing total proteome and phosphoproteome datasets.', NULL, NULL, NULL, NULL);

-- Dataset: 2 row(s)
INSERT INTO public."Dataset" ("id", "created_at", "updated_at", "project_id", "name", "description", "structure_node") VALUES
    (1, '2026-08-18 22:55:53.930174', '2026-08-18 22:55:53.930174', 1, 'TP1 - Total Proteome', 'Supplementary Data 1. Total proteome across CTRL, CI, DEX, TNF, MPQ and AA models with basal and acute insulin-stimulated conditions.', NULL),
    (2, '2026-08-18 22:55:53.930174', '2026-08-18 22:55:53.930174', 1, 'PS1 - Phosphoproteome', 'Supplementary Data 3. Phosphoproteome across CTRL, CI, DEX, TNF, MPQ and AA models with basal and acute insulin-stimulated conditions.', NULL);

-- ExperimentalVariable: 2 row(s)
INSERT INTO public."ExperimentalVariable" ("id", "type", "divergence_node") VALUES
    (1, 'ST', NULL),
    (2, 'ST', NULL);

-- ExperimentalCondition: 8 row(s)
INSERT INTO public."ExperimentalCondition" ("id", "name", "variable") VALUES
    (1, 'CTRL', 1),
    (2, 'CI', 1),
    (3, 'DEX', 1),
    (4, 'TNF', 1),
    (5, 'MPQ', 1),
    (6, 'AA', 1),
    (7, 'BASAL', 2),
    (8, 'INS', 2);

-- SampleGroup: 12 row(s)
INSERT INTO public."SampleGroup" ("id", "name") VALUES
    (1, 'CTRL_BASAL'),
    (2, 'CTRL_INS'),
    (3, 'CI_BASAL'),
    (4, 'CI_INS'),
    (5, 'DEX_BASAL'),
    (6, 'DEX_INS'),
    (7, 'TNF_BASAL'),
    (8, 'TNF_INS'),
    (9, 'MPQ_BASAL'),
    (10, 'MPQ_INS'),
    (11, 'AA_BASAL'),
    (12, 'AA_INS');

-- GroupCondition: 24 row(s)
INSERT INTO public."GroupCondition" ("group", "condition") VALUES
    ('1', '1'),
    ('1', '7'),
    ('2', '1'),
    ('2', '8'),
    ('3', '2'),
    ('3', '7'),
    ('4', '2'),
    ('4', '8'),
    ('5', '3'),
    ('5', '7'),
    ('6', '3'),
    ('6', '8'),
    ('7', '4'),
    ('7', '7'),
    ('8', '4'),
    ('8', '8'),
    ('9', '5'),
    ('9', '7'),
    ('10', '5'),
    ('10', '8'),
    ('11', '6'),
    ('11', '7'),
    ('12', '6'),
    ('12', '8');

-- Sample: 100 row(s)
INSERT INTO public."Sample" ("id", "name", "batch", "dataset", "group") VALUES
    (1, 'CTRL_BASAL_1', 1, 1, 1),
    (2, 'CTRL_BASAL_2', 2, 1, 1),
    (3, 'CTRL_BASAL_3', 3, 1, 1),
    (4, 'CTRL_BASAL_4', 4, 1, 1),
    (5, 'CTRL_BASAL_5', 5, 1, 1),
    (6, 'CTRL_INS_1', 1, 1, 2),
    (7, 'CTRL_INS_2', 2, 1, 2),
    (8, 'CTRL_INS_3', 3, 1, 2),
    (9, 'CTRL_INS_4', 4, 1, 2),
    (10, 'CTRL_INS_5', 5, 1, 2),
    (11, 'CI_BASAL_1', 1, 1, 3),
    (12, 'CI_BASAL_2', 2, 1, 3),
    (13, 'CI_BASAL_3', 3, 1, 3),
    (14, 'CI_INS_1', 1, 1, 4),
    (15, 'CI_INS_2', 2, 1, 4),
    (16, 'CI_INS_3', 3, 1, 4),
    (17, 'CI_INS_4', 4, 1, 4),
    (18, 'DEX_BASAL_1', 1, 1, 5),
    (19, 'DEX_BASAL_2', 2, 1, 5),
    (20, 'DEX_BASAL_3', 3, 1, 5),
    (21, 'DEX_BASAL_4', 4, 1, 5),
    (22, 'DEX_INS_1', 1, 1, 6),
    (23, 'DEX_INS_2', 2, 1, 6),
    (24, 'DEX_INS_3', 3, 1, 6),
    (25, 'DEX_INS_4', 4, 1, 6),
    (26, 'TNF_BASAL_1', 1, 1, 7),
    (27, 'TNF_BASAL_2', 2, 1, 7),
    (28, 'TNF_BASAL_3', 3, 1, 7),
    (29, 'TNF_INS_1', 1, 1, 8),
    (30, 'TNF_INS_2', 2, 1, 8),
    (31, 'TNF_INS_3', 3, 1, 8),
    (32, 'TNF_INS_4', 4, 1, 8),
    (33, 'MPQ_BASAL_1', 1, 1, 9),
    (34, 'MPQ_BASAL_2', 2, 1, 9),
    (35, 'MPQ_BASAL_3', 3, 1, 9),
    (36, 'MPQ_BASAL_4', 4, 1, 9),
    (37, 'MPQ_INS_1', 1, 1, 10),
    (38, 'MPQ_INS_2', 2, 1, 10),
    (39, 'MPQ_INS_3', 3, 1, 10),
    (40, 'MPQ_INS_4', 4, 1, 10),
    (41, 'AA_BASAL_1', 1, 1, 11),
    (42, 'AA_BASAL_2', 2, 1, 11),
    (43, 'AA_BASAL_3', 3, 1, 11),
    (44, 'AA_BASAL_4', 4, 1, 11),
    (45, 'AA_INS_1', 1, 1, 12),
    (46, 'AA_INS_2', 2, 1, 12),
    (47, 'AA_INS_3', 3, 1, 12),
    (48, 'AA_INS_4', 4, 1, 12),
    (49, 'CTRL_BAS_1', 1, 2, 1),
    (50, 'CTRL_BAS_2', 2, 2, 1),
    (51, 'CTRL_BAS_3', 3, 2, 1),
    (52, 'CTRL_BAS_4', 4, 2, 1),
    (53, 'CTRL_BAS_5', 5, 2, 1),
    (54, 'CTRL_BAS_6', 6, 2, 1),
    (55, 'CTRL_INS_1', 1, 2, 2),
    (56, 'CTRL_INS_2', 2, 2, 2),
    (57, 'CTRL_INS_3', 3, 2, 2),
    (58, 'CTRL_INS_4', 4, 2, 2),
    (59, 'CTRL_INS_5', 5, 2, 2),
    (60, 'CTRL_INS_6', 6, 2, 2),
    (61, 'CI_BAS_1', 1, 2, 3),
    (62, 'CI_BAS_2', 2, 2, 3),
    (63, 'CI_BAS_3', 3, 2, 3),
    (64, 'CI_BAS_4', 4, 2, 3),
    (65, 'CI_INS_1', 1, 2, 4),
    (66, 'CI_INS_2', 2, 2, 4),
    (67, 'CI_INS_3', 3, 2, 4),
    (68, 'CI_INS_4', 4, 2, 4),
    (69, 'DEX_BAS_1', 1, 2, 5),
    (70, 'DEX_BAS_2', 2, 2, 5),
    (71, 'DEX_BAS_3', 3, 2, 5),
    (72, 'DEX_BAS_4', 4, 2, 5),
    (73, 'DEX_INS_1', 1, 2, 6),
    (74, 'DEX_INS_2', 2, 2, 6),
    (75, 'DEX_INS_3', 3, 2, 6),
    (76, 'DEX_INS_4', 4, 2, 6),
    (77, 'TNF_BAS_1', 1, 2, 7),
    (78, 'TNF_BAS_2', 2, 2, 7),
    (79, 'TNF_BAS_3', 3, 2, 7),
    (80, 'TNF_BAS_4', 4, 2, 7),
    (81, 'TNF_INS_1', 1, 2, 8),
    (82, 'TNF_INS_2', 2, 2, 8),
    (83, 'TNF_INS_3', 3, 2, 8),
    (84, 'TNF_INS_4', 4, 2, 8),
    (85, 'MPQ_BAS_1', 1, 2, 9),
    (86, 'MPQ_BAS_2', 2, 2, 9),
    (87, 'MPQ_BAS_3', 3, 2, 9),
    (88, 'MPQ_BAS_4', 4, 2, 9),
    (89, 'MPQ_INS_1', 1, 2, 10),
    (90, 'MPQ_INS_2', 2, 2, 10),
    (91, 'MPQ_INS_3', 3, 2, 10),
    (92, 'MPQ_INS_4', 4, 2, 10),
    (93, 'AA_BAS_1', 1, 2, 11),
    (94, 'AA_BAS_2', 2, 2, 11),
    (95, 'AA_BAS_3', 3, 2, 11),
    (96, 'AA_BAS_4', 4, 2, 11),
    (97, 'AA_INS_1', 1, 2, 12),
    (98, 'AA_INS_2', 2, 2, 12),
    (99, 'AA_INS_3', 3, 2, 12),
    (100, 'AA_INS_4', 4, 2, 12);

COMMIT;

-- Expected row counts after import:
-- Project: 1
-- Dataset: 2
-- ExperimentalVariable: 2
-- ExperimentalCondition: 8
-- SampleGroup: 12
-- GroupCondition: 24
-- Sample: 100