CREATE TABLE [dbo].[Dogs] (
    [Handle] [varchar](50) NOT NULL,
    [Name] [varchar](50) NOT NULL,
    [Bio] [text] NULL,
    [Age] [int] NULL
);

ALTER TABLE [dbo].[Dogs]
ALTER COLUMN [Password] [varchar](100) NOT NULL

UPDATE [dbo].[Dogs]
SET [Password] = 'pbkdf2:sha256:150000$p3XX5E60$738e098d4aab8a006c545e5e2b35bb0ca826193bac4edfb66ad14b788f4b9455'
WHERE [Handle] = 'chucky'

SELECT * FROM Dogs