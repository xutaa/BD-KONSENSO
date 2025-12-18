-- =============================================
-- UDF: HashPassword
-- Descrição: Gera um hash SHA2_256 para uma password fornecida.
-- =============================================
CREATE OR ALTER FUNCTION dbo.HashPassword(@Password NVARCHAR(100))
RETURNS NVARCHAR(100)
AS BEGIN
	DECLARE @HashThis NVARCHAR(2056)
	DECLARE @Hash VARBINARY(32)

	SET @HashThis = @Password
	SET @Hash = HASHBYTES('SHA2_256', @HashThis)

	RETURN CONVERT(NVARCHAR(100), @Hash, 1)
END
GO

-- =============================================
-- UDF: ValidarNIF
-- Descrição: Valida se um NIF (Número de Identificação Fiscal) português é válido.
-- =============================================
CREATE FUNCTION dbo.ValidarNIF(@NIF VARCHAR(9))
RETURNS BIT
AS BEGIN
    IF LEN(@NIF) <> 9 RETURN 0;
    IF @NIF NOT LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' RETURN 0;
    RETURN 1;
END;


-- TODO: Ainda NADA usado