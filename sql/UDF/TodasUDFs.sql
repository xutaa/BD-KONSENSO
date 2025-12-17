-- =============================================
-- UDF: HashPassword
-- Descrição: Gera um hash SHA2_256 para uma password fornecida.
-- =============================================
CREATE OR ALTER FUNCTION dbo.HashPassword(@Password NVARCHAR(100))
RETURNS NVARCHAR(100)
AS BEGIN
	DECLARE @HashThis NVARCHAR(4000)
	DECLARE @Hash VARBINARY(32)

	SET @HashThis = @Password
	SET @Hash = HASHBYTES('SHA2_256', @HashThis)

	RETURN CONVERT(NVARCHAR(100), @Hash, 1)
END
GO
-- TODO: Ainda nao usada