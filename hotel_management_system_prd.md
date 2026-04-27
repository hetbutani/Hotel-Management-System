# Product Requirements Document: Hotel Management System

## Project Overview
A comprehensive full-stack hotel management platform for Admins, Staff, and Guests.

## User Roles & Key Features

### 1. Guest (Customer)
*   **Landing Page:** Hero section, room showcase, testimonials, and booking CTAs.
*   **Auth:** Login/Signup with role selection.
*   **Booking:** Search/filter rooms, real-time availability, and booking forms.
*   **Customer Panel:** Booking history, profile management, and cancellation.
*   **Payment:** Simulated payment tracking.

### 2. Staff
*   **Dashboard:** Overview of stats (Occupancy, incoming bookings).
*   **Room Management:** Update status, view availability.
*   **Booking Management:** Check-in/check-out processing.

### 3. Admin
*   **Advanced Dashboard:** Analytics charts (Revenue, growth).
*   **User Management:** Control staff and customer accounts.
*   **System Config:** Full CRUD for rooms and pricing.
*   **Reports:** Daily/Monthly revenue and booking statistics.

## Tech Stack
*   **Frontend:** React.js, Tailwind CSS, Lucide Icons, Chart.js.
*   **Backend:** Node.js, Express.js, JWT, Bcrypt.
*   **Database:** MongoDB (Mongoose).

## Design Direction
*   **Aesthetic:** Clean, modern SaaS-style dashboard.
*   **Layout:** Sidebar navigation, card-based stats, data tables, and modals.
*   **Features:** Light/Dark mode support, smooth transitions.

## Data Models
*   **User:** Name, email, password, role.
*   **Room:** Number, type, price, status, description, images.
*   **Booking:** UserID, RoomID, check-in/out dates, status.
*   **Payment:** BookingID, amount, status.
