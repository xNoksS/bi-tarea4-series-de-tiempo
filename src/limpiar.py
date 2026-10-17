import pandas as pd

# StockCode que NO son productos (cobros, envíos, ajustes y comisiones).
NO_PRODUCTO = {
    "POST", "DOT", "C2",                   # envíos / carriage / postage
    "M",                                   # ajustes manuales
    "D",                                   # descuentos
    "S",                                   # muestras
    "BANK CHARGES", "AMAZONFEE", "CRUK",   # cargos y comisiones
    "B",                                   # ajuste de deuda incobrable
}


def _ventas_anuladas_manualmente(x):
    """Ventas que una cancelación manual ('M') anuló: mismo cliente, mismo día
    y mismo monto. La regla de códigos no producto elimina la cancelación 'M';
    sin esta regla quedaría la venta 'huérfana' inflando la serie diaria."""
    cm = x[(x["StockCode"] == "M")
           & x["InvoiceNo"].str.startswith("C")
           & x["CustomerID"].notna()]
    llaves = pd.MultiIndex.from_arrays(
        [cm["CustomerID"], cm["InvoiceDate"].dt.normalize(), (-cm["monto"]).round(2)])
    idx = pd.MultiIndex.from_arrays(
        [x["CustomerID"], x["InvoiceDate"].dt.normalize(), x["monto"].round(2)])
    return (pd.Series(idx.isin(llaves), index=x.index)
            & (x["monto"] > 0)
            & (x["StockCode"] != "M")
            & ~x["InvoiceNo"].str.startswith("C"))


def limpiar(df, devolver_bitacora=False):
    """Limpia Online Retail y devuelve un DataFrame.

    Conserva las filas sin CustomerID (sirven para la serie de ventas; la
    Parte 6 las excluye por su cuenta). Las cancelaciones ('C') se conservan
    porque su cantidad negativa ya resta de las ventas del día.

    Si devolver_bitacora=True, devuelve (df_limpio, bitacora), con una fila
    por regla en el orden en que se aplicaron.
    """
    d = df.copy()
    d["monto"] = d["Quantity"] * d["UnitPrice"]

    # Cada regla devuelve la máscara de filas que SE ELIMINAN.
    # El orden importa: cada regla cuenta solo lo que elimina en ese momento.
    reglas = [
        ("a) duplicados exactos",
         lambda x: x.duplicated()),
        ("b) factura con prefijo A (ajuste contable)",
         lambda x: x["InvoiceNo"].str.startswith("A")),
        ("c) venta anulada por cancelación manual (M)",
         _ventas_anuladas_manualmente),
        ("d) StockCode que no es producto",
         lambda x: x["StockCode"].isin(NO_PRODUCTO)),
        ("e) precio <= 0",
         lambda x: x["UnitPrice"] <= 0),
        ("f) cantidad negativa sin 'C'",
         lambda x: (x["Quantity"] < 0) & ~x["InvoiceNo"].str.startswith("C")),
    ]

    filas = []
    for nombre, regla in reglas:
        mask = regla(d)
        filas.append({
            "regla": nombre,
            "filas_eliminadas": int(mask.sum()),
            "monto_gbp": float(d.loc[mask, "monto"].sum()),
        })
        d = d[~mask]

    limpio = d.drop(columns="monto").reset_index(drop=True)
    if devolver_bitacora:
        return limpio, pd.DataFrame(filas)
    return limpio
