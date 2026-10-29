PRAGMA foreign_keys = ON;


CREATE TABLE brands(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    parent_company TEXT,
    cruelty_free TEXT NOT NULL DEFAULT 'unknown',
    certification TEXT,
    CHECK(cruelty_free IN ('yes', 'no', 'unknown')),
    CHECK(certification IN ('leaping_bunny', 'peta', 'both'))
);

CREATE TABLE products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand_id INTEGER NOT NULL,
    subcategory TEXT NOT NULL,
    barcode TEXT UNIQUE,
    product_url TEXT,
    FOREIGN KEY (brand_id) REFERENCES brands(id)
);

-- Raw ingredient names in label order; matched against animal_ingredients at query time
CREATE TABLE product_ingredients(
    product_id INTEGER NOT NULL,
    position INTEGER NOT NULL,
    name TEXT NOT NULL,
    PRIMARY KEY (product_id, position),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE animal_ingredients(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    status TEXT NOT NULL,
    notes TEXT,
    CHECK(status IN ('animal', 'maybe'))
);

-- Alternate label names (lowercase), e.g. 'cera alba' for beeswax
CREATE TABLE ingredient_aliases(
    alias TEXT PRIMARY KEY,
    ingredient_id INTEGER NOT NULL,
    FOREIGN KEY (ingredient_id) REFERENCES animal_ingredients(id)
);

-- Each claim backs either a brand's cruelty-free status or an ingredient's status
CREATE TABLE evidence(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand_id INTEGER,
    ingredient_id INTEGER,
    claim TEXT NOT NULL,
    source_url TEXT,
    CHECK((brand_id IS NULL) != (ingredient_id IS NULL)),
    FOREIGN KEY (brand_id) REFERENCES brands(id),
    FOREIGN KEY (ingredient_id) REFERENCES animal_ingredients(id)
);
