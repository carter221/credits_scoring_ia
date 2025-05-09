-- Suppression des tables si elles existent déjà
DROP TABLE IF EXISTS loan_features;
DROP TABLE IF EXISTS loan_applications;
DROP TABLE IF EXISTS clients;

-- Création de la table clients
CREATE TABLE clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sk_id_curr INTEGER UNIQUE,
    code_gender TEXT,
    flag_own_car TEXT,
    flag_own_realty TEXT,
    cnt_children INTEGER,
    days_birth INTEGER,
    days_employed INTEGER,
    amt_income_total REAL,
    region_population_relative REAL,
    ext_source_1 REAL,
    ext_source_2 REAL,
    ext_source_3 REAL,
    created_date TEXT,
    status TEXT DEFAULT 'active'
);

-- Création de la table demandes de prêt
CREATE TABLE loan_applications (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    name_contract_type TEXT,
    amt_credit REAL,
    amt_annuity REAL,
    amt_goods_price REAL,
    days_employed_anom INTEGER,
    application_date TEXT,
    status TEXT,
    target INTEGER,
    prediction_probability REAL,
    FOREIGN KEY (client_id) REFERENCES clients(client_id)
);

-- Création de la table pour les variables calculées
CREATE TABLE loan_features (
    feature_id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id INTEGER,
    dir_ratio REAL,  -- debt-to-income ratio
    air_ratio REAL,  -- annuity-to-income ratio
    acr_ratio REAL,  -- annuity-to-credit ratio
    dar_ratio REAL,  -- days-employed-to-age ratio
    FOREIGN KEY (application_id) REFERENCES loan_applications(application_id)
);

-- Insertion de données de clients générées
INSERT INTO clients (sk_id_curr, code_gender, flag_own_car, flag_own_realty, cnt_children, days_birth, days_employed, amt_income_total, region_population_relative, ext_source_1, ext_source_2, ext_source_3, created_date, status)
VALUES
    (100001, 'M', 'Y', 'Y', 1, -12784, -3521, 45000.00, 0.025478, 0.6, 0.8, 0.7, '2023-01-15', 'active'),
    (100002, 'F', 'N', 'Y', 0, -18327, -5214, 36500.00, 0.035698, 0.5, 0.7, 0.8, '2023-02-20', 'active'),
    (100003, 'M', 'Y', 'N', 2, -15640, -2134, 55000.00, 0.018945, 0.7, 0.6, 0.5, '2023-03-05', 'active'),
    (100004, 'F', 'Y', 'Y', 1, -20158, -4587, 65000.00, 0.042136, 0.8, 0.5, 0.6, '2023-03-10', 'active'),
    (100005, 'M', 'N', 'Y', 0, -16789, -3215, 42000.00, 0.031254, 0.6, 0.7, 0.8, '2023-04-18', 'active'),
    (100006, 'F', 'N', 'N', 1, -14520, -1823, 38000.00, 0.027896, 0.7, 0.6, 0.5, '2023-05-22', 'active'),
    (100007, 'M', 'Y', 'Y', 3, -19874, -8965, 75000.00, 0.053214, 0.5, 0.8, 0.7, '2023-06-01', 'active'),
    (100008, 'F', 'Y', 'N', 0, -17456, -2375, 48000.00, 0.029654, 0.8, 0.7, 0.6, '2023-06-15', 'active'),
    (100009, 'M', 'N', 'Y', 2, -14239, -3641, 52000.00, 0.034125, 0.7, 0.5, 0.8, '2023-07-20', 'active'),
    (100010, 'F', 'Y', 'Y', 1, -16543, -4578, 39500.00, 0.021487, 0.6, 0.6, 0.7, '2023-08-05', 'active'),
    (100011, 'M', 'N', 'N', 0, -21354, -7654, 85000.00, 0.048965, 0.9, 0.8, 0.9, '2023-08-12', 'active'),
    (100012, 'F', 'Y', 'N', 1, -18965, -2987, 41000.00, 0.031576, 0.7, 0.7, 0.8, '2023-09-01', 'active'),
    (100013, 'M', 'Y', 'Y', 2, -15741, -3654, 58000.00, 0.023478, 0.6, 0.9, 0.6, '2023-09-15', 'active'),
    (100014, 'F', 'N', 'Y', 0, -19874, -5421, 44000.00, 0.035142, 0.8, 0.6, 0.5, '2023-10-10', 'active'),
    (100015, 'M', 'Y', 'N', 1, -17845, -4124, 62000.00, 0.028756, 0.7, 0.7, 0.7, '2023-10-25', 'active');

-- Insertion de demandes de prêt
INSERT INTO loan_applications (client_id, name_contract_type, amt_credit, amt_annuity, amt_goods_price, days_employed_anom, application_date, status, target, prediction_probability)
VALUES
    (1, 'Cash loans', 20000.00, 1666.67, 18000.00, 0, '2023-01-20', 'approved', 0, 0.15),
    (2, 'Revolving loans', 15000.00, 1250.00, 13500.00, 0, '2023-02-25', 'approved', 0, 0.12),
    (3, 'Cash loans', 30000.00, 2500.00, 27000.00, 0, '2023-03-08', 'approved', 0, 0.09),
    (4, 'Cash loans', 35000.00, 2916.67, 31500.00, 0, '2023-03-15', 'rejected', 1, 0.65),
    (5, 'Revolving loans', 18000.00, 1500.00, 16200.00, 0, '2023-04-20', 'approved', 0, 0.18),
    (6, 'Revolving loans', 12000.00, 1000.00, 10800.00, 0, '2023-05-25', 'approved', 0, 0.22),
    (7, 'Cash loans', 50000.00, 4166.67, 45000.00, 1, '2023-06-05', 'rejected', 1, 0.72),
    (8, 'Cash loans', 25000.00, 2083.33, 22500.00, 0, '2023-06-18', 'approved', 0, 0.14),
    (9, 'Revolving loans', 28000.00, 2333.33, 25200.00, 0, '2023-07-22', 'approved', 0, 0.25),
    (10, 'Cash loans', 15000.00, 1250.00, 13500.00, 0, '2023-08-10', 'rejected', 1, 0.58),
    (11, 'Cash loans', 60000.00, 5000.00, 54000.00, 0, '2023-08-15', 'approved', 0, 0.11),
    (12, 'Revolving loans', 20000.00, 1666.67, 18000.00, 0, '2023-09-05', 'approved', 0, 0.17),
    (13, 'Cash loans', 32000.00, 2666.67, 28800.00, 0, '2023-09-20', 'rejected', 1, 0.62),
    (14, 'Revolving loans', 22000.00, 1833.33, 19800.00, 0, '2023-10-15', 'approved', 0, 0.24),
    (15, 'Cash loans', 40000.00, 3333.33, 36000.00, 0, '2023-11-01', 'pending', 0, 0.32),
    (1, 'Revolving loans', 15000.00, 1250.00, 13500.00, 0, '2023-04-10', 'approved', 0, 0.16),
    (3, 'Cash loans', 25000.00, 2083.33, 22500.00, 0, '2023-05-15', 'rejected', 1, 0.55),
    (5, 'Revolving loans', 20000.00, 1666.67, 18000.00, 0, '2023-07-01', 'approved', 0, 0.21),
    (7, 'Cash loans', 30000.00, 2500.00, 27000.00, 0, '2023-08-20', 'approved', 0, 0.28),
    (9, 'Revolving loans', 18000.00, 1500.00, 16200.00, 0, '2023-10-05', 'pending', 0, 0.35);

-- Insertion de caractéristiques calculées
INSERT INTO loan_features (application_id, dir_ratio, air_ratio, acr_ratio, dar_ratio)
VALUES
    (1, 0.444, 0.037, 0.083, 0.275),
    (2, 0.411, 0.034, 0.083, 0.284),
    (3, 0.545, 0.045, 0.083, 0.136),
    (4, 0.538, 0.045, 0.083, 0.227),
    (5, 0.429, 0.036, 0.083, 0.191),
    (6, 0.316, 0.026, 0.083, 0.126),
    (7, 0.667, 0.056, 0.083, 0.451),
    (8, 0.521, 0.043, 0.083, 0.136),
    (9, 0.538, 0.045, 0.083, 0.256),
    (10, 0.380, 0.032, 0.083, 0.277),
    (11, 0.706, 0.059, 0.083, 0.358),
    (12, 0.488, 0.041, 0.083, 0.157),
    (13, 0.552, 0.046, 0.083, 0.232),
    (14, 0.500, 0.042, 0.083, 0.273),
    (15, 0.645, 0.054, 0.083, 0.231),
    (16, 0.333, 0.028, 0.083, 0.275),
    (17, 0.455, 0.038, 0.083, 0.136),
    (18, 0.476, 0.040, 0.083, 0.191),
    (19, 0.400, 0.033, 0.083, 0.451),
    (20, 0.346, 0.029, 0.083, 0.256);

-- Insertion complémentaire de clients plus diversifiés
INSERT INTO clients (sk_id_curr, code_gender, flag_own_car, flag_own_realty, cnt_children, days_birth, days_employed, amt_income_total, region_population_relative, ext_source_1, ext_source_2, ext_source_3, created_date, status)
VALUES
    (100016, 'M', 'Y', 'Y', 0, -22458, -8745, 95000.00, 0.045123, 0.85, 0.92, 0.78, '2023-11-05', 'active'),
    (100017, 'F', 'N', 'Y', 3, -16987, -2145, 32000.00, 0.019876, 0.45, 0.38, 0.52, '2023-11-10', 'active'),
    (100018, 'M', 'Y', 'N', 1, -19543, -6234, 68000.00, 0.037456, 0.72, 0.65, 0.70, '2023-11-15', 'active'),
    (100019, 'F', 'Y', 'Y', 2, -14765, -1987, 40000.00, 0.026437, 0.58, 0.63, 0.49, '2023-11-20', 'active'),
    (100020, 'M', 'N', 'Y', 0, -20765, -7654, 78000.00, 0.041235, 0.79, 0.81, 0.75, '2023-11-25', 'active'),
    (100021, 'F', 'N', 'N', 1, -18432, -3567, 42000.00, 0.028765, 0.61, 0.58, 0.63, '2023-11-30', 'active'),
    (100022, 'M', 'Y', 'Y', 4, -16543, -4321, 85000.00, 0.047632, 0.76, 0.72, 0.68, '2023-12-05', 'active'),
    (100023, 'F', 'Y', 'N', 0, -21876, -6789, 55000.00, 0.032145, 0.81, 0.77, 0.83, '2023-12-10', 'active'),
    (100024, 'M', 'N', 'Y', 2, -17654, -3456, 47500.00, 0.029874, 0.65, 0.59, 0.71, '2023-12-15', 'active'),
    (100025, 'F', 'Y', 'Y', 1, -19765, -5432, 51000.00, 0.036218, 0.73, 0.68, 0.64, '2023-12-20', 'active');
