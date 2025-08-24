# Crypto Tracker API

A Django REST API + Vue.js for tracking crypto coins with **price history** updated periodically using Celery and Redis.

---

## **Tech Stack**
- **Python 3.11+**
- **Vue.js (Frontend)**
- **Django 5.2.5**
- **Django REST Framework (DRF)**
- **PostgreSQL**
- **Celery + Redis** (for async tasks)
- **Virtual Environment** for dependency isolation

---

## **Setup Instructions**

### **1️⃣ Clone the repository**
```bash
git clone https://github.com/omiid-ad/crypto_tracker.git
```

### **2️⃣ Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3️⃣ Install dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Setup environment variables**
Create a `.env` file at the root of your project (use `sample.env` as a template):

```env
SECRET_KEY=SOME_SECRET
DEBUG=True
ALLOWED_HOSTS=
DATABASE_NAME=example
DATABASE_USER=root
DATABASE_PASSWORD=1234
DATABASE_HOST=localhost
DATABASE_PORT=5432
REDIS_HOST=redis://localhost:6379
```

### **5️⃣ Setup PostgreSQL by creating a fresh database**


### **6️⃣ Run initial migrations**
```bash
python manage.py migrate
```

### **7️⃣ Create a superuser**
```bash
python manage.py createsuperuser
```

### **8️⃣ Run the development server**
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000** to **explore the Vue.js frontend**

or

Visit: **http://127.0.0.1:8000/admin/** (admin panel)

### **9️⃣ Start Redis and Celery**
**Run Redis server**
```bash
redis-server
```

**Run Celery worker**
```bash
celery -A crypto_tracker worker -l info --pool=solo
```

**Run Celery beat** (for scheduled periodic tasks)
```bash
celery -A crypto_tracker beat -l info
```

### **🔟 Periodic price updates**
The `update_or_create_coins` task runs __**every minute**__ and stores price history.

---

## **API Endpoints**
| Method | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/api/v1/crypto/coins/` | List all coins (paginated) |
| `GET` | `/api/v1/crypto/coins/<id>/` | Retrieve coin by ID |
| `GET` | `/api/v1/crypto/coins/<symbol>/` | Retrieve coin by symbol |
| `GET` | `/api/v1/crypto/coins/<id or symbol>/history/` | Retrieve price history for the last 3 days |

---

### **Example Requests**
**Get all coins**
```bash
curl http://127.0.0.1:8000/api/v1/crypto/coins/
```

**Get coin by ID**
```bash
curl http://127.0.0.1:8000/api/v1/crypto/coins/1/
```

**Get coin by symbol**
```bash
curl http://127.0.0.1:8000/api/v1/crypto/coins/BTC/
```

**Get last 3 days history**
```bash
curl http://127.0.0.1:8000/api/v1/crypto/coins/BTC/history/
```

---

## **License**
Omid Adibfar, Hope Enjoy It ;)
