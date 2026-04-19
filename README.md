# LocalNecessaryServiceHub 🛠️

**LocalNecessaryServiceHub** is a digital platform designed to bridge the gap between local service providers and residents. It serves as a centralized directory where users can find essential services such as plumbing, electrical work, computer repairs, and more, within their immediate vicinity.

---

## 🛠️ Tech Stack

* **Backend:** Python with **Flask** (RESTful API design)
* **Database:** **MongoDB** (for flexible service provider listings and user data)
* **Frontend:** HTML5, CSS3, and JavaScript (Bootstrap for responsive UI)
* **Authentication:** JWT (JSON Web Tokens) for secure user and provider logins
* **Environment:** `python-dotenv` for managing sensitive configurations

---

## ✨ Key Features

* **Service Categorization:** Browse services by category (e.g., Home Maintenance, Technical Support, Health).
* **Provider Listings:** Detailed profiles for local experts, including contact info and service descriptions.
* **Search & Filter:** Find exactly what you need based on location and service type.
* **User/Provider Dashboard:** Separate interfaces for users to book services and providers to manage their listings.
* **Real-time Availability:** Status indicators to show if a service provider is currently active.

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10+
* MongoDB (local instance or MongoDB Atlas)

### 2. Installation
Clone the repository:
```bash
git clone https://github.com/Sundaraj0828/localNecessaryServiceHub.git
cd localNecessaryServiceHub
```

### 3. Environment Configuration
Create a `.env` file in the project root:
```env
MONGO_URI=mongodb://localhost:27017/servicehub_db
SECRET_KEY=your_secure_secret_key
FLASK_APP=app.py
FLASK_ENV=development
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Launch the Application
```bash
flask run
```
Access the hub at `http://127.0.0.1:5000/`.

---

## 📁 Project Structure
```text
├── app/
│   ├── routes/          # API endpoints for services and users
│   ├── models/          # MongoDB data structures
│   ├── static/          # CSS, Images, and Client-side JS
│   └── templates/       # HTML views
├── .env                 # Environment variables
├── app.py               # Main entry point
├── requirements.txt     # Python packages
└── README.md            # Documentation
```

---

## 🔗 Core API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/services` | Retrieve all available service categories |
| **GET** | `/api/providers` | Search for providers based on location/service |
| **POST** | `/api/register` | User or Provider registration |
| **PUT** | `/api/profile` | Update provider service details |

---

## 📄 License
Distributed under the MIT License.

---

**Developed with ❤️ by [L.C.Sundaraj](https://github.com/Sundaraj0828)**
