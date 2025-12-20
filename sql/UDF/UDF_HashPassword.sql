-- =============================================
-- UDF: HashPassword
-- Descrição: Gera um hash SHA2_256 para uma password fornecida.
-- =============================================
CREATE OR ALTER FUNCTION dbo.HashPassword(@Password NVARCHAR(100))
RETURNS NVARCHAR(100)
AS BEGIN
    DECLARE @Hash VARBINARY(32)
    SET @Hash = HASHBYTES('SHA2_256', @Password)
    RETURN CONVERT(NVARCHAR(100), @Hash, 1)
END
GO
