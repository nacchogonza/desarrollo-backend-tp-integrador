import asyncio
from datetime import date

# Asegúrate de que estas importaciones son correctas según la estructura de tu proyecto
# Si tus modelos están en api.models, entonces:
from api.core.models import (
    Pais,
    Provincia,
    Ciudad,
    Cliente,
    Proveedor,
    Producto,
    Sucursal,
    Deposito,
    RemitoVenta,
    Stock,
)

# Si tu función get_db está en api.core.database, entonces:
from api.core.database import engine, Base, get_db


async def create_all_tables():
    """Crea todas las tablas de la base de datos."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas (o verificadas) correctamente.")


async def seed_data():
    """Inserta datos de prueba en la base de datos."""
    async for db in get_db():  # Obtiene una sesión de base de datos
        try:
            # --- Inserción de Datos Geográficos ---
            print("Insertando datos geográficos...")
            pais = Pais(nombre="Argentina")
            db.add(pais)
            await db.flush()  # Para obtener el ID del país antes del commit

            provincia = Provincia(nombre="Entre Ríos", id_pais=pais.id)
            db.add(provincia)
            await db.flush()

            ciudad = Ciudad(nombre="Victoria", id_provincia=provincia.id)
            db.add(ciudad)
            await db.flush()
            print(
                f"País '{pais.nombre}' (ID: {pais.id}), Provincia '{provincia.nombre}' (ID: {provincia.id}), Ciudad '{ciudad.nombre}' (ID: {ciudad.id}) creados."
            )

            ciudad2 = Ciudad(nombre="Parana", id_provincia=provincia.id)
            db.add(ciudad2)
            await db.flush()
            print(
                f"País '{pais.nombre}' (ID: {pais.id}), Provincia '{provincia.nombre}' (ID: {provincia.id}), Ciudad '{ciudad2.nombre}' (ID: {ciudad2.id}) creados."
            )

            # --- Inserción de Otros Datos Base ---
            print(
                "Insertando datos de Cliente, Proveedor, Producto, Sucursal, Depósito..."
            )
            cliente1 = Cliente(
                nombre="Juan Pérez",
                telefono="3434112233",
                email="juan.perez@example.com",
                direccion="Av. San Martín 123",
                id_ciudad=ciudad.id,
            )
            cliente2 = Cliente(
                nombre="Ana Gómez",
                telefono="3434445566",
                email="ana.gomez@example.com",
                direccion="Calle Falsa 45",
                id_ciudad=ciudad.id,
            )
            db.add_all([cliente1, cliente2])
            await db.flush()
            print(
                f"Clientes '{cliente1.nombre}' (ID: {cliente1.id}), '{cliente2.nombre}' (ID: {cliente2.id}) creados."
            )

            proveedor = Proveedor(
                nombre="Tech S.A.",
                telefono="1122334455",
                email="contacto@techsa.com",
                direccion="Calle Falsa 456",
                id_ciudad=ciudad.id,
            )
            db.add(proveedor)
            await db.flush()
            print(f"Proveedor '{proveedor.nombre}' (ID: {proveedor.id}) creado.")

            producto1 = Producto(
                nombre="Televisor LED 4K",
                descripcion="Smart TV de 55 pulgadas",
                categoria="Electrónica",
                precioCompra=500.00,
                precioVenta=800.00,
                id_proveedor=proveedor.id,
            )
            producto2 = Producto(
                nombre="Smartphone X",
                descripcion="Último modelo de teléfono",
                categoria="Telefonía",
                precioCompra=300.00,
                precioVenta=550.00,
                id_proveedor=proveedor.id,
            )
            db.add_all([producto1, producto2])
            await db.flush()
            print(
                f"Productos '{producto1.nombre}' (ID: {producto1.id}), '{producto2.nombre}' (ID: {producto2.id}) creados."
            )

            sucursal = Sucursal(
                nombre="Sucursal Centro",
                telefono="3434667788",
                email="centro@miempresa.com",
                direccion="Calle Principal 789",
                id_ciudad=ciudad.id,
            )
            db.add(sucursal)
            await db.flush()
            print(f"Sucursal '{sucursal.nombre}' (ID: {sucursal.id}) creada.")

            stock1 = Deposito(
                nombre="Depósito Principal",
                telefono="3434990011",
                email="deposito@miempresa.com",
                direccion="Ruta 12 Km 5",
                id_ciudad=ciudad.id,
            )
            db.add(stock1)
            await db.flush()
            print(f"Depósito '{stock1.nombre}' (ID: {stock1.id}) creado.")

            stock1 = Stock(
                cantidad_sucursal=100,
                cantidad_deposito=200,
                id_deposito=1,
                id_sucursal=1,
                id_producto=1,
            )
            db.add(stock1)
            await db.flush()
            print(f"Stock (ID: {stock1.id}) creado.")

            stock2 = Stock(
                cantidad_sucursal=300,
                cantidad_deposito=600,
                id_deposito=1,
                id_sucursal=1,
                id_producto=2,
            )
            db.add(stock2)
            await db.flush()
            print(f"Stock (ID: {stock2.id}) creado.")

            # --- Inserción de Remitos de Venta (para el reporte) ---
            print("Insertando remitos de venta...")
            remitos = [
                RemitoVenta(
                    fecha=date(2025, 1, 15),
                    cantidad=1,
                    id_cliente=cliente1.id,
                    id_producto=producto1.id,
                    id_sucursal=sucursal.id,
                ),
                RemitoVenta(
                    fecha=date(2025, 2, 20),
                    cantidad=2,
                    id_cliente=cliente1.id,
                    id_producto=producto2.id,
                    id_sucursal=sucursal.id,
                ),
                RemitoVenta(
                    fecha=date(2025, 3, 5),
                    cantidad=3,
                    id_cliente=cliente2.id,
                    id_producto=producto1.id,
                    id_sucursal=sucursal.id,
                ),
                RemitoVenta(
                    fecha=date(2025, 3, 10),
                    cantidad=1,
                    id_cliente=cliente2.id,
                    id_producto=producto2.id,
                    id_sucursal=sucursal.id,
                ),
                RemitoVenta(
                    fecha=date(2025, 4, 1),
                    cantidad=2,
                    id_cliente=cliente1.id,
                    id_producto=producto1.id,
                    id_sucursal=sucursal.id,
                ),
                RemitoVenta(
                    fecha=date(2025, 5, 12),
                    cantidad=1,
                    id_cliente=cliente2.id,
                    id_producto=producto2.id,
                    id_sucursal=sucursal.id,
                ),
                RemitoVenta(
                    fecha=date(2025, 6, 27),
                    cantidad=4,
                    id_cliente=cliente1.id,
                    id_producto=producto1.id,
                    id_sucursal=sucursal.id,
                ),  # Hoy
                RemitoVenta(
                    fecha=date(2025, 6, 27),
                    cantidad=1,
                    id_cliente=cliente2.id,
                    id_producto=producto1.id,
                    id_sucursal=sucursal.id,
                ),  # Hoy
            ]
            db.add_all(remitos)
            await db.commit()  # Commit final para guardar todos los cambios pendientes
            print("Remitos de venta insertados.")

        except Exception as e:
            await db.rollback()  # Si algo falla, revierte todos los cambios
            print(f"Error al insertar datos: {e}")
        finally:
            await db.close()  # Cierra la sesión


if __name__ == "__main__":
    asyncio.run(seed_data())
