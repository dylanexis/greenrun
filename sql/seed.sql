PRAGMA foreign_keys = ON;

-- Cruelty-free status stays 'unknown' until backed by a Leaping Bunny or PETA source in evidence
INSERT INTO brands(name, parent_company)
VALUES ('Nivea', 'Beiersdorf'),
('Dove', 'Unilever');

INSERT INTO products(name, brand_id, subcategory)
VALUES ('Body Lotion', 1, 'skin_care'),
('Moisturizing Creme', 1, 'skin_care'),
('Body Wash', 1, 'hygiene'),
('Body Wash', 2, 'hygiene'),
('Shampoo', 1, 'hair_care');
