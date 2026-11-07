-- Organism row exported by the project author; generated from organism.csv.
-- Run after schema creation and base metadata, before the Python entity loaders.
BEGIN;
INSERT INTO public."Organism" (taxonomy_id, scientific_name, common_name)
VALUES (10090, 'Mus musculus', 'mouse');
COMMIT;
