# 🛠️ Taller Mecánico API (taller_api)

¡Bienvenido al backend del Sistema de Gestión para Taller Mecánico! Esta es una API REST robusta y modular desarrollada con **Django** y **Django Rest Framework (DRF)**, utilizando **PostgreSQL** como base de datos relacional y **SimpleJWT** para la autenticación segura mediante JSON Web Tokens.

---

## 👥 Integrantes
* **[Jonathan Torres]** - Desarrollo Backend e Infraestructura
* **[Franciso Soliz]** - [Aporte en el despliegue en vps]

---

## 📝 Descripción del Sistema
El sistema automatiza todo el flujo operativo y financiero de un taller mecánico automotriz moderno. Está dividido estratégicamente en 4 módulos integrados:
* **Módulo 1 (Catálogos Base):** Control de clientes, proveedores, métodos de pago, servicios base, especialidades de mecánicos y roles del sistema.
* **Módulo 2 (Personal y Modelos):** Registro de mecánicos, gestión de stock de repuestos, perfiles de usuarios y parametrización de vehículos por marca y modelo.
* **Módulo 3 (Operaciones):** Gestión de vehículos vinculados a clientes, flujo de citas web y apertura de Órdenes de Reparación.
* **Módulo 4 (Finanzas):** Liquidación de mano de obra (servicios) y repuestos asignados a órdenes, generación automática de facturas y pasarela de registros de pago con cálculo automático de saldos.

---

## 🚀 Instalación y Configuración Local

Sigue estos pasos para levantar el entorno de desarrollo en tu máquina local:

### 1. Clonación del repositorio
```bash
git clone [Roman2018122]/[https://github.com/Roman2018122/Taller_mecanico_api.git].git
cd torres_taller_api