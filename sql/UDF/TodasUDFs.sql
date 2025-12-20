-- =============================================
-- TODAS AS UDFs - BD-KONSENSO
-- Executa este ficheiro no SSMS para criar todas as UDFs
-- =============================================

USE p2g4;
GO

-- =============================================
-- UDF 1: HashPassword
-- =============================================
CREATE OR ALTER FUNCTION dbo.HashPassword(@Password NVARCHAR(100))
RETURNS NVARCHAR(100)
AS BEGIN
    DECLARE @Hash VARBINARY(32)
    SET @Hash = HASHBYTES('SHA2_256', @Password)
    RETURN CONVERT(NVARCHAR(100), @Hash, 1)
END
GO

-- =============================================
-- UDF 2: ValidarNIF
-- =============================================
CREATE OR ALTER FUNCTION dbo.ValidarNIF(@NIF VARCHAR(9))
RETURNS BIT
AS BEGIN
    IF LEN(@NIF) <> 9 RETURN 0;
    IF @NIF NOT LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' RETURN 0;
    RETURN 1;
END
GO

PRINT '✅ Todas as 2 UDFs criadas com sucesso!';
GO