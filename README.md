# Alke Wallet 💳

Aplicación web de gestión de wallet digital desarrollada con Django para **Alke Financial**, una fintech ficticia. Permite a los usuarios registrarse, administrar su saldo y registrar transacciones financieras desde el navegador.

---

## Tecnologías

- **Backend:** Python 3.12 + Django 6.0
- **Base de datos:** SQLite3
- **Frontend:** Bootstrap 5 + Bootstrap Icons
- **Autenticación:** Django Auth (sesiones, hashing PBKDF2-SHA256)
- **Variables de entorno:** python-dotenv

---

## Funcionalidades

- Registro de usuario con creación automática de wallet
- Login y logout con sistema de sesiones de Django
- Dashboard con saldo actualizado en tiempo real
- Historial de transacciones con filtros por tipo y fecha
- Creación de transacciones (depósito, retiro, transferencia)
- Detalle de transacción
- Eliminación de transacciones con pantalla de confirmación
- Transacciones inmutables (no editables) por principio de auditoría
- Saldo recalculado automáticamente via señales Django

---

## Modelo de datos

```
User (django.contrib.auth)
 │
 │ OneToOneField (CASCADE)
 ▼
Wallet
 ├── balance: DecimalField
 ├── currency: CharField (USD / EUR / CLP)
 └── created_at: DateTimeField
 │
 │ ForeignKey (CASCADE)
 ▼
Transaction
 ├── amount: DecimalField
 ├── transaction_type: CharField (deposit / withdrawal / transfer)
 ├── description: CharField (opcional)
 └── created_at: DateTimeField
```

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/alkewallet.git
cd alkewallet
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install django python-dotenv
```

### 4. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto (junto a `manage.py`):

```env
SECRET_KEY=tu_secret_key_aqui
DEBUG=True
```

Para generar una `SECRET_KEY` nueva:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Aplicar migraciones

```bash
python manage.py migrate
```

### 6. Levantar el servidor

```bash
python manage.py runserver
```

Visita `http://127.0.0.1:8000/` en el navegador.

---

## Estructura del proyecto

```
alkewallet/
├── config/                  # Configuración global del proyecto
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── wallet/                  # App principal
│   ├── migrations/
│   ├── templates/wallet/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── transaction_list.html
│   │   ├── transaction_detail.html
│   │   ├── transaction_form.html
│   │   └── transaction_confirm_delete.html
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── signals.py
│   └── urls.py
├── manage.py
├── db.sqlite3
├── .env                     # No incluido en el repositorio
├── .gitignore
└── README.md
```

---

## Decisiones técnicas

**`DecimalField` sobre `FloatField`**
Los floats tienen errores de precisión binaria inaceptables en sistemas financieros. `DecimalField` garantiza precisión decimal exacta.

**`OneToOneField` entre User y Wallet**
Garantiza a nivel de base de datos que cada usuario tiene exactamente una wallet.

**Transacciones inmutables**
Las transacciones no pueden editarse una vez creadas. Para corregir un error se elimina y se crea una nueva. Principio estándar de auditoría financiera.

**Señales Django para recalcular saldo**
El balance se recalcula automáticamente via `post_save` y `post_delete` cada vez que se crea o elimina una transacción, sin lógica manual en las vistas.

**`select_related` para evitar N+1**
Las vistas usan `select_related('wallet')` para traer transacciones y wallet en un solo JOIN SQL.

---

## Mejoras futuras

- Modelo `Contact` para gestionar destinatarios de transferencias
- Modelo `Transfer` con `wallet_origin` y `wallet_destination`
- Paginación en el historial de transacciones
- Exportación del historial a CSV
- Soporte para múltiples monedas con conversión

---

## Autor

Desarrollado por **NiConBravo** como proyecto del Módulo 7 — Bootcamp de Programación.
