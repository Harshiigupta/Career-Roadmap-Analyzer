

## Summary
Single Django project that provides:
- Frontend (Django templates) for user input and dashboard
- Backend APIs:
  - `POST /api/skill-gap/` — returns matched & missing skills, recommendations, suggested order
  - `POST /api/roadmap/` — returns a 3-phase roadmap for the chosen role
  - `GET  /api/news/` — returns top 5 HackerNews stories (title, url, score, time, type, by)

Data source for role skills: `careerapp/skills.json` (predefined).

## Tech stack
- Python + Django
- requests (for HackerNews fetch)
- No database required (optional JSON file storage `submissions.json` used to save inputs)

## Setup (local)
1. Ensure Python is installed (3.8+ recommended).
2. (Optional) create and activate a virtual environment.
3. Install requirements:

