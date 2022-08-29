-- Number of Ungeocoded Tweets
select count(t.user_location) from tweet t
left outer join geocoded g on t.user_location = g.location_name
where t.user_location is not null
and g.location_name is null

-- Number of (successfully) Geocoded Tweets
select count(t.user_location) from tweet t
inner join geocoded g on t.user_location = g.location_name
where t.user_location is not null
and g.raw_geo_data::text != '[]'

-- Ungeocoded locations ordered by frequency
select t.user_location, count(t.user_location) as ct from tweet t
left outer join geocoded g on t.user_location = g.location_name
where t.user_location is not null
and g.location_name is null
group by t.user_location
order by ct desc

-- Most frequent locations
select user_location as loc, count(*) as ct from tweet
group by loc
order by ct desc;

-- Non-place locations
select t.user_location, count(t.user_location) as ct from tweet t
inner join geocoded g on t.user_location = g.location_name
where t.user_location is not null
and g.raw_geo_data::text = '[]'
group by t.user_location
order by ct desc

-- View number of tweets by day
select date_trunc('day', created_at) as dia, count(*) from tweet
group by dia
