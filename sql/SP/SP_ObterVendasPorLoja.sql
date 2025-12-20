-- =============================================
-- SP: ObterVendasPorLoja
-- Descrição: Obtém as vendas filtradas por loja
-- =============================================
CREATE OR ALTER PROCEDURE dbo.ObterVendasPorLoja
    @LojaID INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        V.Id, V.DataHora, V.ValorTotal, V.MetodoPagamento, V.Cliente_Nif, L.Id
    FROM
        dbo.Venda V
    INNER JOIN
        dbo.Loja L ON V.Loja_Id = L.Id
    WHERE
        (@LojaID IS NULL OR V.Loja_Id = @LojaID)
    ORDER BY
        V.Id DESC;
END
GO
