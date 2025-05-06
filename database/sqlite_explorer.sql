-- SQLite
select cf.event_date, md.state, cf.campaign_product, cd.spent_amt, cf.conversion_channel_nm, 
sum(click_qty), sum(impression_qty), SUM(quote_start),SUM(quote_COMPLETE) from campaign_fact cf, member_dim md, campaign_dim cd
where cf.member_number = md.member_number
and cf.campaign_nm = cd.campaign_nm
GROUP BY cf.event_date, md.state, cf.campaign_product, 
cd.spent_amt, cf.conversion_channel_nm;
--select * from campaign_fact 
--WHERE campaign_nm IN (SELECT DISTINCT campaign_nm FROM 
--campaign_dim)
--AND member_number IN (SELECT DISTINCT member_number FROM member_dim)

drop table if exists directmail_agg;
drop TABLE IF EXISTS email_agg;
drop table if exists paid_search_agg;
drop table if exists paid_display_agg;
drop table if exists paid_social_agg;

create table if not exists member_dim (member_id text, age_grp text, marital_status text, 
military_status text,
       member_status text, active_pnc text, active_bank text, active_life text,
       active_credit_card text, active_deposits text, active_auto_insurance text,
       active_homeowners text, active_renters text, active_life_insurance text,
       geo_city text);

create table if not exists evt_search_dtl  (
event_date text, member_id text, mkt_channel text, campaign_name text,
       campaign_product text, conversion_product text, conversion_channel text,
       conversion_type text,
       FOREIGN KEY (member_id) REFERENCES member_dim(member_id));
create table if not exists evt_social_dtl  (
event_date text, member_id text, mkt_channel text, campaign_name text,
       campaign_product text, conversion_product text, conversion_channel text,
       conversion_type text,
       FOREIGN KEY (member_id) REFERENCES member_dim(member_id));
create table if not exists evt_display_dtl  (
event_date text, member_id text, mkt_channel text, campaign_name text,
       campaign_product text, conversion_product text, conversion_channel text,
       conversion_type text,
       FOREIGN KEY (member_id) REFERENCES member_dim(member_id));
create table if not exists evt_email_dtl  (
event_date text, member_id text, mkt_channel text, campaign_name text,
       campaign_product text, conversion_product text, conversion_channel text,
       conversion_type text,
       FOREIGN KEY (member_id) REFERENCES member_dim(member_id));
create table if not exists evt_dm_dtl  (
event_date text, member_id text, mkt_channel text, campaign_name text,
       campaign_product text, conversion_product text, conversion_channel text,
       conversion_type text,
       FOREIGN KEY (member_id) REFERENCES member_dim(member_id));


create table paid_display_agg (
event_date text,  campaign_product text,  campaign_cosa text,  converted_product text, 
       converted_cosa text,  campaign_nm text,  conversion_channel_nm text,  spend_amt integer, 
       quote_start_qty integer,  quote_complete_qty integer,  app_start_qty integer, 
       app_complete_qty integer,  prod_acq_qty integer,  impression_qty integer,  click_qty integer, 
       campaign_funding_source text);
create table paid_social_agg (
event_date text,  campaign_product text,  campaign_cosa text,  converted_product text, 
       converted_cosa text,  campaign_nm text,  conversion_channel_nm text,  spend_amt integer, 
       quote_start_qty integer,  quote_complete_qty integer,  app_start_qty integer, 
       app_complete_qty integer,  prod_acq_qty integer,  impression_qty integer,  click_qty integer, 
       campaign_funding_source text);

create table paid_search_agg (
event_date text,  campaign_product text,  campaign_cosa text,  converted_product text, 
       converted_cosa text,  campaign_nm text,  conversion_channel_nm text,  spend_amt integer, 
       quote_start_qty integer,  quote_complete_qty integer,  app_start_qty integer, 
       app_complete_qty integer,  prod_acq_qty integer,  impression_qty integer,  click_qty integer, 
       campaign_funding_source text);

create table email_agg (
event_date text,  campaign_product text,  campaign_cosa text,  converted_product text, 
       converted_cosa text,  campaign_nm text,  conversion_channel_nm text,  spend_amt integer, 
       quote_start_qty integer,  quote_complete_qty integer,  app_start_qty integer, 
       app_complete_qty integer,  prod_acq_qty integer,  impression_qty integer,  click_qty integer, 
       campaign_funding_source text);
create table directmail_agg (
event_date text,  campaign_product text,  campaign_cosa text,  converted_product text, 
       converted_cosa text,  campaign_nm text,  conversion_channel_nm text,  spend_amt integer, 
       quote_start_qty integer,  quote_complete_qty integer,  app_start_qty integer, 
       app_complete_qty integer,  prod_acq_qty integer,  impression_qty integer,  click_qty integer, 
       campaign_funding_source text);

alter table evt_dm_dtl rename to evt_directmail_dtl;

select distinct event_date from paid_search_agg;

SELECT distinct campaign_product FROM paid_search_agg WHERE lower(campaign_product) = lower('Auto insurance')

SELECT campaign_product, SUM(quote_start_qty) FROM paid_search_agg WHERE 
event_date BETWEEN '2025-01-01' AND '2025-01-15' AND lower(campaign_product) 
IN ('auto insurance', 'homeowners insurance', 'renters insurance') GROUP BY campaign_product

select * from paid_search_agg WHERE event_date BETWEEN '2025-01-01' AND '2025-01-15'
create table campaign_agg (
event_date text,  campaign_product text,  campaign_cosa text,  converted_product text, 
       converted_cosa text,  campaign_nm text, spend_amt integer, 
       quote_start_qty integer,  quote_complete_qty integer,  app_start_qty integer, 
       app_complete_qty integer,  prod_acq_qty integer,  impression_qty integer,  click_qty integer, 
       campaign_funding_source text, onversion_channel_nm text);

insert into campaign_agg
select event_date, campaign_product, campaign_cosa, converted_product, 
       converted_cosa, campaign_nm, spend_amt, quote_start_qty, quote_complete_qty, 
       app_start_qty, app_complete_qty, prod_acq_qty, impression_qty, click_qty,
       campaign_funding_source, 'paid_search' as conversion_channel_nm
       from paid_search_agg
    union ALL
    select event_date, campaign_product, campaign_cosa, converted_product, 
       converted_cosa, campaign_nm, spend_amt, quote_start_qty, quote_complete_qty, 
       app_start_qty, app_complete_qty, prod_acq_qty, impression_qty, click_qty,
       campaign_funding_source, 'paid_social' as conversion_channel_nm
       from paid_search_agg
       union ALL
       select event_date, campaign_product, campaign_cosa, converted_product, 
       converted_cosa, campaign_nm, spend_amt, quote_start_qty, quote_complete_qty, 
       app_start_qty, app_complete_qty, prod_acq_qty, impression_qty, click_qty,
       campaign_funding_source, 'paid_display' as conversion_channel_nm
       from paid_search_agg
       union all
       select event_date, campaign_product, campaign_cosa, converted_product, 
       converted_cosa, campaign_nm, spend_amt, quote_start_qty, quote_complete_qty, 
       app_start_qty, app_complete_qty, prod_acq_qty, impression_qty, click_qty,
       campaign_funding_source, 'email' as conversion_channel_nm
       from paid_search_agg
       union all
       select event_date, campaign_product, campaign_cosa, converted_product, 
       converted_cosa, campaign_nm, spend_amt, quote_start_qty, quote_complete_qty, 
       app_start_qty, app_complete_qty, prod_acq_qty, impression_qty, click_qty,
       campaign_funding_source, 'direct_mail' as conversion_channel_nm
       from paid_search_agg


create table if not exists marketing_event_dtl  (
event_date text, member_id text, mkt_channel text, campaign_name text,
       campaign_product text, conversion_product text, conversion_channel text,
       conversion_type text,
       FOREIGN KEY (member_id) REFERENCES member_dim(member_id));

insert into marketing_event_dtl
select * from evt_search_dtl 
UNION ALL
select * from evt_social_dtl
UNION ALL
select * from evt_display_dtl
UNION ALL
select * from evt_email_dtl
UNION ALL
select * from evt_directmail_dtl


drop table evt_directmail_dtl;
drop table evt_email_dtl;
drop table evt_display_dtl;
drop table evt_social_dtl;
drop table evt_search_dtl;

drop table marketing_event_dtl

drop table orders;
drop table product;
drop table customer;