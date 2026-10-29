PRAGMA foreign_keys = ON;

-- Lifecycle medians (gCO2eq/kWh) from IPCC AR5 WGIII Annex III, Table A.III.2
-- OIL and OTH have no IPCC median; they stay NULL until a cited value is chosen
INSERT INTO emission_factors(fuel, name, g_co2_per_kwh, source_url)
VALUES ('COL', 'Coal', 820, 'https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf'),
('NG', 'Natural gas (combined cycle)', 490, 'https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf'),
('NUC', 'Nuclear', 12, 'https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf'),
('WAT', 'Hydro', 24, 'https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf'),
('SUN', 'Solar PV (utility)', 48, 'https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf'),
('WND', 'Wind (onshore)', 11, 'https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf'),
('OIL', 'Petroleum', NULL, NULL),
('OTH', 'Other', NULL, NULL);
