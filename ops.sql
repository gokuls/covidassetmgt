--
-- PostgreSQL database dump
--

-- Dumped from database version 11.12 (Debian 11.12-0+deb10u1)
-- Dumped by pg_dump version 11.12 (Debian 11.12-0+deb10u1)

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

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: assetmgt_asset; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.assetmgt_asset (
    asset_id bigint NOT NULL,
    asset_name character varying(250) NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    author_id integer NOT NULL
);


ALTER TABLE public.assetmgt_asset OWNER TO covidast;

--
-- Name: assetmgt_asset_asset_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.assetmgt_asset_asset_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assetmgt_asset_asset_id_seq OWNER TO covidast;

--
-- Name: assetmgt_asset_asset_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.assetmgt_asset_asset_id_seq OWNED BY public.assetmgt_asset.asset_id;


--
-- Name: assetmgt_assetfiles; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.assetmgt_assetfiles (
    id integer NOT NULL,
    file_name character varying(250) NOT NULL,
    datafile character varying(100) NOT NULL,
    uploaded_at timestamp with time zone NOT NULL
);


ALTER TABLE public.assetmgt_assetfiles OWNER TO covidast;

--
-- Name: assetmgt_assetfiles_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.assetmgt_assetfiles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assetmgt_assetfiles_id_seq OWNER TO covidast;

--
-- Name: assetmgt_assetfiles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.assetmgt_assetfiles_id_seq OWNED BY public.assetmgt_assetfiles.id;


--
-- Name: assetmgt_assetmgt; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.assetmgt_assetmgt (
    id integer NOT NULL,
    asset_total integer NOT NULL,
    asset_utilized integer,
    asset_balance integer,
    creation_date timestamp with time zone NOT NULL,
    asset_id_id bigint NOT NULL,
    author_id integer,
    hospital_id_id bigint NOT NULL,
    CONSTRAINT assetmgt_assetmgt_asset_balance_check CHECK ((asset_balance >= 0)),
    CONSTRAINT assetmgt_assetmgt_asset_total_check CHECK ((asset_total >= 0)),
    CONSTRAINT assetmgt_assetmgt_asset_utilized_check CHECK ((asset_utilized >= 0))
);


ALTER TABLE public.assetmgt_assetmgt OWNER TO covidast;

--
-- Name: assetmgt_assetmgt_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.assetmgt_assetmgt_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assetmgt_assetmgt_id_seq OWNER TO covidast;

--
-- Name: assetmgt_assetmgt_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.assetmgt_assetmgt_id_seq OWNED BY public.assetmgt_assetmgt.id;


--
-- Name: assetmgt_district; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.assetmgt_district (
    district_id bigint NOT NULL,
    district_name character varying(250) NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    state_id_id bigint NOT NULL
);


ALTER TABLE public.assetmgt_district OWNER TO covidast;

--
-- Name: assetmgt_district_district_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.assetmgt_district_district_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assetmgt_district_district_id_seq OWNER TO covidast;

--
-- Name: assetmgt_district_district_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.assetmgt_district_district_id_seq OWNED BY public.assetmgt_district.district_id;


--
-- Name: assetmgt_hospassetmapping; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.assetmgt_hospassetmapping (
    id integer NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    assetsmapped_id bigint NOT NULL,
    hospital_id bigint NOT NULL
);


ALTER TABLE public.assetmgt_hospassetmapping OWNER TO covidast;

--
-- Name: assetmgt_hospassetmapping_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.assetmgt_hospassetmapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assetmgt_hospassetmapping_id_seq OWNER TO covidast;

--
-- Name: assetmgt_hospassetmapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.assetmgt_hospassetmapping_id_seq OWNED BY public.assetmgt_hospassetmapping.id;


--
-- Name: assetmgt_hospital; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.assetmgt_hospital (
    hospital_id bigint NOT NULL,
    hospital_name character varying(250),
    hospital_type character varying(250),
    address character varying(250),
    contact_number character varying(250),
    city character varying(250),
    taluk character varying(250),
    pincode character varying(250),
    doctors integer,
    healthworkers integer,
    latitude character varying(250),
    longitude character varying(250),
    creation_date timestamp with time zone NOT NULL,
    district_id_id bigint NOT NULL,
    htype_id bigint,
    state_id_id bigint NOT NULL
);


ALTER TABLE public.assetmgt_hospital OWNER TO covidast;

--
-- Name: assetmgt_hospital_hospital_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.assetmgt_hospital_hospital_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assetmgt_hospital_hospital_id_seq OWNER TO covidast;

--
-- Name: assetmgt_hospital_hospital_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.assetmgt_hospital_hospital_id_seq OWNED BY public.assetmgt_hospital.hospital_id;


--
-- Name: assetmgt_hospitaltype; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.assetmgt_hospitaltype (
    htype_id bigint NOT NULL,
    hospital_type character varying(250) NOT NULL,
    creation_date timestamp with time zone NOT NULL
);


ALTER TABLE public.assetmgt_hospitaltype OWNER TO covidast;

--
-- Name: assetmgt_hospitaltype_htype_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.assetmgt_hospitaltype_htype_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assetmgt_hospitaltype_htype_id_seq OWNER TO covidast;

--
-- Name: assetmgt_hospitaltype_htype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.assetmgt_hospitaltype_htype_id_seq OWNED BY public.assetmgt_hospitaltype.htype_id;


--
-- Name: assetmgt_htypeassetmapping; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.assetmgt_htypeassetmapping (
    id integer NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    assetsmapped_id bigint NOT NULL,
    district_id bigint NOT NULL,
    htype_id bigint NOT NULL,
    state_id bigint NOT NULL
);


ALTER TABLE public.assetmgt_htypeassetmapping OWNER TO covidast;

--
-- Name: assetmgt_htypeassetmapping_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.assetmgt_htypeassetmapping_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assetmgt_htypeassetmapping_id_seq OWNER TO covidast;

--
-- Name: assetmgt_htypeassetmapping_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.assetmgt_htypeassetmapping_id_seq OWNED BY public.assetmgt_htypeassetmapping.id;


--
-- Name: assetmgt_patientstat; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.assetmgt_patientstat (
    id integer NOT NULL,
    patient_count integer NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    author_id integer,
    hospital_id_id bigint NOT NULL
);


ALTER TABLE public.assetmgt_patientstat OWNER TO covidast;

--
-- Name: assetmgt_patientstat_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.assetmgt_patientstat_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assetmgt_patientstat_id_seq OWNER TO covidast;

--
-- Name: assetmgt_patientstat_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.assetmgt_patientstat_id_seq OWNED BY public.assetmgt_patientstat.id;


--
-- Name: assetmgt_state; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.assetmgt_state (
    state_id bigint NOT NULL,
    state_name character varying(250) NOT NULL,
    creation_date timestamp with time zone NOT NULL
);


ALTER TABLE public.assetmgt_state OWNER TO covidast;

--
-- Name: assetmgt_state_state_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.assetmgt_state_state_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assetmgt_state_state_id_seq OWNER TO covidast;

--
-- Name: assetmgt_state_state_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.assetmgt_state_state_id_seq OWNED BY public.assetmgt_state.state_id;


--
-- Name: assetmgt_userprofile; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.assetmgt_userprofile (
    id integer NOT NULL,
    adminstate integer NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    district_id_id bigint NOT NULL,
    hospital_id_id bigint,
    state_id_id bigint NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.assetmgt_userprofile OWNER TO covidast;

--
-- Name: assetmgt_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.assetmgt_userprofile_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.assetmgt_userprofile_id_seq OWNER TO covidast;

--
-- Name: assetmgt_userprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.assetmgt_userprofile_id_seq OWNED BY public.assetmgt_userprofile.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO covidast;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO covidast;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.auth_group_id_seq OWNED BY public.auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO covidast;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO covidast;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.auth_group_permissions_id_seq OWNED BY public.auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO covidast;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO covidast;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.auth_permission_id_seq OWNED BY public.auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO covidast;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO covidast;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO covidast;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.auth_user_groups_id_seq OWNED BY public.auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO covidast;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.auth_user_id_seq OWNED BY public.auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO covidast;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO covidast;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.auth_user_user_permissions_id_seq OWNED BY public.auth_user_user_permissions.id;


--
-- Name: captcha_captchastore; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.captcha_captchastore (
    id integer NOT NULL,
    challenge character varying(32) NOT NULL,
    response character varying(32) NOT NULL,
    hashkey character varying(40) NOT NULL,
    expiration timestamp with time zone NOT NULL
);


ALTER TABLE public.captcha_captchastore OWNER TO covidast;

--
-- Name: captcha_captchastore_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.captcha_captchastore_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.captcha_captchastore_id_seq OWNER TO covidast;

--
-- Name: captcha_captchastore_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.captcha_captchastore_id_seq OWNED BY public.captcha_captchastore.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO covidast;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO covidast;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.django_admin_log_id_seq OWNED BY public.django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO covidast;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO covidast;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.django_content_type_id_seq OWNED BY public.django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.django_migrations OWNER TO covidast;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: covidast
--

CREATE SEQUENCE public.django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_migrations_id_seq OWNER TO covidast;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: covidast
--

ALTER SEQUENCE public.django_migrations_id_seq OWNED BY public.django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: covidast
--

CREATE TABLE public.django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO covidast;

--
-- Name: assetmgt_asset asset_id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_asset ALTER COLUMN asset_id SET DEFAULT nextval('public.assetmgt_asset_asset_id_seq'::regclass);


--
-- Name: assetmgt_assetfiles id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_assetfiles ALTER COLUMN id SET DEFAULT nextval('public.assetmgt_assetfiles_id_seq'::regclass);


--
-- Name: assetmgt_assetmgt id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_assetmgt ALTER COLUMN id SET DEFAULT nextval('public.assetmgt_assetmgt_id_seq'::regclass);


--
-- Name: assetmgt_district district_id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_district ALTER COLUMN district_id SET DEFAULT nextval('public.assetmgt_district_district_id_seq'::regclass);


--
-- Name: assetmgt_hospassetmapping id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_hospassetmapping ALTER COLUMN id SET DEFAULT nextval('public.assetmgt_hospassetmapping_id_seq'::regclass);


--
-- Name: assetmgt_hospital hospital_id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_hospital ALTER COLUMN hospital_id SET DEFAULT nextval('public.assetmgt_hospital_hospital_id_seq'::regclass);


--
-- Name: assetmgt_hospitaltype htype_id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_hospitaltype ALTER COLUMN htype_id SET DEFAULT nextval('public.assetmgt_hospitaltype_htype_id_seq'::regclass);


--
-- Name: assetmgt_htypeassetmapping id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_htypeassetmapping ALTER COLUMN id SET DEFAULT nextval('public.assetmgt_htypeassetmapping_id_seq'::regclass);


--
-- Name: assetmgt_patientstat id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_patientstat ALTER COLUMN id SET DEFAULT nextval('public.assetmgt_patientstat_id_seq'::regclass);


--
-- Name: assetmgt_state state_id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_state ALTER COLUMN state_id SET DEFAULT nextval('public.assetmgt_state_state_id_seq'::regclass);


--
-- Name: assetmgt_userprofile id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_userprofile ALTER COLUMN id SET DEFAULT nextval('public.assetmgt_userprofile_id_seq'::regclass);


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_group ALTER COLUMN id SET DEFAULT nextval('public.auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_permission ALTER COLUMN id SET DEFAULT nextval('public.auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_user ALTER COLUMN id SET DEFAULT nextval('public.auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_user_groups ALTER COLUMN id SET DEFAULT nextval('public.auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('public.auth_user_user_permissions_id_seq'::regclass);


--
-- Name: captcha_captchastore id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.captcha_captchastore ALTER COLUMN id SET DEFAULT nextval('public.captcha_captchastore_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.django_admin_log ALTER COLUMN id SET DEFAULT nextval('public.django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.django_content_type ALTER COLUMN id SET DEFAULT nextval('public.django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.django_migrations ALTER COLUMN id SET DEFAULT nextval('public.django_migrations_id_seq'::regclass);


--
-- Data for Name: assetmgt_asset; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.assetmgt_asset (asset_id, asset_name, creation_date, author_id) FROM stdin;
2	Oxygen	2021-12-28 09:38:00.890285+05:30	1
3	ECG Monitor	2021-12-28 09:38:12.817315+05:30	1
4	X - RAY	2021-12-28 09:38:56.645422+05:30	1
5	Refrigerator	2021-12-28 09:39:17.606233+05:30	1
6	Pulse oximeter	2021-12-28 09:39:26.901083+05:30	1
7	Patient monitor	2021-12-28 09:39:55.996709+05:30	1
8	Ambulance	2021-12-28 09:42:30.81674+05:30	1
10	Ventilator	2021-12-28 09:51:53.997574+05:30	1
1	Bed	2021-12-28 09:33:03.611274+05:30	1
\.


--
-- Data for Name: assetmgt_assetfiles; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.assetmgt_assetfiles (id, file_name, datafile, uploaded_at) FROM stdin;
\.


--
-- Data for Name: assetmgt_assetmgt; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.assetmgt_assetmgt (id, asset_total, asset_utilized, asset_balance, creation_date, asset_id_id, author_id, hospital_id_id) FROM stdin;
1	100	25	75	2021-12-28 10:54:30.806756+05:30	1	1	1
2	150	50	100	2021-12-28 10:54:30.848433+05:30	2	1	1
3	10	3	7	2021-12-28 10:54:30.861555+05:30	3	1	1
4	5	5	0	2021-12-28 10:54:30.873481+05:30	4	1	1
5	10	6	4	2021-12-28 10:54:30.885514+05:30	5	1	1
6	150	100	50	2021-12-28 10:54:30.8988+05:30	6	1	1
7	100	75	25	2021-12-28 10:54:30.910822+05:30	7	1	1
8	10	5	5	2021-12-28 10:54:30.924139+05:30	8	1	1
9	50	35	15	2021-12-28 10:54:30.936158+05:30	10	1	1
10	75	25	50	2021-12-28 10:55:39.346997+05:30	1	1	2
11	120	25	95	2021-12-28 10:55:39.367063+05:30	2	1	2
12	50	30	20	2021-12-28 10:55:39.378799+05:30	3	1	2
13	25	15	10	2021-12-28 10:55:39.392125+05:30	4	1	2
14	5	2	3	2021-12-28 10:55:39.404125+05:30	5	1	2
15	100	25	75	2021-12-28 10:55:39.417395+05:30	6	1	2
16	150	50	100	2021-12-28 10:55:39.429381+05:30	7	1	2
17	5	2	3	2021-12-28 10:55:39.442703+05:30	8	1	2
18	100	35	65	2021-12-28 10:55:39.45475+05:30	10	1	2
19	150	50	100	2021-12-28 10:56:12.531682+05:30	1	1	3
20	100	25	75	2021-12-28 10:56:12.555385+05:30	3	1	3
21	150	65	85	2021-12-28 10:56:12.567082+05:30	6	1	3
22	100	32	68	2021-12-28 10:56:12.580349+05:30	10	1	3
23	100	26	74	2021-12-28 10:56:50.99173+05:30	1	1	4
24	50	23	27	2021-12-28 10:56:51.021243+05:30	3	1	4
25	15	12	3	2021-12-28 10:56:51.034362+05:30	4	1	4
26	100	25	75	2021-12-28 10:56:51.046305+05:30	6	1	4
27	200	120	80	2021-12-28 10:56:51.059574+05:30	10	1	4
28	150	50	100	2021-12-28 10:57:11.307453+05:30	1	1	6
29	100	26	74	2021-12-28 10:57:11.344223+05:30	6	1	6
30	10	5	5	2021-12-28 10:57:11.378275+05:30	8	1	6
31	150	100	50	2021-12-28 11:09:32.195372+05:30	3	1	8
32	100	20	80	2021-12-28 11:09:32.221626+05:30	6	1	8
33	150	60	90	2021-12-28 11:09:32.233205+05:30	10	1	8
34	120	25	95	2021-12-28 11:09:55.527215+05:30	3	1	7
35	150	25	125	2021-12-28 11:09:55.561938+05:30	10	1	7
36	100	50	50	2021-12-28 11:10:40.045615+05:30	1	1	9
37	150	50	100	2021-12-28 11:10:40.060537+05:30	2	1	9
38	10	2	8	2021-12-28 11:10:40.073461+05:30	4	1	9
39	5	1	4	2021-12-28 11:10:40.085442+05:30	8	1	9
40	150	100	50	2021-12-28 11:10:40.098752+05:30	10	1	9
145	100	50	50	2021-12-28 12:11:36.188595+05:30	3	1	3
146	150	65	85	2021-12-28 12:11:36.218916+05:30	6	1	3
147	100	32	68	2021-12-28 12:11:36.23165+05:30	10	1	3
148	150	50	100	2021-12-28 12:11:36.243326+05:30	1	1	3
\.


--
-- Data for Name: assetmgt_district; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.assetmgt_district (district_id, district_name, creation_date, state_id_id) FROM stdin;
1	Chennai	2021-12-27 19:54:28.792762+05:30	1
2	Ariyalur	2021-12-28 09:43:52.460586+05:30	1
3	Erode	2021-12-28 09:44:02.684231+05:30	1
4	The Nilgiris	2021-12-28 09:44:11.4626+05:30	1
5	Cuddalore	2021-12-28 09:44:19.161948+05:30	1
6	Karur	2021-12-28 09:44:27.283567+05:30	1
7	Kallakurichi	2021-12-28 09:44:35.618742+05:30	1
8	Kancheepuram	2021-12-28 09:44:44.665593+05:30	1
9	Krishnagiri	2021-12-28 09:44:52.051711+05:30	1
10	Coimbatore	2021-12-28 09:45:00.802034+05:30	1
11	Sivagangai	2021-12-28 09:46:32.810232+05:30	1
12	Salem	2021-12-28 09:46:47.76828+05:30	1
13	Chengalpet	2021-12-28 09:46:57.579446+05:30	1
14	Thanjavur	2021-12-28 09:47:05.923451+05:30	1
15	Dharmapuri	2021-12-28 09:47:14.181557+05:30	1
16	Dindigul	2021-12-28 09:47:22.15382+05:30	1
17	Trichirappalli	2021-12-28 09:47:31.233546+05:30	1
18	Thirunelveli	2021-12-28 09:47:41.205633+05:30	1
19	Tirupathur	2021-12-28 09:47:50.74937+05:30	1
20	Tiruppur	2021-12-28 09:47:59.964202+05:30	1
21	Tiruvannamalai	2021-12-28 09:48:08.370153+05:30	1
22	Thiruvallur	2021-12-28 09:48:19.164356+05:30	1
23	Thiruvarur	2021-12-28 09:48:32.294485+05:30	1
24	Tuticorin	2021-12-28 09:48:40.657611+05:30	1
25	Tenkasi	2021-12-28 09:48:49.120293+05:30	1
26	Theni	2021-12-28 09:48:58.310056+05:30	1
27	Nagapattinam	2021-12-28 09:49:06.42936+05:30	1
28	Kanyakumari	2021-12-28 09:49:15.470218+05:30	1
29	Namakkal	2021-12-28 09:49:23.790981+05:30	1
30	Pudukottai	2021-12-28 09:49:35.042983+05:30	1
31	Perambalur	2021-12-28 09:49:46.871796+05:30	1
32	Madurai	2021-12-28 09:49:54.819411+05:30	1
33	Mayiladuthurai	2021-12-28 09:50:02.813025+05:30	1
34	Ranipet	2021-12-28 09:50:11.816742+05:30	1
35	Ramanathapuram	2021-12-28 09:50:23.348591+05:30	1
36	Virudhunagar	2021-12-28 09:50:31.305328+05:30	1
37	Viluppuram	2021-12-28 09:50:38.915902+05:30	1
38	Vellore	2021-12-28 09:50:48.472009+05:30	1
\.


--
-- Data for Name: assetmgt_hospassetmapping; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.assetmgt_hospassetmapping (id, creation_date, assetsmapped_id, hospital_id) FROM stdin;
1	2021-12-28 10:22:16.003703+05:30	1	1
2	2021-12-28 10:22:28.82305+05:30	2	1
3	2021-12-28 10:22:40.476083+05:30	3	1
4	2021-12-28 10:23:00.438959+05:30	4	1
5	2021-12-28 10:23:08.115172+05:30	5	1
6	2021-12-28 10:23:15.366075+05:30	6	1
7	2021-12-28 10:23:23.436809+05:30	7	1
8	2021-12-28 10:23:31.331214+05:30	8	1
9	2021-12-28 10:23:38.612574+05:30	8	1
10	2021-12-28 10:23:45.688692+05:30	10	1
11	2021-12-28 10:34:09.608316+05:30	1	2
12	2021-12-28 10:34:15.563271+05:30	2	2
13	2021-12-28 10:34:35.353134+05:30	3	2
14	2021-12-28 10:34:39.990376+05:30	4	2
15	2021-12-28 10:34:44.573852+05:30	5	2
16	2021-12-28 10:34:49.232405+05:30	6	2
17	2021-12-28 10:34:54.018253+05:30	7	2
18	2021-12-28 10:34:58.462287+05:30	8	2
19	2021-12-28 10:35:02.606787+05:30	10	2
20	2021-12-28 10:35:07.38376+05:30	1	3
21	2021-12-28 10:35:12.872137+05:30	3	3
22	2021-12-28 10:35:18.158951+05:30	6	3
23	2021-12-28 10:35:23.212247+05:30	10	3
24	2021-12-28 10:35:38.422287+05:30	1	4
25	2021-12-28 10:35:45.304657+05:30	3	4
26	2021-12-28 10:35:50.279289+05:30	4	4
27	2021-12-28 10:35:54.670622+05:30	6	4
28	2021-12-28 10:36:00.140386+05:30	10	4
29	2021-12-28 10:36:05.629197+05:30	1	5
30	2021-12-28 10:36:10.918525+05:30	2	5
31	2021-12-28 10:36:16.735062+05:30	3	5
32	2021-12-28 10:36:21.390945+05:30	5	5
33	2021-12-28 10:36:25.965253+05:30	6	5
34	2021-12-28 10:36:30.333306+05:30	8	5
35	2021-12-28 10:36:34.390281+05:30	10	5
36	2021-12-28 10:36:39.060093+05:30	8	5
37	2021-12-28 10:36:44.330661+05:30	1	6
38	2021-12-28 10:36:49.136128+05:30	8	6
39	2021-12-28 10:36:54.073384+05:30	6	6
40	2021-12-28 11:06:29.134767+05:30	3	7
41	2021-12-28 11:06:49.028949+05:30	10	7
42	2021-12-28 11:07:02.673805+05:30	3	7
43	2021-12-28 11:07:27.715286+05:30	3	8
44	2021-12-28 11:07:32.559747+05:30	10	8
45	2021-12-28 11:07:47.464274+05:30	6	8
46	2021-12-28 11:07:54.353711+05:30	2	9
47	2021-12-28 11:08:00.591362+05:30	1	9
48	2021-12-28 11:08:06.825364+05:30	4	9
49	2021-12-28 11:08:12.415568+05:30	8	9
50	2021-12-28 11:08:17.450619+05:30	10	9
51	2021-12-28 11:08:23.401295+05:30	1	10
52	2021-12-28 11:08:28.436149+05:30	2	10
53	2021-12-28 11:08:34.889214+05:30	3	10
54	2021-12-28 11:08:40.897199+05:30	5	10
55	2021-12-28 11:08:46.032658+05:30	6	10
56	2021-12-28 11:08:50.461313+05:30	10	10
\.


--
-- Data for Name: assetmgt_hospital; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.assetmgt_hospital (hospital_id, hospital_name, hospital_type, address, contact_number, city, taluk, pincode, doctors, healthworkers, latitude, longitude, creation_date, district_id_id, htype_id, state_id_id) FROM stdin;
1	Rajiv Gandhi Government General Hospital	Government	GH Post Office, Poonamallee High Road, 3, Grand Southern Trunk Rd, near Park Town. Central, Park Town, Chennai	044 2530 5000	Chennai	Chennai	600003	150	300	13.0809°	80.2773°	2021-12-28 09:53:45.425783+05:30	1	1	1
2	Tamil Nadu Government Multi-Super-Speciality Hospital	Government	Government Estate, Anna Salai, Chennai, Tamil Nadu	044 2530 5001	Chennai	Chennai	600002	100	200	13.0691°	80.2738°	2021-12-28 09:56:45.473701+05:30	1	1	1
3	DR.KAMAKSHI MEMORIAL HOSPITALS	Private	1, 200 Feet Radial Rd, Dandeeswarar Nagar, Rose Avenue, Pallikaranai, Chennai	044 6630 0300	Chennai	Chennai	600100	300	450	12.9492	80.2096	2021-12-28 09:59:39.133897+05:30	1	2	1
4	Government Hospital, Coimbatore (BIG)	Government	1561, Trichy Rd, Highways Colony, Gopalapuram, Coimbatore	0422 239 0261	Coimbatore	Coimbatore	641002	100	248	10.9963	76.9701	2021-12-28 10:02:34.572029+05:30	10	1	1
5	Konkunadu hospital	Private	Kongunadu Hospital, Tatabad, Coimbatore	0422 239 0262	Coimbatore	Coimbatore	641002	100	150	11.0177	76.9605	2021-12-28 10:04:40.342875+05:30	5	2	1
6	Sri Ramakrishna Hospital (Multi-Speciality)	Private	395, Sarojini Naidu Rd, Siddhapudur, Balasundaram Layout, B.K.R Nagar, Coimbatore, Tamil Nadu	0422 239 0263	Coimbatore	Coimbatore	641044	100	150	11.0231	76.9776	2021-12-28 10:33:32.290576+05:30	10	2	1
7	Ariyalur Government Hospital	Government	43V9+3V5, Rajajinagar, Ariyalur	04329 224 050	Ariyalur	Ariyalur	621704	150	250	11.3345	79.2318	2021-12-28 10:42:58.281875+05:30	2	1	1
8	ARIYALUR GOLDEN HOSPITAL PVT LTD	Private	Ariyalur - Sendurai Rd, Periyar Nagar, Ariyalur	094875 76493	Ariyalur	Ariyalur	621704	50	150	11.3345	79.2318	2021-12-28 10:45:20.642118+05:30	2	2	1
9	KMS HOSPITAL	Private	46, Trichy Main Rd, Meala Agraharam, MIN Nagar, Ariyalur	04329 222 199	Ariyalur	Ariyalur	621704	50	100	13.0783	80.2439	2021-12-28 10:47:18.463517+05:30	3	2	1
10	Thanthai Periyar Government Headquarters Hospital	Government	EVN Rd, Kaikolar Thottam, Erode	0424 225 3676	Erode	Erode	638009	75	100	11.3398	77.7173	2021-12-28 10:49:45.088925+05:30	3	1	1
\.


--
-- Data for Name: assetmgt_hospitaltype; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.assetmgt_hospitaltype (htype_id, hospital_type, creation_date) FROM stdin;
1	Government	2021-12-28 09:32:05.638148+05:30
2	Private	2021-12-28 09:32:37.383595+05:30
\.


--
-- Data for Name: assetmgt_htypeassetmapping; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.assetmgt_htypeassetmapping (id, creation_date, assetsmapped_id, district_id, htype_id, state_id) FROM stdin;
1	2021-12-28 10:37:36.640158+05:30	1	1	1	1
2	2021-12-28 10:37:46.517602+05:30	2	1	1	1
\.


--
-- Data for Name: assetmgt_patientstat; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.assetmgt_patientstat (id, patient_count, creation_date, author_id, hospital_id_id) FROM stdin;
\.


--
-- Data for Name: assetmgt_state; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.assetmgt_state (state_id, state_name, creation_date) FROM stdin;
1	TamilNadu	2021-12-27 19:54:14.371997+05:30
\.


--
-- Data for Name: assetmgt_userprofile; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.assetmgt_userprofile (id, adminstate, creation_date, district_id_id, hospital_id_id, state_id_id, user_id) FROM stdin;
1	2	2021-12-27 19:54:59.777079+05:30	1	\N	1	1
\.


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add asset	7	add_asset
26	Can change asset	7	change_asset
27	Can delete asset	7	delete_asset
28	Can view asset	7	view_asset
29	Can add asset files	8	add_assetfiles
30	Can change asset files	8	change_assetfiles
31	Can delete asset files	8	delete_assetfiles
32	Can view asset files	8	view_assetfiles
33	Can add district	9	add_district
34	Can change district	9	change_district
35	Can delete district	9	delete_district
36	Can view district	9	view_district
37	Can add hospital	10	add_hospital
38	Can change hospital	10	change_hospital
39	Can delete hospital	10	delete_hospital
40	Can view hospital	10	view_hospital
41	Can add hospital type	11	add_hospitaltype
42	Can change hospital type	11	change_hospitaltype
43	Can delete hospital type	11	delete_hospitaltype
44	Can view hospital type	11	view_hospitaltype
45	Can add state	12	add_state
46	Can change state	12	change_state
47	Can delete state	12	delete_state
48	Can view state	12	view_state
49	Can add user profile	13	add_userprofile
50	Can change user profile	13	change_userprofile
51	Can delete user profile	13	delete_userprofile
52	Can view user profile	13	view_userprofile
53	Can add patient stat	14	add_patientstat
54	Can change patient stat	14	change_patientstat
55	Can delete patient stat	14	delete_patientstat
56	Can view patient stat	14	view_patientstat
57	Can add htype asset mapping	15	add_htypeassetmapping
58	Can change htype asset mapping	15	change_htypeassetmapping
59	Can delete htype asset mapping	15	delete_htypeassetmapping
60	Can view htype asset mapping	15	view_htypeassetmapping
61	Can add hosp asset mapping	16	add_hospassetmapping
62	Can change hosp asset mapping	16	change_hospassetmapping
63	Can delete hosp asset mapping	16	delete_hospassetmapping
64	Can view hosp asset mapping	16	view_hospassetmapping
65	Can add asset mgt	17	add_assetmgt
66	Can change asset mgt	17	change_assetmgt
67	Can delete asset mgt	17	delete_assetmgt
68	Can view asset mgt	17	view_assetmgt
69	Can add captcha store	18	add_captchastore
70	Can change captcha store	18	change_captchastore
71	Can delete captcha store	18	delete_captchastore
72	Can view captcha store	18	view_captchastore
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$180000$fDLZGFpIEWgr$D3Q2aMDh+cswwtAI/T2JcpBqkjn/EVPVMVcgD7wiwk4=	2021-12-28 16:59:29.905548+05:30	t	admin				t	t	2021-12-27 12:06:44.590942+05:30
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: captcha_captchastore; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.captcha_captchastore (id, challenge, response, hashkey, expiration) FROM stdin;
36	KSLC	kslc	1360944e714d30778638e8889a8fb14b94a295a8	2021-12-28 17:04:03.322713+05:30
37	IQCH	iqch	a9d8c0507135a31d3fd75f1bc7611f9753396e9f	2021-12-28 17:04:09.816044+05:30
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2021-12-27 19:54:14.372894+05:30	1	Tamilnadu	1	[{"added": {}}]	12	1
2	2021-12-27 19:54:28.795485+05:30	1	Chennai	1	[{"added": {}}]	9	1
3	2021-12-27 19:54:59.780038+05:30	1	admin	1	[{"added": {}}]	13	1
4	2021-12-28 09:32:05.639053+05:30	1	Government	1	[{"added": {}}]	11	1
5	2021-12-28 09:32:37.384236+05:30	2	Private	1	[{"added": {}}]	11	1
6	2021-12-28 09:33:03.612224+05:30	1	Bad	1	[{"added": {}}]	7	1
7	2021-12-28 09:38:00.891014+05:30	2	Oxygen	1	[{"added": {}}]	7	1
8	2021-12-28 09:38:12.818049+05:30	3	ECG Monitor	1	[{"added": {}}]	7	1
9	2021-12-28 09:38:56.646099+05:30	4	X - RAY	1	[{"added": {}}]	7	1
10	2021-12-28 09:39:17.607061+05:30	5	Refrigerator	1	[{"added": {}}]	7	1
11	2021-12-28 09:39:26.901835+05:30	6	Pulse oximeter	1	[{"added": {}}]	7	1
12	2021-12-28 09:39:55.997452+05:30	7	Patient monitor	1	[{"added": {}}]	7	1
13	2021-12-28 09:42:30.817445+05:30	8	Ambulance	1	[{"added": {}}]	7	1
14	2021-12-28 09:42:46.247869+05:30	9	ventilator	1	[{"added": {}}]	7	1
15	2021-12-28 09:43:52.461324+05:30	2	Ariyalur	1	[{"added": {}}]	9	1
16	2021-12-28 09:44:02.68499+05:30	3	Erode	1	[{"added": {}}]	9	1
17	2021-12-28 09:44:11.463263+05:30	4	The Nilgiris	1	[{"added": {}}]	9	1
18	2021-12-28 09:44:19.162684+05:30	5	Cuddalore	1	[{"added": {}}]	9	1
19	2021-12-28 09:44:27.28432+05:30	6	Karur	1	[{"added": {}}]	9	1
20	2021-12-28 09:44:35.619574+05:30	7	Kallakurichi	1	[{"added": {}}]	9	1
21	2021-12-28 09:44:44.666336+05:30	8	Kancheepuram	1	[{"added": {}}]	9	1
22	2021-12-28 09:44:52.052462+05:30	9	Krishnagiri	1	[{"added": {}}]	9	1
23	2021-12-28 09:45:00.802698+05:30	10	Coimbatore	1	[{"added": {}}]	9	1
24	2021-12-28 09:46:32.810898+05:30	11	Sivagangai	1	[{"added": {}}]	9	1
25	2021-12-28 09:46:47.768991+05:30	12	Salem	1	[{"added": {}}]	9	1
26	2021-12-28 09:46:57.580178+05:30	13	Chengalpet	1	[{"added": {}}]	9	1
27	2021-12-28 09:47:05.92418+05:30	14	Thanjavur	1	[{"added": {}}]	9	1
28	2021-12-28 09:47:14.182348+05:30	15	Dharmapuri	1	[{"added": {}}]	9	1
29	2021-12-28 09:47:22.154496+05:30	16	Dindigul	1	[{"added": {}}]	9	1
30	2021-12-28 09:47:31.234212+05:30	17	Trichirappalli	1	[{"added": {}}]	9	1
31	2021-12-28 09:47:41.206371+05:30	18	Thirunelveli	1	[{"added": {}}]	9	1
32	2021-12-28 09:47:50.7501+05:30	19	Tirupathur	1	[{"added": {}}]	9	1
33	2021-12-28 09:47:59.964876+05:30	20	Tiruppur	1	[{"added": {}}]	9	1
34	2021-12-28 09:48:08.370879+05:30	21	Tiruvannamalai	1	[{"added": {}}]	9	1
35	2021-12-28 09:48:19.165104+05:30	22	Thiruvallur	1	[{"added": {}}]	9	1
36	2021-12-28 09:48:32.295234+05:30	23	Thiruvarur	1	[{"added": {}}]	9	1
37	2021-12-28 09:48:40.658349+05:30	24	Tuticorin	1	[{"added": {}}]	9	1
38	2021-12-28 09:48:49.121054+05:30	25	Tenkasi	1	[{"added": {}}]	9	1
39	2021-12-28 09:48:58.310808+05:30	26	Theni	1	[{"added": {}}]	9	1
40	2021-12-28 09:49:06.430094+05:30	27	Nagapattinam	1	[{"added": {}}]	9	1
41	2021-12-28 09:49:15.470963+05:30	28	Kanyakumari	1	[{"added": {}}]	9	1
42	2021-12-28 09:49:23.791785+05:30	29	Namakkal	1	[{"added": {}}]	9	1
43	2021-12-28 09:49:35.043706+05:30	30	Pudukottai	1	[{"added": {}}]	9	1
44	2021-12-28 09:49:46.872526+05:30	31	Perambalur	1	[{"added": {}}]	9	1
45	2021-12-28 09:49:54.820073+05:30	32	Madurai	1	[{"added": {}}]	9	1
46	2021-12-28 09:50:02.813761+05:30	33	Mayiladuthurai	1	[{"added": {}}]	9	1
47	2021-12-28 09:50:11.817477+05:30	34	Ranipet	1	[{"added": {}}]	9	1
48	2021-12-28 09:50:23.349294+05:30	35	Ramanathapuram	1	[{"added": {}}]	9	1
49	2021-12-28 09:50:31.306058+05:30	36	Virudhunagar	1	[{"added": {}}]	9	1
50	2021-12-28 09:50:38.916647+05:30	37	Viluppuram	1	[{"added": {}}]	9	1
51	2021-12-28 09:50:48.472862+05:30	38	Vellore	1	[{"added": {}}]	9	1
52	2021-12-28 09:51:37.458334+05:30	9	ventilator	3		7	1
53	2021-12-28 09:51:53.998411+05:30	10	Ventilator	1	[{"added": {}}]	7	1
54	2021-12-28 09:53:45.427367+05:30	1	Rajiv Gandhi Government General Hospital	1	[{"added": {}}]	10	1
55	2021-12-28 09:56:45.474962+05:30	2	Tamil Nadu Government Multi-Super-Speciality Hospital	1	[{"added": {}}]	10	1
56	2021-12-28 09:59:39.135141+05:30	3	DR.KAMAKSHI MEMORIAL HOSPITALS	1	[{"added": {}}]	10	1
57	2021-12-28 10:02:34.573296+05:30	4	Government Hospital, Coimbatore (BIG)	1	[{"added": {}}]	10	1
58	2021-12-28 10:04:40.344119+05:30	5	Konkunadu hospital	1	[{"added": {}}]	10	1
59	2021-12-28 10:22:16.004778+05:30	1	Rajiv Gandhi Government General Hospital-Bad	1	[{"added": {}}]	16	1
60	2021-12-28 10:22:28.823826+05:30	2	Rajiv Gandhi Government General Hospital-Oxygen	1	[{"added": {}}]	16	1
61	2021-12-28 10:22:40.476952+05:30	3	Rajiv Gandhi Government General Hospital-ECG Monitor	1	[{"added": {}}]	16	1
62	2021-12-28 10:23:00.439734+05:30	4	Rajiv Gandhi Government General Hospital-X - RAY	1	[{"added": {}}]	16	1
63	2021-12-28 10:23:08.115973+05:30	5	Rajiv Gandhi Government General Hospital-Refrigerator	1	[{"added": {}}]	16	1
64	2021-12-28 10:23:15.36693+05:30	6	Rajiv Gandhi Government General Hospital-Pulse oximeter	1	[{"added": {}}]	16	1
65	2021-12-28 10:23:23.437659+05:30	7	Rajiv Gandhi Government General Hospital-Patient monitor	1	[{"added": {}}]	16	1
66	2021-12-28 10:23:31.33207+05:30	8	Rajiv Gandhi Government General Hospital-Ambulance	1	[{"added": {}}]	16	1
67	2021-12-28 10:23:38.613424+05:30	9	Rajiv Gandhi Government General Hospital-Ambulance	1	[{"added": {}}]	16	1
68	2021-12-28 10:23:45.689575+05:30	10	Rajiv Gandhi Government General Hospital-Ventilator	1	[{"added": {}}]	16	1
69	2021-12-28 10:33:32.29183+05:30	6	Sri Ramakrishna Hospital (Multi-Speciality)	1	[{"added": {}}]	10	1
70	2021-12-28 10:34:09.60918+05:30	11	Tamil Nadu Government Multi-Super-Speciality Hospital-Bad	1	[{"added": {}}]	16	1
71	2021-12-28 10:34:15.564059+05:30	12	Tamil Nadu Government Multi-Super-Speciality Hospital-Oxygen	1	[{"added": {}}]	16	1
72	2021-12-28 10:34:35.354002+05:30	13	Tamil Nadu Government Multi-Super-Speciality Hospital-ECG Monitor	1	[{"added": {}}]	16	1
73	2021-12-28 10:34:39.991152+05:30	14	Tamil Nadu Government Multi-Super-Speciality Hospital-X - RAY	1	[{"added": {}}]	16	1
74	2021-12-28 10:34:44.574713+05:30	15	Tamil Nadu Government Multi-Super-Speciality Hospital-Refrigerator	1	[{"added": {}}]	16	1
75	2021-12-28 10:34:49.233269+05:30	16	Tamil Nadu Government Multi-Super-Speciality Hospital-Pulse oximeter	1	[{"added": {}}]	16	1
76	2021-12-28 10:34:54.019106+05:30	17	Tamil Nadu Government Multi-Super-Speciality Hospital-Patient monitor	1	[{"added": {}}]	16	1
77	2021-12-28 10:34:58.463128+05:30	18	Tamil Nadu Government Multi-Super-Speciality Hospital-Ambulance	1	[{"added": {}}]	16	1
78	2021-12-28 10:35:02.607555+05:30	19	Tamil Nadu Government Multi-Super-Speciality Hospital-Ventilator	1	[{"added": {}}]	16	1
79	2021-12-28 10:35:07.384634+05:30	20	DR.KAMAKSHI MEMORIAL HOSPITALS-Bad	1	[{"added": {}}]	16	1
80	2021-12-28 10:35:12.873022+05:30	21	DR.KAMAKSHI MEMORIAL HOSPITALS-ECG Monitor	1	[{"added": {}}]	16	1
81	2021-12-28 10:35:18.159806+05:30	22	DR.KAMAKSHI MEMORIAL HOSPITALS-Pulse oximeter	1	[{"added": {}}]	16	1
82	2021-12-28 10:35:23.213128+05:30	23	DR.KAMAKSHI MEMORIAL HOSPITALS-Ventilator	1	[{"added": {}}]	16	1
83	2021-12-28 10:35:38.423143+05:30	24	Government Hospital, Coimbatore (BIG)-Bad	1	[{"added": {}}]	16	1
84	2021-12-28 10:35:45.305452+05:30	25	Government Hospital, Coimbatore (BIG)-ECG Monitor	1	[{"added": {}}]	16	1
85	2021-12-28 10:35:50.280079+05:30	26	Government Hospital, Coimbatore (BIG)-X - RAY	1	[{"added": {}}]	16	1
86	2021-12-28 10:35:54.671568+05:30	27	Government Hospital, Coimbatore (BIG)-Pulse oximeter	1	[{"added": {}}]	16	1
87	2021-12-28 10:36:00.14124+05:30	28	Government Hospital, Coimbatore (BIG)-Ventilator	1	[{"added": {}}]	16	1
88	2021-12-28 10:36:05.630055+05:30	29	Konkunadu hospital-Bad	1	[{"added": {}}]	16	1
89	2021-12-28 10:36:10.919301+05:30	30	Konkunadu hospital-Oxygen	1	[{"added": {}}]	16	1
90	2021-12-28 10:36:16.736005+05:30	31	Konkunadu hospital-ECG Monitor	1	[{"added": {}}]	16	1
91	2021-12-28 10:36:21.391726+05:30	32	Konkunadu hospital-Refrigerator	1	[{"added": {}}]	16	1
92	2021-12-28 10:36:25.966103+05:30	33	Konkunadu hospital-Pulse oximeter	1	[{"added": {}}]	16	1
93	2021-12-28 10:36:30.334181+05:30	34	Konkunadu hospital-Ambulance	1	[{"added": {}}]	16	1
94	2021-12-28 10:36:34.391126+05:30	35	Konkunadu hospital-Ventilator	1	[{"added": {}}]	16	1
95	2021-12-28 10:36:39.060963+05:30	36	Konkunadu hospital-Ambulance	1	[{"added": {}}]	16	1
96	2021-12-28 10:36:44.331516+05:30	37	Sri Ramakrishna Hospital (Multi-Speciality)-Bad	1	[{"added": {}}]	16	1
97	2021-12-28 10:36:49.136999+05:30	38	Sri Ramakrishna Hospital (Multi-Speciality)-Ambulance	1	[{"added": {}}]	16	1
98	2021-12-28 10:36:54.074163+05:30	39	Sri Ramakrishna Hospital (Multi-Speciality)-Pulse oximeter	1	[{"added": {}}]	16	1
99	2021-12-28 10:37:36.641472+05:30	1	Government-Bad	1	[{"added": {}}]	15	1
100	2021-12-28 10:37:46.51879+05:30	2	Government-Oxygen	1	[{"added": {}}]	15	1
101	2021-12-28 10:42:58.283149+05:30	7	Ariyalur Government Hospital	1	[{"added": {}}]	10	1
102	2021-12-28 10:45:20.64352+05:30	8	ARIYALUR GOLDEN HOSPITAL PVT LTD	1	[{"added": {}}]	10	1
103	2021-12-28 10:47:18.464764+05:30	9	KMS HOSPITAL	1	[{"added": {}}]	10	1
104	2021-12-28 10:49:45.090186+05:30	10	Thanthai Periyar Government Headquarters Hospital	1	[{"added": {}}]	10	1
105	2021-12-28 11:06:29.135655+05:30	40	Ariyalur Government Hospital-ECG Monitor	1	[{"added": {}}]	16	1
106	2021-12-28 11:06:49.029811+05:30	41	Ariyalur Government Hospital-Ventilator	1	[{"added": {}}]	16	1
107	2021-12-28 11:07:02.674666+05:30	42	Ariyalur Government Hospital-ECG Monitor	1	[{"added": {}}]	16	1
108	2021-12-28 11:07:27.716152+05:30	43	ARIYALUR GOLDEN HOSPITAL PVT LTD-ECG Monitor	1	[{"added": {}}]	16	1
109	2021-12-28 11:07:32.560541+05:30	44	ARIYALUR GOLDEN HOSPITAL PVT LTD-Ventilator	1	[{"added": {}}]	16	1
110	2021-12-28 11:07:47.465157+05:30	45	ARIYALUR GOLDEN HOSPITAL PVT LTD-Pulse oximeter	1	[{"added": {}}]	16	1
111	2021-12-28 11:07:54.354569+05:30	46	KMS HOSPITAL-Oxygen	1	[{"added": {}}]	16	1
112	2021-12-28 11:08:00.592173+05:30	47	KMS HOSPITAL-Bad	1	[{"added": {}}]	16	1
113	2021-12-28 11:08:06.826218+05:30	48	KMS HOSPITAL-X - RAY	1	[{"added": {}}]	16	1
114	2021-12-28 11:08:12.416418+05:30	49	KMS HOSPITAL-Ambulance	1	[{"added": {}}]	16	1
115	2021-12-28 11:08:17.451538+05:30	50	KMS HOSPITAL-Ventilator	1	[{"added": {}}]	16	1
116	2021-12-28 11:08:23.402147+05:30	51	Thanthai Periyar Government Headquarters Hospital-Bad	1	[{"added": {}}]	16	1
117	2021-12-28 11:08:28.437116+05:30	52	Thanthai Periyar Government Headquarters Hospital-Oxygen	1	[{"added": {}}]	16	1
118	2021-12-28 11:08:34.889987+05:30	53	Thanthai Periyar Government Headquarters Hospital-ECG Monitor	1	[{"added": {}}]	16	1
119	2021-12-28 11:08:40.89798+05:30	54	Thanthai Periyar Government Headquarters Hospital-Refrigerator	1	[{"added": {}}]	16	1
120	2021-12-28 11:08:46.033615+05:30	55	Thanthai Periyar Government Headquarters Hospital-Pulse oximeter	1	[{"added": {}}]	16	1
121	2021-12-28 11:08:50.463719+05:30	56	Thanthai Periyar Government Headquarters Hospital-Ventilator	1	[{"added": {}}]	16	1
122	2021-12-28 12:00:05.451097+05:30	1	TamilNadu	2	[{"changed": {"fields": ["State name"]}}]	12	1
123	2021-12-28 12:06:26.303138+05:30	1	Bed	2	[{"changed": {"fields": ["Asset name"]}}]	7	1
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	assetmgt	asset
8	assetmgt	assetfiles
9	assetmgt	district
10	assetmgt	hospital
11	assetmgt	hospitaltype
12	assetmgt	state
13	assetmgt	userprofile
14	assetmgt	patientstat
15	assetmgt	htypeassetmapping
16	assetmgt	hospassetmapping
17	assetmgt	assetmgt
18	captcha	captchastore
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2021-12-27 12:05:09.021149+05:30
2	auth	0001_initial	2021-12-27 12:05:09.258473+05:30
3	admin	0001_initial	2021-12-27 12:05:09.715789+05:30
4	admin	0002_logentry_remove_auto_add	2021-12-27 12:05:09.803488+05:30
5	admin	0003_logentry_add_action_flag_choices	2021-12-27 12:05:09.825348+05:30
6	assetmgt	0001_initial	2021-12-27 12:05:10.397445+05:30
7	contenttypes	0002_remove_content_type_name	2021-12-27 12:05:11.076496+05:30
8	auth	0002_alter_permission_name_max_length	2021-12-27 12:05:11.095432+05:30
9	auth	0003_alter_user_email_max_length	2021-12-27 12:05:11.124314+05:30
10	auth	0004_alter_user_username_opts	2021-12-27 12:05:11.153652+05:30
11	auth	0005_alter_user_last_login_null	2021-12-27 12:05:11.182677+05:30
12	auth	0006_require_contenttypes_0002	2021-12-27 12:05:11.197654+05:30
13	auth	0007_alter_validators_add_error_messages	2021-12-27 12:05:11.224112+05:30
14	auth	0008_alter_user_username_max_length	2021-12-27 12:05:11.289077+05:30
15	auth	0009_alter_user_last_name_max_length	2021-12-27 12:05:11.325163+05:30
16	auth	0010_alter_group_name_max_length	2021-12-27 12:05:11.351032+05:30
17	auth	0011_update_proxy_permissions	2021-12-27 12:05:11.38223+05:30
18	captcha	0001_initial	2021-12-27 12:05:11.441059+05:30
19	sessions	0001_initial	2021-12-27 12:05:11.560191+05:30
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: covidast
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
00mwnvputqnzitl02c3uf512nds6ekwa	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-27 20:07:45.129827+05:30
ctvq1vxozvwq30xkx8ik0isb59m2vras	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-28 12:34:00.150708+05:30
dtqdvuwvrwrmu5f3k9ly73awgvwg8th6	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-28 10:19:40.571379+05:30
lihm5smrsci0ncdqgk8diz0qvo0v8z4s	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-28 11:29:49.284337+05:30
uio8ijwumahgkbcxqvpsq3508865gb19	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-28 11:31:02.082579+05:30
9szsejzu2t1xg9j3wcuq3mfj6bfy5osi	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-28 12:37:02.598147+05:30
5gl1h517ccne6q2v4meqxkk9003hrmky	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-28 11:47:10.087479+05:30
y6gajmiiw280n8wwo7p14yxen1hhzd0d	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-27 20:10:00.046654+05:30
bqn6xfwd2ohqgqr9n2q9jko45n46rxjm	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-28 12:26:26.120085+05:30
6y3wdp25d186m7z7da53p29tdqvrwtx8	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-28 12:58:33.850515+05:30
zmzz00rsfaqkjguap4cgnde3ybdmnzxa	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-27 20:11:07.4068+05:30
vjc0d1n9b94bz9alavmt5gf722z6gwap	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-28 12:27:01.055627+05:30
ajuqyugm0ke5v8housp5dlibhaa88bv8	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-28 17:14:38.465891+05:30
7k5vbaypcrlk4vxm833y2wkpdzbramwf	ODU2MDMxZjgyNTdlMmQ3ODEzNWQwZTYxODViMjg0Yjc0YjJkOWJmZjp7fQ==	2021-12-28 11:10:47.979793+05:30
59q7c9udld41bxgq6oomaa7mjguqnn13	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-28 10:43:02.335774+05:30
ucn47sgvirjeetvgxwi8apay5hoa3bmt	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-28 12:24:04.889285+05:30
t36f70shcfaqdm3uh7t1ag6wfz9ld8cq	Nzc4ZGFlOGZhZWQ3ZGI3ZmFkYTVkMjkwZDA1ODMzYzVjNjYzOGZlNDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI0NTM0MzQ4MTMxMTk4ZThlMzM4OGZmYmYyODliZmM3MmM2NGNlMGU2In0=	2021-12-28 12:16:17.771843+05:30
\.


--
-- Name: assetmgt_asset_asset_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.assetmgt_asset_asset_id_seq', 10, true);


--
-- Name: assetmgt_assetfiles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.assetmgt_assetfiles_id_seq', 1, false);


--
-- Name: assetmgt_assetmgt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.assetmgt_assetmgt_id_seq', 148, true);


--
-- Name: assetmgt_district_district_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.assetmgt_district_district_id_seq', 38, true);


--
-- Name: assetmgt_hospassetmapping_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.assetmgt_hospassetmapping_id_seq', 160, true);


--
-- Name: assetmgt_hospital_hospital_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.assetmgt_hospital_hospital_id_seq', 428, true);


--
-- Name: assetmgt_hospitaltype_htype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.assetmgt_hospitaltype_htype_id_seq', 2, true);


--
-- Name: assetmgt_htypeassetmapping_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.assetmgt_htypeassetmapping_id_seq', 2, true);


--
-- Name: assetmgt_patientstat_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.assetmgt_patientstat_id_seq', 1, false);


--
-- Name: assetmgt_state_state_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.assetmgt_state_state_id_seq', 1, true);


--
-- Name: assetmgt_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.assetmgt_userprofile_id_seq', 1, true);


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 72, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.auth_user_id_seq', 1, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.auth_user_user_permissions_id_seq', 1, false);


--
-- Name: captcha_captchastore_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.captcha_captchastore_id_seq', 38, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 123, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 18, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: covidast
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 19, true);


--
-- Name: assetmgt_asset assetmgt_asset_asset_name_key; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_asset
    ADD CONSTRAINT assetmgt_asset_asset_name_key UNIQUE (asset_name);


--
-- Name: assetmgt_asset assetmgt_asset_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_asset
    ADD CONSTRAINT assetmgt_asset_pkey PRIMARY KEY (asset_id);


--
-- Name: assetmgt_assetfiles assetmgt_assetfiles_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_assetfiles
    ADD CONSTRAINT assetmgt_assetfiles_pkey PRIMARY KEY (id);


--
-- Name: assetmgt_assetmgt assetmgt_assetmgt_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_assetmgt
    ADD CONSTRAINT assetmgt_assetmgt_pkey PRIMARY KEY (id);


--
-- Name: assetmgt_district assetmgt_district_district_name_key; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_district
    ADD CONSTRAINT assetmgt_district_district_name_key UNIQUE (district_name);


--
-- Name: assetmgt_district assetmgt_district_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_district
    ADD CONSTRAINT assetmgt_district_pkey PRIMARY KEY (district_id);


--
-- Name: assetmgt_hospassetmapping assetmgt_hospassetmapping_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_hospassetmapping
    ADD CONSTRAINT assetmgt_hospassetmapping_pkey PRIMARY KEY (id);


--
-- Name: assetmgt_hospital assetmgt_hospital_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_hospital
    ADD CONSTRAINT assetmgt_hospital_pkey PRIMARY KEY (hospital_id);


--
-- Name: assetmgt_hospitaltype assetmgt_hospitaltype_hospital_type_key; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_hospitaltype
    ADD CONSTRAINT assetmgt_hospitaltype_hospital_type_key UNIQUE (hospital_type);


--
-- Name: assetmgt_hospitaltype assetmgt_hospitaltype_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_hospitaltype
    ADD CONSTRAINT assetmgt_hospitaltype_pkey PRIMARY KEY (htype_id);


--
-- Name: assetmgt_htypeassetmapping assetmgt_htypeassetmapping_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_htypeassetmapping
    ADD CONSTRAINT assetmgt_htypeassetmapping_pkey PRIMARY KEY (id);


--
-- Name: assetmgt_patientstat assetmgt_patientstat_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_patientstat
    ADD CONSTRAINT assetmgt_patientstat_pkey PRIMARY KEY (id);


--
-- Name: assetmgt_state assetmgt_state_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_state
    ADD CONSTRAINT assetmgt_state_pkey PRIMARY KEY (state_id);


--
-- Name: assetmgt_state assetmgt_state_state_name_key; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_state
    ADD CONSTRAINT assetmgt_state_state_name_key UNIQUE (state_name);


--
-- Name: assetmgt_userprofile assetmgt_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_userprofile
    ADD CONSTRAINT assetmgt_userprofile_pkey PRIMARY KEY (id);


--
-- Name: assetmgt_userprofile assetmgt_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_userprofile
    ADD CONSTRAINT assetmgt_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: captcha_captchastore captcha_captchastore_hashkey_key; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.captcha_captchastore
    ADD CONSTRAINT captcha_captchastore_hashkey_key UNIQUE (hashkey);


--
-- Name: captcha_captchastore captcha_captchastore_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.captcha_captchastore
    ADD CONSTRAINT captcha_captchastore_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: assetmgt_asset_asset_name_f9f65e28_like; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_asset_asset_name_f9f65e28_like ON public.assetmgt_asset USING btree (asset_name varchar_pattern_ops);


--
-- Name: assetmgt_asset_author_id_c81c8549; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_asset_author_id_c81c8549 ON public.assetmgt_asset USING btree (author_id);


--
-- Name: assetmgt_assetmgt_asset_id_id_dbb84dcc; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_assetmgt_asset_id_id_dbb84dcc ON public.assetmgt_assetmgt USING btree (asset_id_id);


--
-- Name: assetmgt_assetmgt_author_id_ade0a1a7; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_assetmgt_author_id_ade0a1a7 ON public.assetmgt_assetmgt USING btree (author_id);


--
-- Name: assetmgt_assetmgt_hospital_id_id_2021d4f2; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_assetmgt_hospital_id_id_2021d4f2 ON public.assetmgt_assetmgt USING btree (hospital_id_id);


--
-- Name: assetmgt_district_district_name_23250e03_like; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_district_district_name_23250e03_like ON public.assetmgt_district USING btree (district_name varchar_pattern_ops);


--
-- Name: assetmgt_district_state_id_id_db08d406; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_district_state_id_id_db08d406 ON public.assetmgt_district USING btree (state_id_id);


--
-- Name: assetmgt_hospassetmapping_assetsmapped_id_2fbab786; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_hospassetmapping_assetsmapped_id_2fbab786 ON public.assetmgt_hospassetmapping USING btree (assetsmapped_id);


--
-- Name: assetmgt_hospassetmapping_hospital_id_d5cc4472; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_hospassetmapping_hospital_id_d5cc4472 ON public.assetmgt_hospassetmapping USING btree (hospital_id);


--
-- Name: assetmgt_hospital_district_id_id_6852b523; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_hospital_district_id_id_6852b523 ON public.assetmgt_hospital USING btree (district_id_id);


--
-- Name: assetmgt_hospital_htype_id_58ca6e59; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_hospital_htype_id_58ca6e59 ON public.assetmgt_hospital USING btree (htype_id);


--
-- Name: assetmgt_hospital_state_id_id_57fec823; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_hospital_state_id_id_57fec823 ON public.assetmgt_hospital USING btree (state_id_id);


--
-- Name: assetmgt_hospitaltype_hospital_type_4db95940_like; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_hospitaltype_hospital_type_4db95940_like ON public.assetmgt_hospitaltype USING btree (hospital_type varchar_pattern_ops);


--
-- Name: assetmgt_htypeassetmapping_assetsmapped_id_c5568d6b; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_htypeassetmapping_assetsmapped_id_c5568d6b ON public.assetmgt_htypeassetmapping USING btree (assetsmapped_id);


--
-- Name: assetmgt_htypeassetmapping_district_id_390078ea; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_htypeassetmapping_district_id_390078ea ON public.assetmgt_htypeassetmapping USING btree (district_id);


--
-- Name: assetmgt_htypeassetmapping_htype_id_48df376f; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_htypeassetmapping_htype_id_48df376f ON public.assetmgt_htypeassetmapping USING btree (htype_id);


--
-- Name: assetmgt_htypeassetmapping_state_id_3623e9a2; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_htypeassetmapping_state_id_3623e9a2 ON public.assetmgt_htypeassetmapping USING btree (state_id);


--
-- Name: assetmgt_patientstat_author_id_aee891f0; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_patientstat_author_id_aee891f0 ON public.assetmgt_patientstat USING btree (author_id);


--
-- Name: assetmgt_patientstat_hospital_id_id_5cdf57c6; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_patientstat_hospital_id_id_5cdf57c6 ON public.assetmgt_patientstat USING btree (hospital_id_id);


--
-- Name: assetmgt_state_state_name_1fc52777_like; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_state_state_name_1fc52777_like ON public.assetmgt_state USING btree (state_name varchar_pattern_ops);


--
-- Name: assetmgt_userprofile_district_id_id_6cc648bc; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_userprofile_district_id_id_6cc648bc ON public.assetmgt_userprofile USING btree (district_id_id);


--
-- Name: assetmgt_userprofile_hospital_id_id_98792cb0; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_userprofile_hospital_id_id_98792cb0 ON public.assetmgt_userprofile USING btree (hospital_id_id);


--
-- Name: assetmgt_userprofile_state_id_id_f808b07a; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX assetmgt_userprofile_state_id_id_f808b07a ON public.assetmgt_userprofile USING btree (state_id_id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX auth_group_name_a6ea08ec_like ON public.auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON public.auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON public.auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON public.auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX auth_user_groups_group_id_97559544 ON public.auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON public.auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON public.auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON public.auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX auth_user_username_6821ab7c_like ON public.auth_user USING btree (username varchar_pattern_ops);


--
-- Name: captcha_captchastore_hashkey_cbe8d15a_like; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX captcha_captchastore_hashkey_cbe8d15a_like ON public.captcha_captchastore USING btree (hashkey varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON public.django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON public.django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX django_session_expire_date_a5c62663 ON public.django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: covidast
--

CREATE INDEX django_session_session_key_c0390e0f_like ON public.django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: assetmgt_asset assetmgt_asset_author_id_c81c8549_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_asset
    ADD CONSTRAINT assetmgt_asset_author_id_c81c8549_fk_auth_user_id FOREIGN KEY (author_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_assetmgt assetmgt_assetmgt_asset_id_id_dbb84dcc_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_assetmgt
    ADD CONSTRAINT assetmgt_assetmgt_asset_id_id_dbb84dcc_fk_assetmgt_ FOREIGN KEY (asset_id_id) REFERENCES public.assetmgt_asset(asset_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_assetmgt assetmgt_assetmgt_author_id_ade0a1a7_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_assetmgt
    ADD CONSTRAINT assetmgt_assetmgt_author_id_ade0a1a7_fk_auth_user_id FOREIGN KEY (author_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_assetmgt assetmgt_assetmgt_hospital_id_id_2021d4f2_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_assetmgt
    ADD CONSTRAINT assetmgt_assetmgt_hospital_id_id_2021d4f2_fk_assetmgt_ FOREIGN KEY (hospital_id_id) REFERENCES public.assetmgt_hospital(hospital_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_district assetmgt_district_state_id_id_db08d406_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_district
    ADD CONSTRAINT assetmgt_district_state_id_id_db08d406_fk_assetmgt_ FOREIGN KEY (state_id_id) REFERENCES public.assetmgt_state(state_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_hospassetmapping assetmgt_hospassetma_assetsmapped_id_2fbab786_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_hospassetmapping
    ADD CONSTRAINT assetmgt_hospassetma_assetsmapped_id_2fbab786_fk_assetmgt_ FOREIGN KEY (assetsmapped_id) REFERENCES public.assetmgt_asset(asset_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_hospassetmapping assetmgt_hospassetma_hospital_id_d5cc4472_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_hospassetmapping
    ADD CONSTRAINT assetmgt_hospassetma_hospital_id_d5cc4472_fk_assetmgt_ FOREIGN KEY (hospital_id) REFERENCES public.assetmgt_hospital(hospital_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_hospital assetmgt_hospital_district_id_id_6852b523_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_hospital
    ADD CONSTRAINT assetmgt_hospital_district_id_id_6852b523_fk_assetmgt_ FOREIGN KEY (district_id_id) REFERENCES public.assetmgt_district(district_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_hospital assetmgt_hospital_htype_id_58ca6e59_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_hospital
    ADD CONSTRAINT assetmgt_hospital_htype_id_58ca6e59_fk_assetmgt_ FOREIGN KEY (htype_id) REFERENCES public.assetmgt_hospitaltype(htype_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_hospital assetmgt_hospital_state_id_id_57fec823_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_hospital
    ADD CONSTRAINT assetmgt_hospital_state_id_id_57fec823_fk_assetmgt_ FOREIGN KEY (state_id_id) REFERENCES public.assetmgt_state(state_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_htypeassetmapping assetmgt_htypeassetm_assetsmapped_id_c5568d6b_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_htypeassetmapping
    ADD CONSTRAINT assetmgt_htypeassetm_assetsmapped_id_c5568d6b_fk_assetmgt_ FOREIGN KEY (assetsmapped_id) REFERENCES public.assetmgt_asset(asset_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_htypeassetmapping assetmgt_htypeassetm_district_id_390078ea_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_htypeassetmapping
    ADD CONSTRAINT assetmgt_htypeassetm_district_id_390078ea_fk_assetmgt_ FOREIGN KEY (district_id) REFERENCES public.assetmgt_district(district_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_htypeassetmapping assetmgt_htypeassetm_htype_id_48df376f_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_htypeassetmapping
    ADD CONSTRAINT assetmgt_htypeassetm_htype_id_48df376f_fk_assetmgt_ FOREIGN KEY (htype_id) REFERENCES public.assetmgt_hospitaltype(htype_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_htypeassetmapping assetmgt_htypeassetm_state_id_3623e9a2_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_htypeassetmapping
    ADD CONSTRAINT assetmgt_htypeassetm_state_id_3623e9a2_fk_assetmgt_ FOREIGN KEY (state_id) REFERENCES public.assetmgt_state(state_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_patientstat assetmgt_patientstat_author_id_aee891f0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_patientstat
    ADD CONSTRAINT assetmgt_patientstat_author_id_aee891f0_fk_auth_user_id FOREIGN KEY (author_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_patientstat assetmgt_patientstat_hospital_id_id_5cdf57c6_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_patientstat
    ADD CONSTRAINT assetmgt_patientstat_hospital_id_id_5cdf57c6_fk_assetmgt_ FOREIGN KEY (hospital_id_id) REFERENCES public.assetmgt_hospital(hospital_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_userprofile assetmgt_userprofile_district_id_id_6cc648bc_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_userprofile
    ADD CONSTRAINT assetmgt_userprofile_district_id_id_6cc648bc_fk_assetmgt_ FOREIGN KEY (district_id_id) REFERENCES public.assetmgt_district(district_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_userprofile assetmgt_userprofile_hospital_id_id_98792cb0_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_userprofile
    ADD CONSTRAINT assetmgt_userprofile_hospital_id_id_98792cb0_fk_assetmgt_ FOREIGN KEY (hospital_id_id) REFERENCES public.assetmgt_hospital(hospital_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_userprofile assetmgt_userprofile_state_id_id_f808b07a_fk_assetmgt_; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_userprofile
    ADD CONSTRAINT assetmgt_userprofile_state_id_id_f808b07a_fk_assetmgt_ FOREIGN KEY (state_id_id) REFERENCES public.assetmgt_state(state_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: assetmgt_userprofile assetmgt_userprofile_user_id_2658e208_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.assetmgt_userprofile
    ADD CONSTRAINT assetmgt_userprofile_user_id_2658e208_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES public.auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES public.auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES public.django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: covidast
--

ALTER TABLE ONLY public.django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES public.auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

