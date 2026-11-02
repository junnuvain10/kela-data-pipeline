import random
from datetime import date, timedelta
from faker import Faker
from psycopg2.extras import execute_values
from database import get_connection

# Initialize Faker with Finnish locale for authentic names and SSNs
fake = Faker('fi_FI')

# Static reference data for OLTP tables extracted from the provided dataset
MUNICIPALITIES = [
    ('020', 'Akaa'), ('005', 'Alajärvi'), ('009', 'Alavieska'),
    ('010', 'Alavus'), ('016', 'Asikkala'), ('018', 'Askola'),
    ('019', 'Aura'), ('035', 'Brändö'), ('043', 'Eckerö'),
    ('046', 'Enonkoski'), ('047', 'Enontekiö'), ('049', 'Espoo'),
    ('050', 'Eura'), ('051', 'Eurajoki'), ('052', 'Evijärvi'),
    ('060', 'Finström'), ('061', 'Forssa'), ('062', 'Föglö'),
    ('065', 'Geta'), ('069', 'Haapajärvi'), ('071', 'Haapavesi'),
    ('072', 'Hailuoto'), ('074', 'Halsua'), ('075', 'Hamina'),
    ('076', 'Hammarland'), ('077', 'Hankasalmi'), ('078', 'Hanko'),
    ('079', 'Harjavalta'), ('081', 'Hartola'), ('082', 'Hattula'),
    ('086', 'Hausjärvi'), ('111', 'Heinola'), ('090', 'Heinävesi'),
    ('091', 'Helsinki'), ('097', 'Hirvensalmi'), ('098', 'Hollola'),
    ('102', 'Huittinen'), ('103', 'Humppila'), ('105', 'Hyrynsalmi'),
    ('106', 'Hyvinkää'), ('108', 'Hämeenkyrö'), ('109', 'Hämeenlinna'),
    ('139', 'Ii'), ('140', 'Iisalmi'), ('142', 'Iitti'),
    ('143', 'Ikaalinen'), ('145', 'Ilmajoki'), ('146', 'Ilomantsi'),
    ('153', 'Imatra'), ('148', 'Inari'), ('149', 'Inkoo'),
    ('150', 'Isojoki'), ('152', 'Isokyrö'), ('165', 'Janakkala'),
    ('167', 'Joensuu'), ('169', 'Jokioinen'), ('170', 'Jomala'),
    ('171', 'Joroinen'), ('172', 'Joutsa'), ('176', 'Juuka'),
    ('177', 'Juupajoki'), ('178', 'Juva'), ('179', 'Jyväskylä'),
    ('181', 'Jämijärvi'), ('182', 'Jämsä'), ('186', 'Järvenpää'),
    ('202', 'Kaarina'), ('204', 'Kaavi'), ('205', 'Kajaani'),
    ('208', 'Kalajoki'), ('211', 'Kangasala'), ('213', 'Kangasniemi'),
    ('214', 'Kankaanpää'), ('216', 'Kannonkoski'), ('217', 'Kannus'),
    ('218', 'Karijoki'), ('224', 'Karkkila'), ('226', 'Karstula'),
    ('230', 'Karvia'), ('231', 'Kaskinen'), ('232', 'Kauhajoki'),
    ('233', 'Kauhava'), ('235', 'Kauniainen'), ('236', 'Kaustinen'),
    ('239', 'Keitele'), ('240', 'Kemi'), ('241', 'Keminmaa'),
    ('244', 'Kempele'), ('245', 'Kerava'), ('249', 'Keuruu'),
    ('250', 'Kihniö'), ('256', 'Kinnula'), ('257', 'Kirkkonummi'),
    ('260', 'Kitee'), ('261', 'Kittilä'), ('263', 'Kiuruvesi'),
    ('265', 'Kivijärvi'), ('271', 'Kokemäki'), ('272', 'Kokkola'),
    ('273', 'Kolari'), ('275', 'Konnevesi'), ('276', 'Kontiolahti'),
    ('280', 'Korsnäs'), ('284', 'Koski Tl'), ('285', 'Kotka'),
    ('286', 'Kouvola'), ('287', 'Kristiinankaupunki'), ('288', 'Kruunupyy'),
    ('295', 'Kuhmo'), ('291', 'Kuhmoinen'), ('297', 'Kuopio'),
    ('300', 'Kuortane'), ('301', 'Kurikka'), ('304', 'Kustavi'),
    ('305', 'Kuusamo'), ('312', 'Kyyjärvi'), ('316', 'Kärkölä'),
    ('317', 'Kärsämäki'), ('318', 'Kökar'), ('320', 'Kemijärvi'),
    ('322', 'Kemiönsaari'), ('398', 'Lahti'), ('399', 'Laihia'),
    ('400', 'Laitila'), ('402', 'Lapinjärvi'), ('403', 'Lapinlahti'),
    ('405', 'Lappajärvi'), ('407', 'Lappeenranta'), ('408', 'Lapinjoki'),
    ('408', 'Lapua'), ('410', 'Laukaa'), ('416', 'Lemi'),
    ('417', 'Lemland'), ('418', 'Lempäälä'), ('420', 'Leppävirta'),
    ('421', 'Lestijärvi'), ('422', 'Lieksa'), ('423', 'Lieto'),
    ('425', 'Liminka'), ('426', 'Liperi'), ('430', 'Loimaa'),
    ('433', 'Loppi'), ('434', 'Loviisa'), ('435', 'Luhanka'),
    ('436', 'Lumijoki'), ('438', 'Lumparland'), ('440', 'Luoto'),
    ('441', 'Luumäki'), ('444', 'Lohja'), ('475', 'Maalahti'),
    ('478', 'Maaninka'), ('480', 'Masku'), ('481', 'Merijärvi'),
    ('483', 'Merikarvia'), ('484', 'Miehikkälä'), ('489', 'Mikkeli'),
    ('491', 'Mikkeli'), ('491', 'Muhos'), ('492', 'Multia'),
    ('494', 'Muonio'), ('495', 'Mustasaari'), ('498', 'Muurame'),
    ('500', 'Mynämäki'), ('503', 'Myrskylä'), ('504', 'Mäntsälä'),
    ('505', 'Mänttä-Vilppula'), ('507', 'Mäntyharju'), ('508', 'Mänttä-Vilppula'),
    ('529', 'Naantali'), ('531', 'Nakkila'), ('535', 'Nivala'),
    ('536', 'Nokia'), ('538', 'Nousiainen'), ('541', 'Nurmes'),
    ('543', 'Nurmijärvi'), ('545', 'Närpiö'), ('560', 'Orimattila'),
    ('561', 'Oripää'), ('562', 'Orivesi'), ('563', 'Oulainen'),
    ('564', 'Oulu'), ('576', 'Outokumpu'), ('577', 'Padasjoki'),
    ('578', 'Paimio'), ('580', 'Paltamo'), ('581', 'Parainen'),
    ('583', 'Pelkosenniemi'), ('584', 'Perho'), ('588', 'Pertunmaa'),
    ('592', 'Petäjävesi'), ('593', 'Pieksämäki'), ('595', 'Pielavesi'),
    ('598', 'Pietarsaari'), ('599', 'Pedersören kunta'), ('601', 'Pihtipudas'),
    ('604', 'Pirkkala'), ('607', 'Polvijärvi'), ('608', 'Pomarkku'),
    ('609', 'Pori'), ('611', 'Pornainen'), ('614', 'Porvoo'),
    ('615', 'Posio'), ('616', 'Pudasjärvi'), ('619', 'Pukkila'),
    ('620', 'Punkalaidun'), ('623', 'Puolanka'), ('624', 'Puumala'),
    ('625', 'Pyhtää'), ('626', 'Pyhäjoki'), ('630', 'Pyhäjärvi'),
    ('631', 'Pyhäntä'), ('635', 'Pyhäranta'), ('636', 'Pälkäne'),
    ('638', 'Pöytyä'), ('678', 'Raahe'), ('680', 'Raisio'),
    ('681', 'Rantasalmi'), ('683', 'Ranua'), ('684', 'Rauma'),
    ('686', 'Rautalampi'), ('687', 'Rautavaara'), ('689', 'Rautjärvi'),
    ('691', 'Reisjärvi'), ('694', 'Riihimäki'), ('697', 'Ristijärvi'),
    ('698', 'Rovaniemi'), ('700', 'Ruokolahti'), ('702', 'Ruovesi'),
    ('704', 'Rusko'), ('707', 'Rääkkylä'), ('710', 'Raasepori'),
    ('729', 'Saarijärvi'), ('732', 'Salla'), ('734', 'Salo'),
    ('736', 'Saltvik'), ('738', 'Sastamala'), ('739', 'Sauvo'),
    ('740', 'Savitaipale'), ('742', 'Savonlinna'), ('743', 'Savukoski'),
    ('746', 'Seinäjoki'), ('747', 'Sievi'), ('748', 'Siikainen'),
    ('749', 'Siikajoki'), ('751', 'Siikalatva'), ('753', 'Sipoo'),
    ('755', 'Siuntio'), ('758', 'Sodankylä'), ('759', 'Soini'),
    ('761', 'Somero'), ('762', 'Sonkajärvi'), ('765', 'Sotkamo'),
    ('766', 'Sottunga'), ('768', 'Sulkava'), ('771', 'Sund'),
    ('777', 'Suomussalmi'), ('778', 'Suonenjoki'), ('781', 'Sysmä'),
    ('783', 'Säkylä'), ('831', 'Taipalsaari'), ('832', 'Taivalkoski'),
    ('833', 'Taivassalo'), ('834', 'Tammela'), ('837', 'Tampere'),
    ('844', 'Tervo'), ('845', 'Tervola'), ('846', 'Teuva'),
    ('848', 'Tohmajärvi'), ('849', 'Toholampi'), ('850', 'Toivakka'),
    ('851', 'Tornio'), ('853', 'Turku'), ('854', 'Pello'),
    ('857', 'Tuusniemi'), ('858', 'Tuusula'), ('859', 'Tyrnävä'),
    ('863', 'Töysä'), ('864', 'Ulvila'), ('886', 'Urjala'),
    ('887', 'Utajärvi'), ('889', 'Utsjoki'), ('890', 'Uurainen'),
    ('892', 'Uusikaarlepyy'), ('893', 'Uusikaupunki'), ('895', 'Vaala'),
    ('905', 'Vaasa'), ('908', 'Valkeakoski'), ('911', 'Valtimo'),
    ('915', 'Varkaus'), ('918', 'Vehmaa'), ('921', 'Vesanto'),
    ('922', 'Vesilahti'), ('924', 'Veteli'), ('925', 'Vieremä'),
    ('927', 'Vihti'), ('931', 'Viitasaari'), ('934', 'Vimpeli'),
    ('935', 'Virolahti'), ('936', 'Virrat'), ('941', 'Vårdö'),
    ('946', 'Vöyri'), ('976', 'Ylitornio'), ('977', 'Ylivieska'),
    ('980', 'Ylöjärvi'), ('981', 'Ypäjä'), ('989', 'Ähtäri'),
    ('992', 'Äänekoski'),
]

BENEFITS = [
    ('Elatustuki', 'Kuukausi'),
    ('Eläke-etuudet (pl. takuueläke)', 'Kuukausi'),
    ('Eläketuki', 'Kuukausi'),
    ('Eläkkeensaajan asumistuki', 'Kuukausi'),
    ('Erityishoitoraha', 'Kuukausi'),
    ('Koulumatkatuki', 'Kuukausi'),
    ('Kuntoutus', 'Kuukausi'),
    ('Kuntoutusraha', 'Kuukausi'),
    ('Lapsilisä', 'Kuukausi'),
    ('Lastenhoidon tuet', 'Kuukausi'),
    ('Lääkeluotto', 'Kuukausi'),
    ('Maahanmuuttajan erityistuki', 'Kuukausi'),
    ('Opintolainahyvitys', 'Kuukausi'),
    ('Opintolainan korkoavustus', 'Kuukausi'),
    ('Opintolainavähennys', 'Kuukausi'),
    ('Opintotuki (opintoraha, asumislisä, lainatakaus)', 'Kuukausi'),
    ('Perhevapaakorvaus', 'Kuukausi'),
    ('Perustoimeentulotuki', 'Kuukausi'),
    ('Sairaanhoitokorvaukset', 'Kuukausi'),
    ('Sairauspäivärahat', 'Kuukausi'),
    ('Sotilasavustus', 'Kuukausi'),
    ('Takuueläke', 'Kuukausi'),
    ('Työttömyysturva', 'Kuukausi'),
    ('Vammaisetuudet', 'Kuukausi'),
    ('Vanhempainpäiväraha', 'Kuukausi'),
    ('Vuosilomakustannuskorvaus', 'Kuukausi'),
    ('Väliaikainen sähkötuki', 'Kuukausi'),
    ('Yleinen asumistuki', 'Kuukausi'),
    ('Äitiysavustus', 'Kuukausi'),
]

NUM_CUSTOMERS = 1000
NUM_PAYMENTS = 10000

def insert_reference_data(conn):
    """Inserts static dimension data: municipalities and benefits."""
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO municipality (municipality_code, municipality_name) VALUES %s ON CONFLICT (municipality_code) DO NOTHING",
            MUNICIPALITIES
        )
        execute_values(
            cur,
            "INSERT INTO benefit (benefit_name, time_type) VALUES %s",
            BENEFITS
        )
    conn.commit()
    print("Reference data (Municipalities, Benefits) inserted.")

def insert_customers(conn) -> list:
    """Generates and inserts customer data, returning a list of customer IDs."""
    customers = []
    used_ssns = set()
    
    while len(customers) < NUM_CUSTOMERS:
        ssn = fake.ssn()
        # Ensure unique SSN and minimum length as per database constraints
        if ssn not in used_ssns and len(ssn) >= 10:
            used_ssns.add(ssn)
            municipality_code = random.choice(MUNICIPALITIES)[0]
            full_name = fake.name()
            customers.append((ssn, full_name, municipality_code))
            
    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO customer (ssn, full_name, municipality_code) VALUES %s",
            customers
        )
        # Fetch all generated customer IDs to link them with payments later
        cur.execute("SELECT customer_id FROM customer")
        customer_ids = [row[0] for row in cur.fetchall()]
        
    conn.commit()
    print(f"Inserted {NUM_CUSTOMERS} customers.")
    return customer_ids

def insert_payments(conn, customer_ids):
    """Generates and inserts random payment transactions for the year 2025."""
    payments = []
    start_date = date(2025, 1, 1)
    end_date = date(2025, 12, 31)
    delta = end_date - start_date

    for _ in range(NUM_PAYMENTS):
        customer_id = random.choice(customer_ids)
        benefit_id = random.randint(1, len(BENEFITS))
        payment_date = start_date + timedelta(days=random.randint(0, delta.days))
        
        # Generate amount between 20.00 and 1500.00, ensuring it's > 0 per constraint
        amount = round(random.uniform(20.0, 1500.0), 2)
        payments.append((customer_id, benefit_id, payment_date, amount))

    with conn.cursor() as cur:
        execute_values(
            cur,
            "INSERT INTO payment_transaction (customer_id, benefit_id, payment_date, amount) VALUES %s",
            payments
        )
    conn.commit()
    print(f"Inserted {NUM_PAYMENTS} payment transactions.")

def main():
    print("Starting data generation process...")
    conn = None
    try:
        conn = get_connection()
        insert_reference_data(conn)
        customer_ids = insert_customers(conn)
        insert_payments(conn, customer_ids)
        print("Data generation completed successfully.")
    except Exception as e:
        print(f"An error occurred during data generation: {e}")
    finally:
        # Guarantee that the connection is closed even if an error occurred above
        if conn is not None and not conn.closed:
            conn.close()
            print("Database connection safely closed.")

if __name__ == "__main__":
    main()