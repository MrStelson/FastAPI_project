CREATE TABLE ad_type (
    id SERIAL NOT NULL,
    type_name VARCHAR NOT NULL,
    slug VARCHAR NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (slug),
    UNIQUE (type_name)
);

CREATE TABLE app_role (
    id SERIAL NOT NULL,
    name VARCHAR NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE ad_category (
    id SERIAL NOT NULL,
    category_name VARCHAR NOT NULL,
    slug VARCHAR NOT NULL,
    type_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(type_id) REFERENCES ad_type (id),
    UNIQUE (category_name),
    UNIQUE (slug)
);

CREATE TABLE app_user (
    id SERIAL NOT NULL,
    email VARCHAR NOT NULL,
    username VARCHAR NOT NULL,
    registered_at TIMESTAMP WITHOUT TIME ZONE,
    role_id INTEGER,
    hashed_password VARCHAR(1024) NOT NULL,
    is_active BOOLEAN NOT NULL,
    is_superuser BOOLEAN NOT NULL,
    is_verified BOOLEAN NOT NULL,
    is_banned BOOLEAN NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(role_id) REFERENCES app_role (id)
);

CREATE TABLE ad (
    id SERIAL NOT NULL,
    name VARCHAR NOT NULL,
    description VARCHAR,
    price VARCHAR,
    user_id INTEGER,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE,
    category_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(category_id) REFERENCES ad_category (id)
);

CREATE TABLE ad_comment (
    id SERIAL NOT NULL,
    value VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE,
    user_id INTEGER,
    ad_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(ad_id) REFERENCES ad (id)
);

CREATE TABLE ad_complaint (
    id SERIAL NOT NULL,
    value VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE,
    user_id INTEGER,
    ad_id INTEGER,
    PRIMARY KEY (id),
    FOREIGN KEY(ad_id) REFERENCES ad (id)
);

INSERT INTO app_role (name)
VALUES ('user'), ('moderator'), ('admin');

INSERT INTO app_user (email, username, role_id, hashed_password, is_active, is_superuser, is_verified, is_banned)
VALUES ('admin@mail.com', 'Admin', '3', '$2b$12$hRobDSXAV/ssXOvLXu5I9eceU8or1cp.n4/mIma7DnUAf1aj8WRrS', True, False, False, False);

INSERT INTO ad_type (type_name, slug)
VALUES ('Работа', 'rabota'), ('Услуги', 'uslugi'), ('Одежда', 'odejda'), ('Красота', 'krasota'), ('Запчасти', 'zapchasti');

INSERT INTO ad_category (category_name, type_id, slug)
VALUES ('Ищу работу', 1, 'ishu-rabotu'), ('Ищу сотрудника', 1, 'ishu-sotrudnika'), ('Транспорт и перевозки', 2, 'transport-perevozki'), ('Ремонт и отделка', 2, 'remont-otdelka'), ('Строительство', 2, 'stroitelstvo'), ('Обучение и курсы', 2, 'obuchenie-kursi'), ('Для мужчин', 3, 'for-men'), ('Для женщин', 3, 'for-women'), ('Для детей', 3, 'for-child'), ('Маникюр, педикюр', 4, 'manikur-pedikur'), ('Услуги парикмахера', 4, 'uslugi-parikmakher'), ('Ресницы, брови', 4, 'resnici-brovi'), ('Шины, диски', 5, 'shini-diski'), ('Тормозная система', 5, 'tormoznay-sistema'), ('Трансмиссия', 5, 'transmisia');