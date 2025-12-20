-- =============================================
-- UDF: ValidarNIF
-- Descrição: Valida se um NIF (Número de Identificação Fiscal) português é válido.
-- =============================================
CREATE OR ALTER FUNCTION dbo.ValidarNIF(@NIF VARCHAR(9))
RETURNS BIT
AS BEGIN
    IF LEN(@NIF) <> 9 RETURN 0;
    IF @NIF NOT LIKE '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]' RETURN 0;
    RETURN 1;
END
GO
