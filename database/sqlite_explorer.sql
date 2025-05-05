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

