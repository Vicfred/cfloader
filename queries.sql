select * from codeforcer;
select count(*) from codeforcer;

select * from codeforcer where handle = 'Vicfred';

SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle WHERE country = 'Mexico' GROUP BY codeforcer.handle ORDER BY participations DESC;

-- Members in Iberian countries sorted by number of participations in official contests
SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations, country
FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle
WHERE country = 'Brazil' OR country = 'Argentina' OR country = 'Mexico' OR country = 'Spain' OR country = 'Cuba' OR country = 'Peru' OR country = 'Portugal' OR country = 'Colombia' OR country = 'Dominican Republic' OR country = 'Chile' OR country = 'Venezuela' OR country = 'Bolivia' OR country = 'El Salvador' OR country = 'Uruguay' OR country = 'Puerto Rico' OR country = 'Nicaragua' OR country = 'Paraguay'
GROUP BY codeforcer.handle ORDER BY participations DESC;

-- Members in North America sorted by number of participations in official contests
SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations, country
FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle
WHERE country = 'United States' OR country = 'Canada' OR country = 'Mexico'
GROUP BY codeforcer.handle ORDER BY participations DESC;

-- Members in Europe sorted by number of participations in official contests
SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations, country
FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle
WHERE country = 'Germany' OR country = 'United Kingdom' OR country = 'France' OR country = 'Italy' OR country = 'Russia' OR country = 'Spain' OR country = 'Netherlands' OR country = 'Switzerland' OR country = 'Poland' OR country = 'Sweden' OR country = 'Finland' OR country = 'Czechia' OR country = 'Romania' OR country = 'Portugal' OR country = 'Greece' OR country = 'Hungary' OR country = 'Slovakia' OR country = 'Ukraine' OR country = 'Bulgaria' OR country = 'Croatia' OR country = 'Latvia' OR country = 'Estonia' OR country = 'Serbia' OR country = 'Armenia' OR country = 'Moldova' OR country = 'Belarus' OR country = 'Romania' OR country = 'Kazakhstan' OR country = 'Lithuania' OR country = 'Georgia' OR country = 'Serbia' OR country = 'Uzbekistan'
GROUP BY codeforcer.handle ORDER BY participations DESC;

-- Members in Asia TOP 10 sorted by number of participations in official contests
SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations, country
FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle
WHERE country = 'China' OR country = 'Japan' OR country = 'South Korea' OR country = 'Taiwan'
GROUP BY codeforcer.handle ORDER BY participations DESC;

-- Members in Asia TOP 20 sorted by number of participations in official contests
SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations, country
FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle
WHERE country = 'China' OR country = 'Japan' OR country = 'South Korea' OR country = 'Taiwan' OR country = 'Vietnam' OR country = 'Indonesia' OR country = 'Hong Kong' OR country = 'North Korea'
GROUP BY codeforcer.handle ORDER BY participations DESC;

-- Members sorted by number of contests
SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations, country FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle GROUP BY codeforcer.handle ORDER BY participations DESC;
-- Members with more than 100 contests sorted by rating
SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations, country FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle GROUP BY codeforcer.handle HAVING count(codeforcer.handle) >= 100 ORDER BY rating DESC;
-- Members with more than 1900 rating sorted by number of contests
SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations, country FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle WHERE rating >= 1900 GROUP BY codeforcer.handle ORDER BY participations DESC;
-- Members with lots of participations but low rating
SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations, country FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle WHERE rating <= 1600 GROUP BY codeforcer.handle HAVING count(codeforcer.handle) >= 80 ORDER BY participations DESC;
-- Members with more than 1900 rating ordered by number of contests
SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations, country FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle WHERE rating >= 1900 GROUP BY codeforcer.handle ORDER BY participations DESC;
-- Members with more than 100 participations
SELECT codeforcer.handle, rating, "maxRating", count(codeforcer.handle) AS participations, country FROM codeforcer INNER JOIN rating_change ON rating_change.handle=codeforcer.handle GROUP BY codeforcer.handle HAVING count(codeforcer.handle) >= 100 ORDER BY rating DESC;

select * from contest;

select * from rating_change where handle = 'Vicfred';
select count(*) from rating_change;

select * from submission where "programmingLanguage" = 'D' and "verdict" = 'OK';
