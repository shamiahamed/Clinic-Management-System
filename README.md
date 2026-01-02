FastAPI Clinic Management System

A scalable and production-ready Clinic Management System API built using FastAPI and Async SQLAlchemy, following industry-standard backend best practices and a clean layered architecture.

This system manages clinics, doctors, patients, and appointments, providing a secure and efficient backend for real-world healthcare applications.


✨ Key Features
Authentication & Authorization
User registration and login
JWT-based authentication

Role-Based Access Control (Admin / Doctor / Staff)


🏥 Clinic Management

Create and manage clinics

Assign doctors to clinics

Maintain clinic details and status


👨‍⚕️ Doctor Management

Doctor profile creation and updates

Specialization & availability management

Doctor–clinic association


🧑‍🤝‍🧑 Patient Management

Patient registration and profile management

Secure storage of patient information

Patient history tracking (extendable)


📅 Appointment Management

Book, update, cancel, and view appointments

Doctor-wise and patient-wise scheduling

Appointment status handling (Scheduled / Completed / Cancelled)


🛠 Architecture & Code Quality

Clean layered architecture
Router → Controller → Service → Repository
Custom exception handling
Middleware for logging & standardized API responses


🗄 Database Support
Async SQLAlchemy ORM
Supports MySQL and PostgreSQL
Designed for easy schema extension


📈 Production Ready
Modular, scalable, and maintainable codebase
Designed for real-world clinic workflows
Easy to extend with billing, reports, and notifications
