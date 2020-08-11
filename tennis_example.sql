--
-- PostgreSQL database dump
--

-- Dumped from database version 10.12 (Ubuntu 10.12-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.12 (Ubuntu 10.12-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO nikita;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO nikita;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO nikita;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO nikita;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO nikita;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO nikita;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: base_channel; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.base_channel (
    id integer NOT NULL,
    name character varying(64) NOT NULL,
    username character varying(64) NOT NULL,
    code character varying(32) NOT NULL,
    token character varying(256) NOT NULL
);


ALTER TABLE public.base_channel OWNER TO nikita;

--
-- Name: base_channel_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.base_channel_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_channel_id_seq OWNER TO nikita;

--
-- Name: base_channel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.base_channel_id_seq OWNED BY public.base_channel.id;


--
-- Name: base_grouptrainingday; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.base_grouptrainingday (
    id integer NOT NULL,
    date date NOT NULL,
    is_available boolean NOT NULL,
    start_time time without time zone,
    duration interval,
    group_id integer NOT NULL
);


ALTER TABLE public.base_grouptrainingday OWNER TO nikita;

--
-- Name: base_grouptrainingday_absent; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.base_grouptrainingday_absent (
    id integer NOT NULL,
    grouptrainingday_id integer NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.base_grouptrainingday_absent OWNER TO nikita;

--
-- Name: base_grouptrainingday_absent_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.base_grouptrainingday_absent_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_grouptrainingday_absent_id_seq OWNER TO nikita;

--
-- Name: base_grouptrainingday_absent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.base_grouptrainingday_absent_id_seq OWNED BY public.base_grouptrainingday_absent.id;


--
-- Name: base_grouptrainingday_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.base_grouptrainingday_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_grouptrainingday_id_seq OWNER TO nikita;

--
-- Name: base_grouptrainingday_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.base_grouptrainingday_id_seq OWNED BY public.base_grouptrainingday.id;


--
-- Name: base_grouptrainingday_visitors; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.base_grouptrainingday_visitors (
    id integer NOT NULL,
    grouptrainingday_id integer NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.base_grouptrainingday_visitors OWNER TO nikita;

--
-- Name: base_grouptrainingday_visitors_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.base_grouptrainingday_visitors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_grouptrainingday_visitors_id_seq OWNER TO nikita;

--
-- Name: base_grouptrainingday_visitors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.base_grouptrainingday_visitors_id_seq OWNED BY public.base_grouptrainingday_visitors.id;


--
-- Name: base_tarif; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.base_tarif (
    id integer NOT NULL,
    price_per_hour integer NOT NULL,
    name character varying(64)
);


ALTER TABLE public.base_tarif OWNER TO nikita;

--
-- Name: base_tarif_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.base_tarif_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_tarif_id_seq OWNER TO nikita;

--
-- Name: base_tarif_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.base_tarif_id_seq OWNED BY public.base_tarif.id;


--
-- Name: base_traininggroup; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.base_traininggroup (
    id integer NOT NULL,
    dttm_added timestamp with time zone NOT NULL,
    dttm_deleted timestamp with time zone,
    name character varying(32) NOT NULL,
    max_players smallint NOT NULL,
    tarif_id integer
);


ALTER TABLE public.base_traininggroup OWNER TO nikita;

--
-- Name: base_traininggroup_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.base_traininggroup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_traininggroup_id_seq OWNER TO nikita;

--
-- Name: base_traininggroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.base_traininggroup_id_seq OWNED BY public.base_traininggroup.id;


--
-- Name: base_traininggroup_users; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.base_traininggroup_users (
    id integer NOT NULL,
    traininggroup_id integer NOT NULL,
    user_id bigint NOT NULL
);


ALTER TABLE public.base_traininggroup_users OWNER TO nikita;

--
-- Name: base_traininggroup_user_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.base_traininggroup_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_traininggroup_user_id_seq OWNER TO nikita;

--
-- Name: base_traininggroup_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.base_traininggroup_user_id_seq OWNED BY public.base_traininggroup_users.id;


--
-- Name: base_user; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.base_user (
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    username character varying(150) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    id bigint NOT NULL,
    telegram_username character varying(64),
    first_name character varying(32),
    phone_number character varying(16),
    is_superuser boolean NOT NULL,
    is_blocked boolean NOT NULL,
    status character varying(1) NOT NULL,
    time_before_cancel interval,
    bonus_lesson smallint,
    add_info character varying(128)
);


ALTER TABLE public.base_user OWNER TO nikita;

--
-- Name: base_user_groups; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.base_user_groups (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.base_user_groups OWNER TO nikita;

--
-- Name: base_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.base_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_user_groups_id_seq OWNER TO nikita;

--
-- Name: base_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.base_user_groups_id_seq OWNED BY public.base_user_groups.id;


--
-- Name: base_user_user_permissions; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.base_user_user_permissions (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.base_user_user_permissions OWNER TO nikita;

--
-- Name: base_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.base_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_user_user_permissions_id_seq OWNER TO nikita;

--
-- Name: base_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.base_user_user_permissions_id_seq OWNED BY public.base_user_user_permissions.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id bigint NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO nikita;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO nikita;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO nikita;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO nikita;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO nikita;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: nikita
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO nikita;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: nikita
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: nikita
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO nikita;

--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: base_channel id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_channel ALTER COLUMN id SET DEFAULT nextval('public.base_channel_id_seq'::regclass);


--
-- Name: base_grouptrainingday id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday ALTER COLUMN id SET DEFAULT nextval('public.base_grouptrainingday_id_seq'::regclass);


--
-- Name: base_grouptrainingday_absent id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_absent ALTER COLUMN id SET DEFAULT nextval('public.base_grouptrainingday_absent_id_seq'::regclass);


--
-- Name: base_grouptrainingday_visitors id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_visitors ALTER COLUMN id SET DEFAULT nextval('public.base_grouptrainingday_visitors_id_seq'::regclass);


--
-- Name: base_tarif id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_tarif ALTER COLUMN id SET DEFAULT nextval('public.base_tarif_id_seq'::regclass);


--
-- Name: base_traininggroup id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_traininggroup ALTER COLUMN id SET DEFAULT nextval('public.base_traininggroup_id_seq'::regclass);


--
-- Name: base_traininggroup_users id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_traininggroup_users ALTER COLUMN id SET DEFAULT nextval('public.base_traininggroup_user_id_seq'::regclass);


--
-- Name: base_user_groups id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_user_groups ALTER COLUMN id SET DEFAULT nextval('public.base_user_groups_id_seq'::regclass);


--
-- Name: base_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.base_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add content type	4	add_contenttype
11	Can change content type	4	change_contenttype
12	Can delete content type	4	delete_contenttype
13	Can add session	5	add_session
14	Can change session	5	change_session
15	Can delete session	5	delete_session
16	Can add user	6	add_user
17	Can change user	6	change_user
18	Can delete user	6	delete_user
19	Can add group training day	7	add_grouptrainingday
20	Can change group training day	7	change_grouptrainingday
21	Can delete group training day	7	delete_grouptrainingday
22	Can add tarif	8	add_tarif
23	Can change tarif	8	change_tarif
24	Can delete tarif	8	delete_tarif
25	Can add training group	9	add_traininggroup
26	Can change training group	9	change_traininggroup
27	Can delete training group	9	delete_traininggroup
28	Can add channel	10	add_channel
29	Can change channel	10	change_channel
30	Can delete channel	10	delete_channel
\.


--
-- Data for Name: base_channel; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.base_channel (id, name, username, code, token) FROM stdin;
1	TestTennisTulaBot	TestTennisTulaBot	tennis	1224814504:AAFsEymeCAygTKKx3NiBLStffgAon0bx2hM
2	admin tennis	TestAdminTennisTulaBot	admin	1159521643:AAGNeanoIy6y5_W62c2P6kgdDsx73aPrfIw
\.


--
-- Data for Name: base_grouptrainingday; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.base_grouptrainingday (id, date, is_available, start_time, duration, group_id) FROM stdin;
1	2020-07-14	t	09:30:00	01:30:00	1
222	2020-07-16	t	16:30:00	01:30:00	1
223	2020-07-23	t	16:30:00	01:30:00	1
232	2020-07-25	t	16:30:00	01:30:00	1795
231	2020-07-18	t	16:30:00	01:30:00	1795
297	2020-08-13	t	18:00:00	01:00:00	1796
300	2020-09-03	t	18:00:00	01:00:00	1796
301	2020-09-10	t	18:00:00	01:00:00	1796
302	2020-09-17	t	18:00:00	01:00:00	1796
303	2020-09-24	t	18:00:00	01:00:00	1796
304	2020-10-01	t	18:00:00	01:00:00	1796
323	2020-07-30	t	16:30:00	01:30:00	1
328	2020-09-03	t	16:30:00	01:30:00	1
329	2020-09-10	t	16:30:00	01:30:00	1
330	2020-09-17	t	16:30:00	01:30:00	1
331	2020-09-24	t	16:30:00	01:30:00	1
296	2020-08-06	t	18:00:00	01:00:00	1796
352	2020-08-13	t	10:00:00	01:00:00	1801
353	2020-08-20	t	10:00:00	01:00:00	1801
393	2020-08-19	t	18:00:00	02:00:00	1803
325	2020-08-13	t	17:00:00	01:00:00	1
326	2020-08-20	t	16:30:00	01:30:00	1
327	2020-08-27	t	16:30:00	01:30:00	1
299	2020-08-27	t	18:00:00	01:00:00	1796
354	2020-08-27	t	10:00:00	01:00:00	1801
355	2020-09-03	t	10:00:00	01:00:00	1801
332	2020-08-01	t	18:00:00	01:00:00	1797
298	2020-08-20	t	18:00:00	01:00:00	1796
334	2020-08-12	t	09:30:00	01:00:00	1801
335	2020-08-19	t	09:30:00	01:00:00	1801
336	2020-08-26	t	09:30:00	01:00:00	1801
338	2020-09-09	t	09:30:00	01:00:00	1801
339	2020-09-16	t	09:30:00	01:00:00	1801
340	2020-09-23	t	09:30:00	01:00:00	1801
341	2020-09-30	t	09:30:00	01:00:00	1801
356	2020-09-10	t	10:00:00	01:00:00	1801
357	2020-09-17	t	10:00:00	01:00:00	1801
358	2020-09-24	t	10:00:00	01:00:00	1801
359	2020-10-01	t	10:00:00	01:00:00	1801
360	2020-08-06	t	11:00:00	01:00:00	1797
337	2020-09-02	t	09:30:00	01:00:00	1801
351	2020-08-06	t	10:00:00	01:00:00	1801
333	2020-08-05	t	09:30:00	01:00:00	1801
342	2020-09-11	t	18:00:00	01:00:00	1
343	2020-09-18	t	18:00:00	01:00:00	1
344	2020-09-25	t	18:00:00	01:00:00	1
345	2020-10-02	t	18:00:00	01:00:00	1
346	2020-10-09	t	18:00:00	01:00:00	1
347	2020-10-16	t	18:00:00	01:00:00	1
348	2020-10-23	t	18:00:00	01:00:00	1
349	2020-10-30	t	18:00:00	01:00:00	1
350	2020-11-06	t	18:00:00	01:00:00	1
363	2020-08-16	t	10:30:00	01:00:00	1796
364	2020-08-23	t	10:30:00	01:00:00	1796
365	2020-08-30	t	10:30:00	01:00:00	1796
366	2020-09-06	t	10:30:00	01:00:00	1796
367	2020-09-13	t	10:30:00	01:00:00	1796
368	2020-09-20	t	10:30:00	01:00:00	1796
369	2020-09-27	t	10:30:00	01:00:00	1796
324	2020-08-06	t	16:30:00	01:30:00	1
362	2020-08-09	t	13:00:00	01:00:00	1796
361	2020-08-06	t	13:00:00	01:00:00	1796
370	2020-08-09	t	12:00:00	01:00:00	1801
371	2020-08-16	t	12:00:00	01:00:00	1801
372	2020-08-23	t	12:00:00	01:00:00	1801
373	2020-08-30	t	12:00:00	01:00:00	1801
374	2020-09-06	t	12:00:00	01:00:00	1801
375	2020-09-13	t	12:00:00	01:00:00	1801
376	2020-09-20	t	12:00:00	01:00:00	1801
377	2020-09-27	t	12:00:00	01:00:00	1801
378	2020-10-04	t	12:00:00	01:00:00	1801
379	2020-08-09	t	18:00:00	01:00:00	1802
380	2020-08-09	t	10:30:00	01:30:00	1797
381	2020-08-12	t	10:30:00	01:30:00	1796
382	2020-08-19	t	10:30:00	01:30:00	1796
383	2020-08-26	t	10:30:00	01:30:00	1796
384	2020-09-02	t	10:30:00	01:30:00	1796
385	2020-09-09	t	10:30:00	01:30:00	1796
386	2020-09-16	t	10:30:00	01:30:00	1796
387	2020-09-23	t	10:30:00	01:30:00	1796
388	2020-09-30	t	10:30:00	01:30:00	1796
389	2020-10-07	t	10:30:00	01:30:00	1796
390	2020-08-16	t	15:30:00	01:30:00	1803
\.


--
-- Data for Name: base_grouptrainingday_absent; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.base_grouptrainingday_absent (id, grouptrainingday_id, user_id) FROM stdin;
1	232	350490234
2	231	350490234
7	331	350490234
8	323	350490234
10	329	350490234
15	299	2
19	326	350490234
\.


--
-- Data for Name: base_grouptrainingday_visitors; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.base_grouptrainingday_visitors (id, grouptrainingday_id, user_id) FROM stdin;
6	337	3
7	337	340961092
8	333	3
9	333	340961092
10	333	350490234
11	296	4
12	351	123
13	351	3
15	329	350490234
16	356	350490234
17	325	638303006
18	324	638303006
\.


--
-- Data for Name: base_tarif; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.base_tarif (id, price_per_hour, name) FROM stdin;
3	1400	Individual
2	600	Freelancer
1	400	Group
\.


--
-- Data for Name: base_traininggroup; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.base_traininggroup (id, dttm_added, dttm_deleted, name, max_players, tarif_id) FROM stdin;
1	2020-07-14 15:50:45+03	\N	Первая	6	1
1795	2020-07-15 01:32:05.307189+03	\N	Группа Никита Шамаев	1	2
1797	2020-07-31 02:34:53.959762+03	\N	ОльгаШамаева	1	2
1796	2020-07-29 14:57:39.541131+03	\N	вторая	4	1
1801	2020-08-01 14:36:58.539676+03	\N	третья	4	1
1802	2020-08-03 23:07:27.490678+03	\N	БабаЯга	1	2
1803	2020-08-11 11:00:09.632172+03	\N	НикитаШамаев	1	\N
\.


--
-- Data for Name: base_traininggroup_users; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.base_traininggroup_users (id, traininggroup_id, user_id) FROM stdin;
1	1	1
2	1	2
3	1	3
4	1	4
15	1	350490234
16	1795	350490234
17	1796	123
18	1796	22
19	1797	340961092
21	1796	340961092
24	1801	1
25	1801	2
26	1801	638303006
27	1802	2
\.


--
-- Data for Name: base_user; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.base_user (password, last_login, username, last_name, email, is_staff, is_active, date_joined, id, telegram_username, first_name, phone_number, is_superuser, is_blocked, status, time_before_cancel, bonus_lesson, add_info) FROM stdin;
1	\N	340961092	Шамаева		f	t	2020-07-31 01:15:45+03	340961092	\N	Ольга	89611469010	f	f	A	02:00:00	1	\N
1	\N	638303006	Юрков		f	t	2020-08-02 21:26:53.659073+03	638303006	VladlenYS	Владлен	89039600906	f	f	G	03:00:00	2	\N
1	\N	123	dddd		f	t	2020-07-29 14:55:26+03	123	\N	aaaaaaaaaaaaaaa	787978987987	f	f	T	00:00:02	0	\N
11	\N	22			f	t	2020-07-29 14:56:20+03	22	\N	klfflkfkk	1213213214	f	f	T	00:00:23	0	\N
1	\N	3			f	t	2020-07-14 15:49:23+03	3	\N	фыв	444444	f	t	T	00:00:20	0	\N
1	\N	4	asd		f	t	2020-07-14 15:50:08+03	4	\N	Кошка	789	f	t	T	00:00:00	0	\N
1	\N	2	Яга		f	t	2020-07-14 15:48:58+03	2	\N	Баба	214141	f	t	A	00:00:14	0	\N
1	\N	1	asd		f	t	2020-07-14 15:48:23+03	1	\N	Крекс	789456	f	t	W	00:02:30	0	\N
pbkdf2_sha256$100000$KQ87ID09qeE9$uqHZg8uVMnjd1itviF59KxJFF04tvDPyXdBCyBzOhDA=	2020-08-11 10:51:51.968844+03	350490234	Шамаев		t	t	2020-07-15 15:13:23+03	350490234	shamaevnn	Никита	89661215215	t	f	G	01:00:00	8	\N
\.


--
-- Data for Name: base_user_groups; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.base_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: base_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.base_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
181	2020-07-15 17:53:49.243986+03	1	Первая, Group -- 400 руб./час	2	[{"changed": {"fields": ["users"]}}]	9	350490234
182	2020-07-15 18:15:50.530932+03	1795	БабаЯга, Freelancer -- 600 руб./час	2	[{"changed": {"fields": ["users"]}}]	9	350490234
183	2020-07-15 18:16:24.792302+03	231	Группа: БабаЯга, Freelancer -- 600 руб./час, дата тренировки 2020-07-18, время начала: 16:30:00	1	[{"added": {}}]	7	350490234
184	2020-07-15 18:18:13.908116+03	232	Группа: БабаЯга, Freelancer -- 600 руб./час, дата тренировки 2020-07-25, время начала: 16:30:00	1	[{"added": {}}]	7	350490234
185	2020-07-15 18:23:03.838098+03	1795	Группа Никита Шамаев, Freelancer -- 600 руб./час	2	[{"changed": {"fields": ["name"]}}]	9	350490234
186	2020-07-15 18:55:23.185217+03	232	Группа: Группа Никита Шамаев, Freelancer -- 600 руб./час, дата тренировки 2020-07-25, время начала: 16:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
187	2020-07-16 00:21:35.544294+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["last_name", "first_name", "time_before_cancel"]}}]	6	350490234
188	2020-07-16 14:17:09.068071+03	231	Группа: Группа Никита Шамаев, Freelancer -- 600 руб./час, дата тренировки 2020-07-18, время начала: 16:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
189	2020-07-29 14:56:09.779706+03	123	aaaaaaaaaaaaaaa dddd -- 787978987987	1	[{"added": {}}]	6	350490234
190	2020-07-29 14:57:15.039152+03	22	klfflkfkk  -- 1213213214	1	[{"added": {}}]	6	350490234
191	2020-07-29 14:57:39.870039+03	1796	вторая, Group -- 400 руб./час	1	[{"added": {}}]	9	350490234
192	2020-07-29 15:29:50.152906+03	233	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-30, время начала: 18:01:00	1	[{"added": {}}]	7	350490234
193	2020-07-29 15:31:04.389621+03	233	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-30, время начала: 18:01:00	3		7	350490234
194	2020-07-29 16:17:00.528714+03	242	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 18:01:00	1	[{"added": {}}]	7	350490234
195	2020-07-29 16:17:17.261348+03	242	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 18:01:00	3		7	350490234
196	2020-07-29 16:17:40.591076+03	251	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:01:00	1	[{"added": {}}]	7	350490234
197	2020-07-29 16:19:19.503063+03	251	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:01:00	3		7	350490234
198	2020-07-29 16:19:59.024645+03	260	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
199	2020-07-29 16:20:26.588889+03	260	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:00:00	3		7	350490234
200	2020-07-29 16:20:51.716646+03	269	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
201	2020-07-29 16:21:09.812155+03	269	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:00:00	3		7	350490234
202	2020-07-29 16:21:46.04546+03	278	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 13:21:41	1	[{"added": {}}]	7	350490234
203	2020-07-29 16:22:04.105621+03	278	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 13:21:41	3		7	350490234
204	2020-07-29 16:22:23.03196+03	287	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
205	2020-07-29 16:23:15.461262+03	287	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 18:00:00	3		7	350490234
206	2020-07-29 16:48:41.106707+03	296	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
207	2020-07-29 17:53:58.75841+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["time_before_cancel"]}}]	6	350490234
208	2020-07-29 18:39:39.424766+03	224	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-07-30, время начала: 16:30:00	3		7	350490234
209	2020-07-29 18:40:00.928137+03	305	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-07-30, время начала: 16:30:00	1	[{"added": {}}]	7	350490234
210	2020-07-29 18:40:18.125626+03	305	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-07-30, время начала: 16:30:00	3		7	350490234
211	2020-07-29 18:40:44.21475+03	314	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 16:30:00	1	[{"added": {}}]	7	350490234
212	2020-07-29 18:41:43.662042+03	314	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-07-29, время начала: 16:30:00	3		7	350490234
213	2020-07-29 18:42:31.337441+03	323	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-07-30, время начала: 16:30:00	1	[{"added": {}}]	7	350490234
214	2020-07-30 16:04:18.749461+03	325	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-13, время начала: 15:30:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
215	2020-07-30 16:15:34.609484+03	325	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-13, время начала: 17:00:00	2	[{"changed": {"fields": ["start_time", "duration"]}}]	7	350490234
216	2020-07-30 16:17:14.653323+03	325	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-13, время начала: 17:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
217	2020-07-30 16:17:23.714175+03	325	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-13, время начала: 17:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
218	2020-07-30 16:44:50.555148+03	324	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 16:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
219	2020-07-30 16:44:55.749234+03	325	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-13, время начала: 17:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
220	2020-07-30 16:45:00.746365+03	326	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-20, время начала: 16:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
221	2020-07-30 16:45:07.73912+03	327	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-27, время начала: 16:30:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
222	2020-07-30 16:55:19.605982+03	299	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-27, время начала: 18:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
223	2020-07-31 01:43:39.182096+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["time_before_cancel"]}}]	6	350490234
224	2020-07-31 01:46:12.001261+03	340961092	Ольга Шамаева -- 89611469010	2	[]	6	350490234
225	2020-07-31 02:05:47.114864+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["status"]}}]	6	350490234
226	2020-07-31 02:06:19.159857+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["status"]}}]	6	350490234
227	2020-07-31 02:06:48.045398+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["status"]}}]	6	350490234
228	2020-07-31 02:07:07.260509+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["status"]}}]	6	350490234
229	2020-07-31 02:07:15.461182+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["status"]}}]	6	350490234
230	2020-07-31 02:34:53.963473+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["status"]}}]	6	350490234
231	2020-07-31 02:36:03.600566+03	332	Группа: ОльгаШамаева, Freelancer -- 600 руб./час, дата тренировки 2020-07-31, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
232	2020-07-31 02:38:59.017102+03	332	Группа: ОльгаШамаева, Freelancer -- 600 руб./час, дата тренировки 2020-07-31, время начала: 18:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
233	2020-07-31 02:41:06.144297+03	332	Группа: ОльгаШамаева, Freelancer -- 600 руб./час, дата тренировки 2020-08-01, время начала: 18:00:00	2	[{"changed": {"fields": ["date"]}}]	7	350490234
234	2020-07-31 02:42:01.993112+03	1796	вторая, Group -- 400 руб./час	2	[{"changed": {"fields": ["users"]}}]	9	350490234
235	2020-07-31 02:42:28.913707+03	1796	вторая, Group -- 400 руб./час	2	[]	9	350490234
236	2020-07-31 02:52:37.644662+03	296	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:00:00	2	[{"changed": {"fields": ["absent"]}}]	7	350490234
237	2020-07-31 02:53:07.901936+03	332	Группа: ОльгаШамаева, Freelancer -- 600 руб./час, дата тренировки 2020-08-01, время начала: 18:00:00	2	[]	7	350490234
238	2020-07-31 03:23:52.371782+03	340961092	Ольга Шамаева -- 89611469010	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	6	350490234
239	2020-08-01 14:16:42.647924+03	1799	лёдИ, Freelancer -- 600 руб./час	3		9	350490234
240	2020-08-01 14:16:56.746403+03	1800	ОльгаШамаева, Freelancer -- 600 руб./час	3		9	350490234
241	2020-08-01 14:16:56.76935+03	1798	ОльгаШамаева, Freelancer -- 600 руб./час	3		9	350490234
242	2020-08-01 14:19:24.858667+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
243	2020-08-01 14:19:30.778744+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["bonus_lesson"]}}]	6	350490234
244	2020-08-01 14:29:09.008756+03	298	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-20, время начала: 18:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
245	2020-08-01 14:36:58.548039+03	1801	третья, Group -- 400 руб./час	1	[{"added": {}}]	9	350490234
246	2020-08-01 14:37:58.885142+03	333	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-05, время начала: 09:30:00	1	[{"added": {}}]	7	350490234
247	2020-08-01 14:38:39.670246+03	333	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-05, время начала: 09:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
248	2020-08-01 14:45:26.805383+03	333	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-05, время начала: 09:30:00	2	[]	7	350490234
249	2020-08-01 14:47:53.765197+03	333	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-05, время начала: 09:30:00	2	[]	7	350490234
250	2020-08-01 14:53:20.314983+03	337	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-09-02, время начала: 09:30:00	2	[{"changed": {"fields": ["absent", "visitors"]}}]	7	350490234
251	2020-08-01 14:53:32.254336+03	337	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-09-02, время начала: 09:30:00	2	[{"changed": {"fields": ["absent", "visitors"]}}]	7	350490234
252	2020-08-01 15:12:49.483965+03	337	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-09-02, время начала: 09:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
253	2020-08-01 15:14:38.255916+03	333	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-05, время начала: 09:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
254	2020-08-01 15:15:01.395562+03	333	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-05, время начала: 09:30:00	2	[]	7	350490234
255	2020-08-01 15:58:33.518551+03	342	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-09-11, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
256	2020-08-01 16:57:09.321836+03	1796	вторая, Group -- 400 руб./час	2	[{"changed": {"fields": ["max_players"]}}]	9	350490234
257	2020-08-01 16:57:29.912958+03	296	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 18:00:00	2	[{"changed": {"fields": ["absent", "visitors"]}}]	7	350490234
258	2020-08-01 19:28:32.851298+03	351	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 10:00:00	1	[{"added": {}}]	7	350490234
259	2020-08-01 19:29:57.865997+03	360	Группа: ОльгаШамаева, Freelancer -- 600 руб./час, дата тренировки 2020-08-06, время начала: 11:00:00	1	[{"added": {}}]	7	350490234
260	2020-08-01 20:39:00.259924+03	351	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 10:00:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
261	2020-08-02 21:31:51.444546+03	638303006	Владлен Юрков -- 89039600906	2	[{"changed": {"fields": ["status", "time_before_cancel", "bonus_lesson"]}}]	6	350490234
262	2020-08-02 21:39:14.005375+03	361	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-02, время начала: 10:30:00	1	[{"added": {}}]	7	350490234
263	2020-08-02 21:39:45.882392+03	361	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 10:30:00	2	[{"changed": {"fields": ["date"]}}]	7	350490234
264	2020-08-02 21:42:13.363569+03	1801	третья, Group -- 400 руб./час	2	[{"changed": {"fields": ["users"]}}]	9	350490234
265	2020-08-03 18:58:43.864084+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
266	2020-08-03 19:59:44.974866+03	350490234	Никита Шамаев -- 89661215215	2	[{"changed": {"fields": ["status"]}}]	6	350490234
267	2020-08-03 21:14:36.411571+03	324	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 16:30:00	2	[{"changed": {"fields": ["visitors"]}}]	7	350490234
268	2020-08-03 23:02:15.821356+03	324	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 16:30:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
269	2020-08-03 23:06:37.335136+03	324	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 16:30:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
270	2020-08-03 23:06:52.082592+03	324	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 16:30:00	2	[]	7	350490234
271	2020-08-03 23:07:27.749793+03	324	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 16:30:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
272	2020-08-04 11:49:37.725199+03	324	Группа: Первая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 16:30:00	2	[{"changed": {"fields": ["is_available"]}}]	7	350490234
273	2020-08-04 11:50:48.875929+03	362	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-09, время начала: 13:00:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
274	2020-08-04 11:51:11.963504+03	361	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-06, время начала: 13:00:00	2	[{"changed": {"fields": ["start_time"]}}]	7	350490234
275	2020-08-10 00:10:33.791354+03	370	Группа: третья, Group -- 400 руб./час, дата тренировки 2020-08-09, время начала: 12:00:00	1	[{"added": {}}]	7	350490234
276	2020-08-10 00:11:07.746082+03	379	Группа: БабаЯга, Freelancer -- 600 руб./час, дата тренировки 2020-08-09, время начала: 18:00:00	1	[{"added": {}}]	7	350490234
277	2020-08-10 00:13:15.291502+03	380	Группа: ОльгаШамаева, Freelancer -- 600 руб./час, дата тренировки 2020-08-09, время начала: 10:30:00	1	[{"added": {}}]	7	350490234
278	2020-08-10 13:07:01.005203+03	381	Группа: вторая, Group -- 400 руб./час, дата тренировки 2020-08-12, время начала: 10:30:00	1	[{"added": {}}]	7	350490234
279	2020-08-11 11:34:13.715546+03	391	Группа: НикитаШамаев, None, дата тренировки 2020-08-16, время начала: 15:30:00	3		7	350490234
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	base	user
7	base	grouptrainingday
8	base	tarif
9	base	traininggroup
10	base	channel
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2020-07-14 15:29:50.89144+03
2	contenttypes	0002_remove_content_type_name	2020-07-14 15:29:50.923529+03
3	auth	0001_initial	2020-07-14 15:29:51.581241+03
4	auth	0002_alter_permission_name_max_length	2020-07-14 15:29:51.601928+03
5	auth	0003_alter_user_email_max_length	2020-07-14 15:29:51.619533+03
6	auth	0004_alter_user_username_opts	2020-07-14 15:29:51.631859+03
7	auth	0005_alter_user_last_login_null	2020-07-14 15:29:51.654455+03
8	auth	0006_require_contenttypes_0002	2020-07-14 15:29:51.668912+03
9	auth	0007_alter_validators_add_error_messages	2020-07-14 15:29:51.691188+03
10	auth	0008_alter_user_username_max_length	2020-07-14 15:29:51.707432+03
11	auth	0009_alter_user_last_name_max_length	2020-07-14 15:29:51.719296+03
12	base	0001_initial	2020-07-14 15:29:53.693485+03
13	admin	0001_initial	2020-07-14 15:29:54.039102+03
14	admin	0002_logentry_remove_auto_add	2020-07-14 15:29:54.067145+03
15	sessions	0001_initial	2020-07-14 15:29:54.362592+03
16	base	0002_auto_20200714_1331	2020-07-14 16:32:05.208665+03
17	base	0003_auto_20200714_2043	2020-07-14 23:43:33.178087+03
18	base	0004_auto_20200714_2051	2020-07-14 23:51:21.862221+03
19	base	0005_channel	2020-07-15 11:17:40.993903+03
20	base	0006_auto_20200715_2151	2020-07-16 01:03:50.470152+03
21	base	0007_auto_20200716_1025	2020-07-16 13:25:08.191448+03
22	base	0008_auto_20200801_1113	2020-08-01 14:15:24.59089+03
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: nikita
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
s3aitm0xnwwikvr16cuktaijqjhk2edy	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-07-29 15:19:08.352119+03
8ktuy9yxalki32v82vcu9dmwohpbbxtk	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-07-30 14:41:43.897008+03
s6q2v30gi6kj93qt5wzzvqb83bqdpq5v	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-08-13 16:03:28.415883+03
dc4v7utbki9qcs1sn53px0q3xya0b3n3	MzdiOGFjMGU5OTAwY2UxMWFkZDA5YzRhM2ZmZTZmMGU4ZWZjMzEwNjp7Il9hdXRoX3VzZXJfaWQiOiIzNTA0OTAyMzQiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6ImE2MTgyNGMyNzE4Mzg1ZDI2YzlmNWI3YzQxNjk4YjdhYzQ3ZGQ2YTcifQ==	2020-08-25 10:51:52.024718+03
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 30, true);


--
-- Name: base_channel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.base_channel_id_seq', 2, true);


--
-- Name: base_grouptrainingday_absent_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.base_grouptrainingday_absent_id_seq', 19, true);


--
-- Name: base_grouptrainingday_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.base_grouptrainingday_id_seq', 393, true);


--
-- Name: base_grouptrainingday_visitors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.base_grouptrainingday_visitors_id_seq', 18, true);


--
-- Name: base_tarif_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.base_tarif_id_seq', 3, true);


--
-- Name: base_traininggroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.base_traininggroup_id_seq', 1803, true);


--
-- Name: base_traininggroup_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.base_traininggroup_user_id_seq', 27, true);


--
-- Name: base_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.base_user_groups_id_seq', 1, false);


--
-- Name: base_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.base_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 279, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 10, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: nikita
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 22, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: base_channel base_channel_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_channel
    ADD CONSTRAINT base_channel_pkey PRIMARY KEY (id);


--
-- Name: base_grouptrainingday_absent base_grouptrainingday_ab_grouptrainingday_id_user_fbe355a0_uniq; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_absent
    ADD CONSTRAINT base_grouptrainingday_ab_grouptrainingday_id_user_fbe355a0_uniq UNIQUE (grouptrainingday_id, user_id);


--
-- Name: base_grouptrainingday_absent base_grouptrainingday_absent_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_absent
    ADD CONSTRAINT base_grouptrainingday_absent_pkey PRIMARY KEY (id);


--
-- Name: base_grouptrainingday base_grouptrainingday_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday
    ADD CONSTRAINT base_grouptrainingday_pkey PRIMARY KEY (id);


--
-- Name: base_grouptrainingday_visitors base_grouptrainingday_vi_grouptrainingday_id_user_caa8bbcc_uniq; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_visitors
    ADD CONSTRAINT base_grouptrainingday_vi_grouptrainingday_id_user_caa8bbcc_uniq UNIQUE (grouptrainingday_id, user_id);


--
-- Name: base_grouptrainingday_visitors base_grouptrainingday_visitors_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_visitors
    ADD CONSTRAINT base_grouptrainingday_visitors_pkey PRIMARY KEY (id);


--
-- Name: base_tarif base_tarif_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_tarif
    ADD CONSTRAINT base_tarif_pkey PRIMARY KEY (id);


--
-- Name: base_traininggroup base_traininggroup_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_traininggroup
    ADD CONSTRAINT base_traininggroup_pkey PRIMARY KEY (id);


--
-- Name: base_traininggroup_users base_traininggroup_user_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_traininggroup_users
    ADD CONSTRAINT base_traininggroup_user_pkey PRIMARY KEY (id);


--
-- Name: base_traininggroup_users base_traininggroup_user_traininggroup_id_user_id_f4b922a9_uniq; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_traininggroup_users
    ADD CONSTRAINT base_traininggroup_user_traininggroup_id_user_id_f4b922a9_uniq UNIQUE (traininggroup_id, user_id);


--
-- Name: base_user_groups base_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_user_groups
    ADD CONSTRAINT base_user_groups_pkey PRIMARY KEY (id);


--
-- Name: base_user_groups base_user_groups_user_id_group_id_774631b7_uniq; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_user_groups
    ADD CONSTRAINT base_user_groups_user_id_group_id_774631b7_uniq UNIQUE (user_id, group_id);


--
-- Name: base_user base_user_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_user
    ADD CONSTRAINT base_user_pkey PRIMARY KEY (id);


--
-- Name: base_user_user_permissions base_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_user_user_permissions
    ADD CONSTRAINT base_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: base_user_user_permissions base_user_user_permissions_user_id_permission_id_e9093277_uniq; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_user_user_permissions
    ADD CONSTRAINT base_user_user_permissions_user_id_permission_id_e9093277_uniq UNIQUE (user_id, permission_id);


--
-- Name: base_user base_user_username_key; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_user
    ADD CONSTRAINT base_user_username_key UNIQUE (username);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: base_grouptrainingday_absent_grouptrainingday_id_91ce15a9; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_grouptrainingday_absent_grouptrainingday_id_91ce15a9 ON public.base_grouptrainingday_absent USING btree (grouptrainingday_id);


--
-- Name: base_grouptrainingday_absent_user_id_44e6519d; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_grouptrainingday_absent_user_id_44e6519d ON public.base_grouptrainingday_absent USING btree (user_id);


--
-- Name: base_grouptrainingday_group_id_80910337; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_grouptrainingday_group_id_80910337 ON public.base_grouptrainingday USING btree (group_id);


--
-- Name: base_grouptrainingday_visitors_grouptrainingday_id_9d5112bd; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_grouptrainingday_visitors_grouptrainingday_id_9d5112bd ON public.base_grouptrainingday_visitors USING btree (grouptrainingday_id);


--
-- Name: base_grouptrainingday_visitors_user_id_9af98114; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_grouptrainingday_visitors_user_id_9af98114 ON public.base_grouptrainingday_visitors USING btree (user_id);


--
-- Name: base_traininggroup_tarif_id_0c8885bb; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_traininggroup_tarif_id_0c8885bb ON public.base_traininggroup USING btree (tarif_id);


--
-- Name: base_traininggroup_user_traininggroup_id_e28016e2; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_traininggroup_user_traininggroup_id_e28016e2 ON public.base_traininggroup_users USING btree (traininggroup_id);


--
-- Name: base_traininggroup_user_user_id_6eea575e; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_traininggroup_user_user_id_6eea575e ON public.base_traininggroup_users USING btree (user_id);


--
-- Name: base_user_groups_group_id_c0eca7d6; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_user_groups_group_id_c0eca7d6 ON public.base_user_groups USING btree (group_id);


--
-- Name: base_user_groups_user_id_29a796b6; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_user_groups_user_id_29a796b6 ON public.base_user_groups USING btree (user_id);


--
-- Name: base_user_user_permissions_permission_id_0418bc02; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_user_user_permissions_permission_id_0418bc02 ON public.base_user_user_permissions USING btree (permission_id);


--
-- Name: base_user_user_permissions_user_id_2eec4d63; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_user_user_permissions_user_id_2eec4d63 ON public.base_user_user_permissions USING btree (user_id);


--
-- Name: base_user_username_59bfc15c_like; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX base_user_username_59bfc15c_like ON public.base_user USING btree (username varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: nikita
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_grouptrainingday base_grouptrainingda_group_id_80910337_fk_base_trai; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday
    ADD CONSTRAINT base_grouptrainingda_group_id_80910337_fk_base_trai FOREIGN KEY (group_id) REFERENCES public.base_traininggroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_grouptrainingday_absent base_grouptrainingda_grouptrainingday_id_91ce15a9_fk_base_grou; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_absent
    ADD CONSTRAINT base_grouptrainingda_grouptrainingday_id_91ce15a9_fk_base_grou FOREIGN KEY (grouptrainingday_id) REFERENCES public.base_grouptrainingday(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_grouptrainingday_visitors base_grouptrainingda_grouptrainingday_id_9d5112bd_fk_base_grou; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_visitors
    ADD CONSTRAINT base_grouptrainingda_grouptrainingday_id_9d5112bd_fk_base_grou FOREIGN KEY (grouptrainingday_id) REFERENCES public.base_grouptrainingday(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_grouptrainingday_absent base_grouptrainingday_absent_user_id_44e6519d_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_absent
    ADD CONSTRAINT base_grouptrainingday_absent_user_id_44e6519d_fk_base_user_id FOREIGN KEY (user_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_grouptrainingday_visitors base_grouptrainingday_visitors_user_id_9af98114_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_grouptrainingday_visitors
    ADD CONSTRAINT base_grouptrainingday_visitors_user_id_9af98114_fk_base_user_id FOREIGN KEY (user_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_traininggroup base_traininggroup_tarif_id_0c8885bb_fk_base_tarif_id; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_traininggroup
    ADD CONSTRAINT base_traininggroup_tarif_id_0c8885bb_fk_base_tarif_id FOREIGN KEY (tarif_id) REFERENCES public.base_tarif(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_traininggroup_users base_traininggroup_u_traininggroup_id_76a0d7bf_fk_base_trai; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_traininggroup_users
    ADD CONSTRAINT base_traininggroup_u_traininggroup_id_76a0d7bf_fk_base_trai FOREIGN KEY (traininggroup_id) REFERENCES public.base_traininggroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_traininggroup_users base_traininggroup_users_user_id_a4dc9ccf_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_traininggroup_users
    ADD CONSTRAINT base_traininggroup_users_user_id_a4dc9ccf_fk_base_user_id FOREIGN KEY (user_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_user_groups base_user_groups_group_id_c0eca7d6_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_user_groups
    ADD CONSTRAINT base_user_groups_group_id_c0eca7d6_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_user_groups base_user_groups_user_id_29a796b6_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_user_groups
    ADD CONSTRAINT base_user_groups_user_id_29a796b6_fk_base_user_id FOREIGN KEY (user_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_user_user_permissions base_user_user_permi_permission_id_0418bc02_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_user_user_permissions
    ADD CONSTRAINT base_user_user_permi_permission_id_0418bc02_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: base_user_user_permissions base_user_user_permissions_user_id_2eec4d63_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.base_user_user_permissions
    ADD CONSTRAINT base_user_user_permissions_user_id_2eec4d63_fk_base_user_id FOREIGN KEY (user_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_base_user_id; Type: FK CONSTRAINT; Schema: public; Owner: nikita
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_base_user_id FOREIGN KEY (user_id) REFERENCES public.base_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

