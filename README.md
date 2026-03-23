# Vitable Medical Scheduling System

A robust medical scheduling system built using Django, PostgreSQL, HTMX, Tailwind CSS, and Docker. This project uses a custom Admin-driven interface featuring a slick calendar dashboard to seamlessly manage Doctors, Patients, Availabilities, and Appointments without the need for a complex frontend SPA like React or Vue.

## Features
- **Admin-Driven Workflow:** All scheduling is managed smoothly from within the Django Admin ecosystem.
- **Custom Calendar Dashboard:** A highly interactive custom Django Admin index that replaces the standard app list with a responsive monthly grid.
- **HTMX Dynamic Forms:** View and create new appointments via a slide-over modal directly from the calendar, ensuring a modern UX without any full-page reloads.
- **Overbooking Prevention:** Strict validations inside the core Django models prevent scheduling overlapping overlapping hours or violations against a doctor's weekly shift availability.
- **Dynamic Slot Generation:** Selecting a Doctor instantly fetches available 30-minute time slots natively computed against existing schedules.

---

## 🚀 Quickstart Guide

### 1. Requirements
Ensure you have the following installed on your system:
- **Docker**
- **Docker Compose**

### 2. Bootstrapping the Environment
Navigate to the infrastructure directory and spin up the containers:
```bash
cd infra
docker-compose up -d
```
*(The `-d` flag runs the containers in detached mode. Remove it if you want to see the live server logs in your terminal).*

### 3. Database Setup
Once the containers are running securely, apply the schema migrations to PostgreSQL:
```bash
docker-compose exec backend python manage.py migrate
```

### 4. Create an Administrator Account
You need an admin account to access the calendar dashboard:
```bash
docker-compose exec backend python manage.py createsuperuser
```
*(Follow the interactive prompts in the terminal to set your username and password).*

### 5. Access the Platform
Open your browser and navigate to:
**[http://localhost:8000/admin/](http://localhost:8000/admin/)**

---

## 📅 Usage Instructions

1. **Register Doctors & Working Hours:**
   - Navigate to the **Doctors** module via the left sidebar and add a new professional.
   - Go to the **Availabilities** module and assign weekly working days (e.g., Monday 09:00 to 17:00) to that specific doctor. *Appointments cannot be booked outside these shifts!*

2. **Register Patients:**
   - Add your patients inside the **Patients** module.

3. **Schedule Appointments via Calendar:**
   - Return to the main Dashboard (by clicking the header logo).
   - Click on any active day on the Calendar matrix.
   - A modern **HTMX Slide-Over Form** will appear dynamically.
   - Choose a doctor and date—the system instantly queries the database to serve valid open slots.
   - Select a Time Slot (this fully automates the required `start_time` and `end_time` logic natively).
   - Submit the exact form. The appointment drops directly onto the calendar instantly.

---

## 🛠 Useful Developer Commands

- **View Live Backend Logs**:
  ```bash
  docker-compose logs -f backend
  ```
- **Drop into a Django Shell**:
  ```bash
  docker-compose exec backend python manage.py shell
  ```
- **Stop Containers**:
  ```bash
  docker-compose down
  ```
- **Rebuild Images** *(after modifying `requirements.txt` or `Dockerfile`)*:
  ```bash
  docker-compose up --build
  ```
