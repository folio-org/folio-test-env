--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'LATIN1';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: diku_login_module; Type: SCHEMA; Schema: -; Owner: diku_login_module
--

CREATE SCHEMA diku_login_module;


ALTER SCHEMA diku_login_module OWNER TO diku_login_module;

--
-- Name: diku_mod_users; Type: SCHEMA; Schema: -; Owner: diku_mod_users
--

CREATE SCHEMA diku_mod_users;


ALTER SCHEMA diku_mod_users OWNER TO diku_mod_users;

--
-- Name: diku_permissions_module; Type: SCHEMA; Schema: -; Owner: diku_permissions_module
--

CREATE SCHEMA diku_permissions_module;


ALTER SCHEMA diku_permissions_module OWNER TO diku_permissions_module;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET search_path = public, pg_catalog;

--
-- Name: update_modified_column_groups(); Type: FUNCTION; Schema: public; Owner: dbuser
--

CREATE FUNCTION update_modified_column_groups() RETURNS trigger
    LANGUAGE plpgsql
    AS $$ BEGIN     NEW.update_date = current_timestamp;     RETURN NEW; END; $$;


ALTER FUNCTION public.update_modified_column_groups() OWNER TO dbuser;

SET search_path = diku_login_module, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_credentials; Type: TABLE; Schema: diku_login_module; Owner: dbuser
--

CREATE TABLE auth_credentials (
    _id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    jsonb jsonb NOT NULL
);


ALTER TABLE auth_credentials OWNER TO dbuser;

SET search_path = diku_mod_users, pg_catalog;

--
-- Name: groups; Type: TABLE; Schema: diku_mod_users; Owner: dbuser
--

CREATE TABLE groups (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    jsonb jsonb NOT NULL,
    creation_date date DEFAULT now() NOT NULL,
    update_date date DEFAULT now() NOT NULL
);


ALTER TABLE groups OWNER TO dbuser;

--
-- Name: users; Type: TABLE; Schema: diku_mod_users; Owner: dbuser
--

CREATE TABLE users (
    id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    jsonb jsonb NOT NULL
);


ALTER TABLE users OWNER TO dbuser;

SET search_path = diku_permissions_module, pg_catalog;

--
-- Name: permissions; Type: TABLE; Schema: diku_permissions_module; Owner: dbuser
--

CREATE TABLE permissions (
    _id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    jsonb jsonb NOT NULL
);


ALTER TABLE permissions OWNER TO dbuser;

--
-- Name: permissions_users; Type: TABLE; Schema: diku_permissions_module; Owner: dbuser
--

CREATE TABLE permissions_users (
    _id uuid DEFAULT public.gen_random_uuid() NOT NULL,
    jsonb jsonb NOT NULL
);


ALTER TABLE permissions_users OWNER TO dbuser;

SET search_path = diku_login_module, pg_catalog;

--
-- Data for Name: auth_credentials; Type: TABLE DATA; Schema: diku_login_module; Owner: dbuser
--

COPY auth_credentials (_id, jsonb) FROM stdin;
acfee48a-b43e-4cdc-a3ba-6ab1928e718c	{"hash": "F4B3659457E73516B84FDA2DD92D69A3A76770FB", "salt": "B4FF9E7BD0AE71A04CA3978483CCB2A20111BC94", "username": "jill"}
b1e2e3cf-1a97-4484-8930-e73b736eff75	{"hash": "F4B3659457E73516B84FDA2DD92D69A3A76770FB", "salt": "B4FF9E7BD0AE71A04CA3978483CCB2A20111BC94", "username": "shane"}
40a8dd31-5ff6-4519-a428-0d9bcca82d2f	{"hash": "C8C38072D79AD0C97E3FFA11FF0BDF4A4B9128D3", "salt": "F255821CEB07287F673FA9BC54482CF4B1104D69", "username": "joe"}
\.


SET search_path = diku_mod_users, pg_catalog;

--
-- Data for Name: groups; Type: TABLE DATA; Schema: diku_mod_users; Owner: dbuser
--

COPY groups (id, jsonb, creation_date, update_date) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: diku_mod_users; Owner: dbuser
--

COPY users (id, jsonb) FROM stdin;
76b422c8-f271-45fd-ac04-4a48e8be174c	{"id": "0001", "active": true, "username": "jill"}
da2b36d0-9981-4ceb-bb33-e4c895d38927	{"id": "0003", "active": true, "username": "joe"}
2118dc0c-538a-4672-8063-88e5152897ee	{"id": "0002", "active": true, "username": "shane"}
\.


SET search_path = diku_permissions_module, pg_catalog;


--
-- Data for Name: permissions_users; Type: TABLE DATA; Schema: diku_permissions_module; Owner: dbuser
--

COPY permissions_users (_id, jsonb) FROM stdin;
49d17eb7-0ac0-4e67-9e21-41b0364b9f68	{"username": "jack", "permissions": ["thing.read"]}
0a1fcb83-9806-4459-a601-ca75e9551460	{"username": "jill", "permissions": ["thing.read", "thing.see_sensitive", "thing.create", "thing.delete"]}
6d8b21ea-6a34-4d73-8ab8-8c58f8e6c148	{"username": "joe", "permissions": []}
5b5d6eb9-77e7-4589-879d-f25ae80a1b1f	{"username": "shane", "permissions": ["perms.users", "perms.permissions", "login", "users.read", "users.create", "users.edit", "users.delete", "usergroups.read", "usergroups.create", "usergroups.edit", "usergroups.delete", "users.read.basic"]}
\.


SET search_path = diku_login_module, pg_catalog;

--
-- Name: auth_credentials_pkey; Type: CONSTRAINT; Schema: diku_login_module; Owner: dbuser
--

ALTER TABLE ONLY auth_credentials
    ADD CONSTRAINT auth_credentials_pkey PRIMARY KEY (_id);


SET search_path = diku_mod_users, pg_catalog;

--
-- Name: groups_pkey; Type: CONSTRAINT; Schema: diku_mod_users; Owner: dbuser
--

ALTER TABLE ONLY groups
    ADD CONSTRAINT groups_pkey PRIMARY KEY (id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: diku_mod_users; Owner: dbuser
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


SET search_path = diku_permissions_module, pg_catalog;

--
-- Name: permissions_pkey; Type: CONSTRAINT; Schema: diku_permissions_module; Owner: dbuser
--

ALTER TABLE ONLY permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (_id);


--
-- Name: permissions_users_pkey; Type: CONSTRAINT; Schema: diku_permissions_module; Owner: dbuser
--

ALTER TABLE ONLY permissions_users
    ADD CONSTRAINT permissions_users_pkey PRIMARY KEY (_id);


SET search_path = diku_mod_users, pg_catalog;

--
-- Name: group_unique_idx; Type: INDEX; Schema: diku_mod_users; Owner: dbuser
--

CREATE UNIQUE INDEX group_unique_idx ON groups USING btree (((jsonb ->> 'group'::text)));


--
-- Name: idxgin_groups; Type: INDEX; Schema: diku_mod_users; Owner: dbuser
--

CREATE INDEX idxgin_groups ON groups USING gin (jsonb jsonb_path_ops);


--
-- Name: update_date_groups; Type: TRIGGER; Schema: diku_mod_users; Owner: dbuser
--

CREATE TRIGGER update_date_groups BEFORE UPDATE ON groups FOR EACH ROW EXECUTE PROCEDURE public.update_modified_column_groups();


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


SET search_path = diku_login_module, pg_catalog;

--
-- Name: auth_credentials; Type: ACL; Schema: diku_login_module; Owner: dbuser
--

REVOKE ALL ON TABLE auth_credentials FROM PUBLIC;
REVOKE ALL ON TABLE auth_credentials FROM dbuser;
GRANT ALL ON TABLE auth_credentials TO dbuser;
GRANT ALL ON TABLE auth_credentials TO diku_login_module;


SET search_path = diku_mod_users, pg_catalog;

--
-- Name: groups; Type: ACL; Schema: diku_mod_users; Owner: dbuser
--

REVOKE ALL ON TABLE groups FROM PUBLIC;
REVOKE ALL ON TABLE groups FROM dbuser;
GRANT ALL ON TABLE groups TO dbuser;
GRANT ALL ON TABLE groups TO diku_mod_users;


--
-- Name: users; Type: ACL; Schema: diku_mod_users; Owner: dbuser
--

REVOKE ALL ON TABLE users FROM PUBLIC;
REVOKE ALL ON TABLE users FROM dbuser;
GRANT ALL ON TABLE users TO dbuser;
GRANT ALL ON TABLE users TO diku_mod_users;


SET search_path = diku_permissions_module, pg_catalog;

--
-- Name: permissions; Type: ACL; Schema: diku_permissions_module; Owner: dbuser
--

REVOKE ALL ON TABLE permissions FROM PUBLIC;
REVOKE ALL ON TABLE permissions FROM dbuser;
GRANT ALL ON TABLE permissions TO dbuser;
GRANT ALL ON TABLE permissions TO diku_permissions_module;


--
-- Name: permissions_users; Type: ACL; Schema: diku_permissions_module; Owner: dbuser
--

REVOKE ALL ON TABLE permissions_users FROM PUBLIC;
REVOKE ALL ON TABLE permissions_users FROM dbuser;
GRANT ALL ON TABLE permissions_users TO dbuser;
GRANT ALL ON TABLE permissions_users TO diku_permissions_module;


--
-- PostgreSQL database dump complete
--

