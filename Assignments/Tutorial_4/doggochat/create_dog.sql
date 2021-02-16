CREATE TABLE [dbo].[Dogs] (
    [Handle] [varchar](50) NOT NULL,
    [Name] [varchar](50) NOT NULL,
    [Bio] [text] NULL,
    [Age] [int] NULL
);

ALTER TABLE [dbo].[Dogs]
ALTER COLUMN [Password] [varchar](100) NOT NULL

UPDATE [dbo].[Dogs]
SET [Password] = 'pbkdf2:sha256:150000$Y8NtAVQI$6a79d843db32ba1dc77ada96104da4143628c56b697e88bc0b66ee591065b426'
WHERE [Handle] = 'rose'

SELECT * FROM Dogs