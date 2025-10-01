import asyncio
from datetime import date, timedelta
from random import choice, randint, uniform
from sqlalchemy import select  # Importamos select para consultas ORM
from sqlalchemy.future import select as select_future # Para AsyncSession

# Asegúrate de que estas importaciones son correctas
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
from api.core.database import engine, Base, get_db

# --- Datos Geográficos ---
PROVINCIAS_CIUDADES = {
    "Buenos Aires": ["La Plata", "Mar del Plata", "Bahía Blanca", "Tandil", "Pilar"],
    "Córdoba": ["Córdoba Capital", "Villa María", "Río Cuarto", "Carlos Paz"],
    "Santa Fe": ["Rosario", "Santa Fe Capital", "Rafaela", "Venado Tuerto"],
    "Mendoza": ["Mendoza Capital", "San Rafael", "Godoy Cruz"],
    "Entre Ríos": ["Paraná", "Concordia", "Gualeguaychú", "Victoria"],
}

# --- Datos para Clientes/Productos Expansión ---
NOMBRES_CLIENTES = ["Juan", "Ana", "Carlos", "María", "Pedro", "Sofía", "Luis", "Elena", "Gabriel", "Laura", "Diego", "Valeria"]
APELLIDOS_CLIENTES = ["Pérez", "Gómez", "Rodríguez", "Fernández", "Díaz", "López", "Martínez", "Sánchez", "Ruiz", "Torres", "Acosta", "Benítez"]
NOMBRES_PROVEEDORES = ["Tech", "Global", "Innovate", "Smart", "Future", "World", "Alpha", "Omega", "Nexus", "Zenith"]
TIPOS_PROVEEDORES = ["S.A.", "Corp.", "Ltda."]

PRODUCTOS_DATA = [
    {"nombre": "Televisor LED 4K", "desc": "Smart TV 55 pulgadas", "cat": "Electrónica", "compra": 500, "venta": 800},
    {"nombre": "Smartphone X", "desc": "Último modelo de teléfono", "cat": "Telefonía", "compra": 300, "venta": 550},
    {"nombre": "Auriculares Bluetooth", "desc": "Cancelación de ruido", "cat": "Electrónica", "compra": 50, "venta": 100},
    {"nombre": "Laptop Ultrabook", "desc": "Ligera y potente", "cat": "Informática", "compra": 900, "venta": 1500},
    {"nombre": "Mouse Gamer", "desc": "Alta precisión", "cat": "Informática", "compra": 20, "venta": 45},
    {"nombre": "Smartwatch V2", "desc": "Monitor de salud", "cat": "Wearables", "compra": 150, "venta": 250},
    {"nombre": "Cámara Digital", "desc": "Compacta con 20MP", "cat": "Fotografía", "compra": 250, "venta": 400},
    {"nombre": "Impresora Multifunción", "desc": "Inyección de tinta", "cat": "Informática", "compra": 70, "venta": 120},
    {"nombre": "Disco Duro Externo 1TB", "desc": "USB 3.0", "cat": "Almacenamiento", "compra": 40, "venta": 80},
    {"nombre": "Parlante Portátil", "desc": "Resistente al agua", "cat": "Audio", "compra": 60, "venta": 110},
    {"nombre": "Tablet Pro 11", "desc": "Para trabajo y ocio", "cat": "Informática", "compra": 450, "venta": 750},
    {"nombre": "E-Reader", "desc": "Pantalla sin reflejo", "cat": "Lectura", "compra": 90, "venta": 180},
]

async def create_all_tables():
    """Crea todas las tablas de la base de datos."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas (o verificadas) correctamente.")


async def get_or_create(db, model, defaults=None, **kwargs):
    """Busca un registro; si no existe, lo crea. Retorna la instancia."""
    
    # 1. Intentar buscar el registro
    stmt = select_future(model).filter_by(**kwargs)
    result = await db.execute(stmt)
    instance = result.scalars().first()
    
    if instance:
        return instance, False # False indica que NO fue creado (ya existía)
    
    # 2. Si no existe, crear el registro
    params = dict(kwargs, **(defaults or {}))
    instance = model(**params)
    db.add(instance)
    await db.flush() # Importante para obtener el ID antes del commit
    return instance, True # True indica que fue creado

async def seed_data():
    """Inserta un gran set de datos de prueba en la base de datos."""
    async for db in get_db():
        try:
            # --- 1. Datos Geográficos ---
            print("1. Insertando (o verificando) País, Provincias y Ciudades...")
            
            # Verificar/Crear País 'Argentina'
            pais, created_pais = await get_or_create(db, Pais, nombre="Argentina")
            print(f"   -> País '{pais.nombre}' (ID: {pais.id}) {'creado' if created_pais else 'verificado'}.")

            todas_ciudades = []
            
            for nombre_provincia, nombres_ciudades in PROVINCIAS_CIUDADES.items():
                
                # Verificar/Crear Provincia
                provincia, created_prov = await get_or_create(
                    db, Provincia, 
                    id_pais=pais.id, 
                    nombre=nombre_provincia
                )
                
                # Crear Ciudades (solo si no existen)
                for nombre_ciudad in nombres_ciudades:
                    ciudad, created_ciudad = await get_or_create(
                        db, Ciudad,
                        id_provincia=provincia.id,
                        nombre=nombre_ciudad
                    )
                    todas_ciudades.append(ciudad)
            
            print(f"   -> {len(PROVINCIAS_CIUDADES)} Provincias y {len(todas_ciudades)} Ciudades verificadas/creadas.")

            
            # Si se crearon nuevas ciudades, asegurarnos de usar la lista completa de IDs
            ciudad_ids = [c.id for c in todas_ciudades]
            if not ciudad_ids:
                 # Si el script se ejecuta en una base de datos pre-seed, debemos cargar los IDs existentes
                 result = await db.execute(select_future(Ciudad))
                 ciudad_ids = [c.id for c in result.scalars().all()]
                 if not ciudad_ids:
                     print("ADVERTENCIA: No se encontraron ciudades. ¡El script no puede continuar!")
                     return


            # --- 2. Datos Base (Clientes, Proveedores, Productos) ---
            
            # 💡 NOTA: Asumimos que Clientes, Proveedores, Productos y sus relaciones
            # NO deben ser verificados y se pueden insertar cada vez que se ejecuta el script.
            # Si quieres evitar duplicados en estas tablas, también deberás usar get_or_create.

            # Clientes (Total: 100)
            print("2. Insertando 100 Clientes...")
            clientes = []
            for _ in range(100):
                nombre_completo = f"{choice(NOMBRES_CLIENTES)} {choice(APELLIDOS_CLIENTES)}"
                cliente = Cliente(
                    nombre=nombre_completo,
                    telefono=f"34{randint(10, 99)}{randint(100000, 999999)}",
                    email=f"{nombre_completo.replace(' ', '.').lower()}{randint(1, 99)}@example.com",
                    direccion=f"Calle Ficticia {randint(1, 9999)}",
                    id_ciudad=choice(ciudad_ids), # Usamos los IDs verificados/creados
                )
                clientes.append(cliente)
            db.add_all(clientes)
            await db.flush()

            # ... [El resto del código para Proveedores, Productos, Sucursales, Depósitos, Stock y Remitos de Venta 
            # sigue igual, asegurándonos de usar los IDs (e.g., choice(ciudad_ids)) donde corresponda] ...

            # Proveedores (Total: 15)
            print("3. Insertando 15 Proveedores...")
            proveedores = []
            for i in range(15):
                proveedor = Proveedor(
                    nombre=f"{choice(NOMBRES_PROVEEDORES)} {choice(TIPOS_PROVEEDORES)} - {i+1}",
                    telefono=f"11{randint(10, 99)}{randint(100000, 999999)}",
                    email=f"contacto.prov{i+1}@proveedor.com",
                    direccion=f"Av. Principal {randint(100, 900)}",
                    id_ciudad=choice(ciudad_ids),
                )
                proveedores.append(proveedor)
            db.add_all(proveedores)
            await db.flush()
            
            # Productos (Total: 12)
            print(f"4. Insertando {len(PRODUCTOS_DATA)} Productos...")
            productos = []
            proveedor_ids = [p.id for p in proveedores]
            for prod_data in PRODUCTOS_DATA:
                producto = Producto(
                    nombre=prod_data["nombre"],
                    descripcion=prod_data["desc"],
                    categoria=prod_data["cat"],
                    precioCompra=prod_data["compra"] * uniform(0.95, 1.05),
                    precioVenta=prod_data["venta"] * uniform(0.95, 1.05),
                    id_proveedor=choice(proveedor_ids),
                )
                productos.append(producto)
            db.add_all(productos)
            await db.flush()


            # --- 3. Sucursales y Depósitos ---
            
            # Sucursales (Total: 5)
            print("5. Insertando 5 Sucursales...")
            
            # Seleccionamos las primeras 5 ciudades creadas/verificadas
            ciudades_para_sucursales = [c for c in todas_ciudades if c.id in ciudad_ids][:5] 
            
            sucursales = []
            for i, ciudad in enumerate(ciudades_para_sucursales):
                sucursal = Sucursal(
                    nombre=f"Sucursal {ciudad.nombre}",
                    telefono=f"34{randint(10, 99)}{randint(100000, 999999)}",
                    email=f"sucursal.{ciudad.nombre.lower().replace(' ', '')}@miempresa.com",
                    direccion=f"Plaza Central {i+1}",
                    id_ciudad=ciudad.id,
                )
                sucursales.append(sucursal)
            db.add_all(sucursales)
            await db.flush()

            # Depósitos (Total: 3)
            print("6. Insertando 3 Depósitos...")
            ciudades_para_depositos = [c for c in todas_ciudades if c.id in ciudad_ids][:3] # Las primeras 3 ciudades
            depositos = []
            for i, ciudad in enumerate(ciudades_para_depositos):
                deposito = Deposito(
                    nombre=f"Depósito Principal {ciudad.nombre}",
                    telefono=f"34{randint(10, 99)}{randint(100000, 999999)}",
                    email=f"deposito.{ciudad.nombre.lower().replace(' ', '')}@miempresa.com",
                    direccion=f"Zona Industrial {i+1}",
                    id_ciudad=ciudad.id,
                )
                depositos.append(deposito)
            db.add_all(depositos)
            await db.flush()


            # --- 4. Stock ---
            
            # Stock para todos los Productos en todas las Sucursales
            print("7. Insertando Stock (Total: 60 registros)...")
            stocks = []
            producto_ids = [p.id for p in productos]
            sucursal_ids = [s.id for s in sucursales]
            deposito_ids = [d.id for d in depositos]
            
            for producto_id in producto_ids:
                for sucursal_id in sucursal_ids:
                    stock_reg = Stock(
                        cantidad_sucursal=randint(10, 50),
                        cantidad_deposito=randint(50, 200),
                        id_deposito=choice(deposito_ids),
                        id_sucursal=sucursal_id,
                        id_producto=producto_id,
                    )
                    stocks.append(stock_reg)
            db.add_all(stocks)
            await db.flush()


            # --- 5. Remitos de Venta (Transacciones) ---
            
            # 500 Remitos de Venta distribuidos en un rango de 180 días
            print("8. Insertando 500 Remitos de Venta (distribuidos en 6 meses)...")
            remitos = []
            hoy = date.today()
            dias_atras = 180
            cliente_ids = [c.id for c in clientes]

            for _ in range(500):
                # Fecha aleatoria en el rango de los últimos 6 meses
                fecha_venta = hoy - timedelta(days=randint(0, dias_atras))

                remito = RemitoVenta(
                    fecha=fecha_venta,
                    cantidad=randint(1, 5),
                    id_cliente=choice(cliente_ids),
                    id_producto=choice(producto_ids),
                    id_sucursal=choice(sucursal_ids),
                )
                remitos.append(remito)
            
            db.add_all(remitos)
            await db.commit()
            print("   -> Inserción de todos los datos completada con éxito. (Total: 500 Remitos).")

        except Exception as e:
            await db.rollback()
            print(f"Error crítico al insertar datos. Haciendo rollback: {e}")
            raise
        finally:
            await db.close()

if __name__ == "__main__":
    asyncio.run(seed_data())