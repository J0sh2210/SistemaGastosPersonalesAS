class Presupuesto:
    def __init__(self):
        self.gastos = []

    def agregar_gasto(self, descripcion, monto):
        if descripcion.strip() == "":
            return {"error": "Descripción vacía"}
        if monto <= 0:
            return {"error": "Monto inválido"}

        gasto = {
            "descripcion": descripcion,
            "monto": monto
        }
        self.gastos.append(gasto)
        return {"mensaje": "Gasto agregado"}

    def mostrar_gastos(self):
        return self.gastos

    def eliminar_gasto(self, indice):
        if 0 <= indice < len(self.gastos):
            eliminado = self.gastos.pop(indice)
            return eliminado
        return {"error": "Índice no válido"}

    def editar_gasto(self, indice, nueva_desc, nuevo_monto):
        if 0 <= indice < len(self.gastos):
            if nueva_desc.strip() == "":
                return {"error": "Descripción vacía"}
            if nuevo_monto <= 0:
                return {"error": "Monto inválido"}

            self.gastos[indice]["descripcion"] = nueva_desc
            self.gastos[indice]["monto"] = nuevo_monto
            return {"mensaje": "Gasto editado"}

        return {"error": "Índice no válido"}