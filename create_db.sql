

CREATE TABLE IF NOT EXISTS public.country
(
    id serial,
    name character varying(80) COLLATE pg_catalog."default",
    code character(6) COLLATE pg_catalog."default",
    CONSTRAINT country_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.geocoded
(
    location_name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    raw_geo_data json,
    CONSTRAINT pk_location PRIMARY KEY (location_name)
);

CREATE TABLE IF NOT EXISTS public.place
(
    id character varying(80) COLLATE pg_catalog."default" NOT NULL,
    url character varying(255) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    place_type character varying(80) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    name character varying(80) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    full_name character varying(255) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    country_id integer,
    bounding_box polygon,
    country_name character varying(80) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    country_code character(6) COLLATE pg_catalog."default" DEFAULT NULL::bpchar,
    CONSTRAINT place_pkey PRIMARY KEY (id),
    CONSTRAINT fk_place_country FOREIGN KEY (country_id)
        REFERENCES public.country (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

CREATE TABLE IF NOT EXISTS public.tweet_collection
(
    id serial,
    started timestamp with time zone,
    finished timestamp with time zone,
    keywords character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT pk_tweet_collection_id PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.tweet
(
    id serial,
    text character varying(1000) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    created_at timestamp with time zone,
    coordinates character varying(255) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    lang character varying(20) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    retweeted boolean,
    is_quote boolean,
    is_reply boolean,
    place_id character varying(80) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    user_id bigint,
    user_geo_enabled boolean,
    user_lang character varying(20) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    user_place character varying(200) COLLATE pg_catalog."default" DEFAULT NULL::character varying,
    collection_id integer,
    user_location character varying(200) COLLATE pg_catalog."default",
    CONSTRAINT tweet_pkey PRIMARY KEY (id),
    CONSTRAINT fk_collection_id FOREIGN KEY (collection_id)
        REFERENCES public.tweet_collection (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT fk_tweet_place FOREIGN KEY (place_id)
        REFERENCES public.place (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO pesquisa;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO pesquisa;
