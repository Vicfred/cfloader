select * from codeforcer;
select count(*) from codeforcer;
select * from codeforcer where handle = 'Vicfred';
SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle WHERE country = 'Mexico' GROUP BY codeforcer.handle ORDER BY participations DESC;
SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations, country FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle GROUP BY codeforcer.handle ORDER BY participations DESC;
SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations, country FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle WHERE rating >= 1900 GROUP BY codeforcer.handle ORDER BY participations DESC;

SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations, country FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle GROUP BY codeforcer.handle HAVING count(codeforcer.handle) >= 100 ORDER BY rating DESC;

select * from contest;

select * from rating_change where handle = 'Vicfred';
select count(*) from rating_change;

select * from submission where "programmingLanguage" = 'D' and "verdict" = 'OK';