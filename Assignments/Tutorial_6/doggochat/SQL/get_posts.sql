-- INSERT INTO Posts ([Handle], [Text], [Time])
-- VALUES ('melba', 'I''m so excited to move to California! @rose @invalid', '20210122 20:47:05'),
--     ('melba', 'Great game of fetch today with my Dad, Paul', '20210122 05:04:31'),
--     ('chucky', 'Took a great 8 hour nap today, then guarded the household', '20210120 00:00:00'),
--     ('melba', 'Peanut butter is my favorite snack! @chucky @rose', '20210113 12:54:33'),
--     ('rose', 'Today I stole food from a blind dog.', '20181212 04:42:20')

-- DROP TABLE Posts
SELECT * FROM Posts

SELECT
    Posts.Id,
    Posts.Handle,
    Posts.Text,
    Posts.Time,
    Dogs.Name,
    Dogs.AvatarImageName,
    LikeCountQueryResult.LikeCount

FROM Posts

INNER JOIN Dogs ON Posts.Handle = Dogs.Handle

INNER JOIN (
    SELECT
        Posts.Id, 
        COUNT(Likes.Handle) AS LikeCount
    FROM Posts
    LEFT JOIN Likes
        ON Posts.Id = Likes.PostId
    GROUP BY Id) LikeCountQueryResult 
    ON LikeCountQueryResult.Id = Posts.Id

ORDER BY Posts.Time DESC


SELECT * from Likes

-- INSERT INTO Likes ([Handle], [PostId])
-- VALUES 
--     ('chucky', 1),
--     ('chucky', 2),
--     ('rose', 3),
--     ('rose', 4),
--     ('rose', 1),
--     ('melba', 3),
--     ('chucky', 4),
--     ('melba', 4)
    