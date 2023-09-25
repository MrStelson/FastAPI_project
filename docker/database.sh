#!/bin/bash

psql -p "5430" -U "postgres" -d "postgres" -c "INSERT INTO app_role (name) VALUES ('user'), ('moderator'), ('admin');"
psql -p "5430" -U "postgres" -d "postgres" -c "INSERT INTO app_user (email, username, role_id, hashed_password, is_active, is_superuser, is_verified, is_banned) VALUES ('admin@mail.com', 'Admin', '3', '\$2b\$12\$hRobDSXAV/ssXOvLXu5I9eceU8or1cp.n4/mIma7DnUAf1aj8WRrS', True, False, False, False);"
psql -p "5430" -U "postgres" -d "postgres" -c "INSERT INTO ad_type (type_name) VALUES ('Работа'), ('Услуги'), ('Одежда'), ('Красота'), ('Запчасти');"
psql -p "5430" -U "postgres" -d "postgres" -c "INSERT INTO ad_category (category_name, type_id) VALUES ('Ищу работу', 1), ('Ищу сотрудника', 1), ('Транспорт и перевозки', 2), ('Ремнот и отделка', 2), ('Строительство', 2), ('Обучение и курсы', 2), ('Для мужчин', 3), ('Для женщин', 3), ('Для детей', 3), ('Маникюр, педикюр', 4), ('Услуги парикмахера', 4), ('Ресницы, брови', 4), ('Шины, диски', 5), ('Тормозная система', 5), ('Трансмиссия', 5);"
