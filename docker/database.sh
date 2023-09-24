#!/bin/bash

psql -h localhost -p 5430 -t -U postgres -d postgres -c "insert into app_role (name) values ('user'), ('moderator'), ('admin')"
psql -h localhost -p 5430 -t -U postgres -d postgres -c "insert into app_user (email, username, role_id, hashed_password, is_active, is_superuser, is_verified, is_banned) values ('admin@mail.com', 'Admin', '3', '\$2b\$12\$hRobDSXAV/ssXOvLXu5I9eceU8or1cp.n4/mIma7DnUAf1aj8WRrS', True, False, False, False);"