# HTTP Response Registry 🐕

> A visual tool for exploring, filtering, and curating HTTP response codes using the http.dog API.

![Project Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.x-blue)
![Flask](https://img.shields.io/badge/flask-2.x-lightgrey)


## 📖 Overview

**HTTP Response Registry** is a full-stack web application designed to help developers and learners visualize HTTP status codes through memorable imagery. By leveraging the `http.dog` API, this application turns dry technical error codes into an interactive and visual experience.

The core technical challenge of this project was implementing a custom **regex-style filtering engine** that allows users to query response codes using wildcard patterns (e.g., `2xx`, `20x`) and persist these custom collections to their user profile with full CRUD capabilities.



## ✨ Key Features

### 🔐 Secure Authentication
* **User Isolation:** Each user has a private dashboard; data is not shared between accounts.
* **Session Management:** Secure login and signup flows using session-based authentication (or JWT).

### 🔍 Advanced Pattern Filtering
I implemented a flexible search algorithm that supports `x` as a wildcard digit, allowing for granular filtering of response codes.

| Filter Input | Result | Logic |
| :--- | :--- | :--- |
| **203** | Single Code | Matches exact code 203. |
| **2xx** | Broad Class | Matches all codes starting with 2 (Success). |
| **20x** | Sub-Class | Matches codes starting with 20 (200-209). |
| **3xx** | Broad Class | Matches all codes starting with 3 (Redirection). |

### 📂 List Management (CRUD)
* **Save:** Persist filtered results as named lists with timestamps.
* **Edit:** Add or remove specific codes from existing lists.
* **Delete:** Permanently remove lists from the database.
* **Visualize:** View the gallery of dog images associated with any saved list.

## 🛠️ Tech Stack

**Backend:**
* **Framework:** Flask (Python)
* **ORM:** SQLAlchemy

**Frontend:**
* HTML5, CSS3, JavaScript
* Jinja2 Templating

**Database:**
* SQLite (Development) / PostgreSQL (Production)

**External API:**
* [HTTP Dog](https://http.dog/) - Source for status code imagery.

## 🗄️ Database Schema

The application uses a relational database model designed for efficiency and data integrity.

* **Users Table:** Stores authentication data (`id`, `username`, `email`, `password_hash`).
* **Lists Table:** Stores metadata for user collections (`id`, `user_id`, `list_name`, `created_at`).
* **ResponseCodes Table:** Links specific codes to lists (`id`, `list_id`, `status_code`, `image_url`).

## ⚡ Complexity Analysis

One of the goals of this project was to ensure operations remain performant even as user data grows.

* **User Login/Signup:** `O(1)` - Average case using indexed user lookups.
* **Filtering Logic:** `O(n)` - Where *n* is the total number of HTTP codes. The wildcard matching iterates through the predefined set of codes to check for pattern matches.
* **Saving Lists:** `O(k)` - Where *k* is the number of codes in the current filter.
* **Fetching Lists:** `O(m)` - Where *m* is the count of lists owned by the user.

## 🚀 Getting Started

To run this project locally, follow these steps:

### Prerequisites
* Python 3.x
* pip

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/http-response-registry.git
    cd http-response-registry
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Initialize the Database**
    ```bash
    flask db upgrade
    # or python init_db.py (depending on your setup)
    ```

5.  **Run the application**
    ```bash
    flask run
    ```
