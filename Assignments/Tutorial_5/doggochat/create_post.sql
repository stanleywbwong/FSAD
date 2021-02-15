CREATE TABLE [dbo].[Posts] (
    [Id] INT IDENTITY,
    [Handle] [varchar](50) NOT NULL,
    [Text] [varchar](200) NOT NULL,
    [Time] DATETIME NOT NULL
);