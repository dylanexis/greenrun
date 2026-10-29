PRAGMA foreign_keys = ON;

INSERT INTO animal_ingredients(name, status, notes)
VALUES ('beeswax', 'animal', 'Produced by honeybees'),
('lanolin', 'animal', 'Wax from sheep''s wool'),
('carmine', 'animal', 'Red dye from cochineal insects'),
('honey', 'animal', NULL),
('keratin', 'animal', 'Protein from hair, feathers, horns'),
('collagen', 'animal', 'Usually from cow or fish skin and bones'),
('silk', 'animal', 'From silkworm cocoons'),
('shellac', 'animal', 'Resin secreted by lac insects'),
('guanine', 'animal', 'Shimmer from fish scales'),
('gelatin', 'animal', 'From animal skin and bones'),
('casein', 'animal', 'Milk protein'),
('elastin', 'animal', 'Protein from animal tissue'),
('sodium tallowate', 'animal', 'Soap made from animal fat'),
('squalene', 'maybe', 'Shark liver or plant oils; squalane (-ane) is usually plant-based'),
('glycerin', 'maybe', 'Animal fat or plant oils; labels rarely say which'),
('stearic acid', 'maybe', 'Animal fat or plant oils');

INSERT INTO ingredient_aliases(alias, ingredient_id)
VALUES ('beeswax', 1), ('cera alba', 1), ('cera flava', 1),
('lanolin', 2), ('wool wax', 2), ('wool fat', 2),
('carmine', 3), ('ci 75470', 3), ('cochineal', 3), ('carminic acid', 3),
('honey', 4), ('mel', 4),
('keratin', 5), ('hydrolyzed keratin', 5),
('collagen', 6), ('hydrolyzed collagen', 6),
('silk', 7), ('sericin', 7), ('hydrolyzed silk', 7), ('silk powder', 7),
('shellac', 8),
('guanine', 9), ('ci 75170', 9),
('gelatin', 10), ('gelatine', 10),
('casein', 11),
('elastin', 12),
('sodium tallowate', 13), ('tallow', 13),
('squalene', 14),
('glycerin', 15), ('glycerine', 15), ('glycerol', 15),
('stearic acid', 16);
