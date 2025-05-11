-- Suppression des tables si elles existent déjà
DROP TABLE IF EXISTS loan_features;
DROP TABLE IF EXISTS loan_applications;
DROP TABLE IF EXISTS clients;

-- Création de la table clients avec tous les champs demandés
CREATE TABLE clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sk_id_curr INTEGER UNIQUE,
    CODE_GENDER TEXT,
    CNT_CHILDREN INTEGER,
    AMT_CREDIT REAL,
    AMT_GOODS_PRICE REAL,
    DAYS_EMPLOYED INTEGER,
    FLAG_EMP_PHONE INTEGER,
    CNT_FAM_MEMBERS INTEGER,
    REGION_RATING_CLIENT INTEGER,
    REGION_RATING_CLIENT_W_CITY INTEGER,
    REG_REGION_NOT_WORK_REGION INTEGER,
    LIVE_REGION_NOT_WORK_REGION INTEGER,
    REG_CITY_NOT_WORK_CITY INTEGER,
    LIVE_CITY_NOT_WORK_CITY INTEGER,
    YEARS_BEGINEXPLUATATION_AVG REAL,
    FLOORSMAX_AVG REAL,
    YEARS_BEGINEXPLUATATION_MODE REAL,
    FLOORSMAX_MODE REAL,
    YEARS_BEGINEXPLUATATION_MEDI REAL,
    FLOORSMAX_MEDI REAL,
    OBS_30_CNT_SOCIAL_CIRCLE INTEGER,
    DEF_30_CNT_SOCIAL_CIRCLE INTEGER,
    OBS_60_CNT_SOCIAL_CIRCLE INTEGER,
    DEF_60_CNT_SOCIAL_CIRCLE INTEGER,
    created_date TEXT,
    status TEXT DEFAULT 'active'
);

-- Insertion des données de 15 clients
INSERT INTO clients (
    sk_id_curr, CODE_GENDER, CNT_CHILDREN, AMT_CREDIT, AMT_GOODS_PRICE, DAYS_EMPLOYED, 
    FLAG_EMP_PHONE, CNT_FAM_MEMBERS, REGION_RATING_CLIENT, REGION_RATING_CLIENT_W_CITY,
    REG_REGION_NOT_WORK_REGION, LIVE_REGION_NOT_WORK_REGION, REG_CITY_NOT_WORK_CITY, 
    LIVE_CITY_NOT_WORK_CITY, YEARS_BEGINEXPLUATATION_AVG, FLOORSMAX_AVG, 
    YEARS_BEGINEXPLUATATION_MODE, FLOORSMAX_MODE, YEARS_BEGINEXPLUATATION_MEDI, 
    FLOORSMAX_MEDI, OBS_30_CNT_SOCIAL_CIRCLE, DEF_30_CNT_SOCIAL_CIRCLE, 
    OBS_60_CNT_SOCIAL_CIRCLE, DEF_60_CNT_SOCIAL_CIRCLE, created_date, status
)
VALUES
    (100001, 'M', 1, 200000.00, 180000.00, -3521, 1, 3, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-01-15', 'active'),
    (100002, 'F', 0, 150000.00, 135000.00, -5214, 1, 2, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-02-20', 'active'),
    (100003, 'M', 2, 220000.00, 198000.00, -2134, 1, 4, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-03-05', 'active'),
    (100004, 'F', 1, 185000.00, 166500.00, -4587, 1, 3, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-03-10', 'active'),
    (100005, 'M', 0, 175000.00, 157500.00, -3215, 1, 2, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-04-18', 'active'),
    (100006, 'F', 1, 190000.00, 171000.00, -1823, 1, 3, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-05-22', 'active'),
    (100007, 'M', 3, 250000.00, 225000.00, -8965, 1, 5, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-06-01', 'active'),
    (100008, 'F', 0, 140000.00, 126000.00, -2375, 1, 2, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-06-15', 'active'),
    (100009, 'M', 2, 210000.00, 189000.00, -3641, 1, 4, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-07-20', 'active'),
    (100010, 'F', 1, 200000.00, 180000.00, -4578, 1, 3, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-08-05', 'active'),
    (100011, 'M', 0, 160000.00, 144000.00, -7654, 1, 2, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-08-12', 'active'),
    (100012, 'F', 1, 175000.00, 157500.00, -2987, 1, 3, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-09-01', 'active'),
    (100013, 'M', 2, 235000.00, 211500.00, -3654, 1, 4, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-09-15', 'active'),
    (100014, 'F', 0, 155000.00, 139500.00, -5421, 1, 2, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-10-10', 'active'),
    (100015, 'M', 1, 180000.00, 162000.00, -4124, 1, 3, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-10-25', 'active'),
    (100016, 'M', 0, 200000.00, 180000.00, -5000, 1, 2, 1, 1, 0, 0, 0, 0, 0.9, 0.8, 0.9, 0.8, 0.9, 0.8, 0, 0, 0, 0, '2023-11-01', 'active'),
    (100017, 'F', 3, 1500000.00, 1400000.00, -100, 0, 6, 3, 3, 1, 1, 1, 1, 0.2, 0.1, 0.2, 0.1, 0.2, 0.1, 15, 10, 12, 8, '2023-11-05', 'active');

-- Instructions d'utilisation
-- Pour lancer la base de données SQLite avec ce schéma :
-- 1. Ouvrez un terminal et placez-vous dans le dossier contenant ce fichier
-- 2. Exécutez : sqlite3 credit_scoring_simplified.sqlite3 < init_credit_db.sql
-- 3. Vérifiez le contenu : sqlite3 credit_scoring_simplified.sqlite3
-- 4. Dans le prompt SQLite : .tables puis SELECT * FROM clients LIMIT 5;
