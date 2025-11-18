# TalentMatch - Job Matching Platform

## Project Overview
TalentMatch is a Django-based web application for job matching and recruitment. It's a talent management platform connecting candidates with companies through job postings, applications, and AI-assisted features.

## Project Structure
- **Django Version**: 5.2.8
- **Python Version**: 3.11
- **Database**: SQLite (development)
- **Language**: Portuguese (pt-br)

## Core Features
- **Landing Page**: Public-facing homepage
- **User Dashboards**: Separate dashboards for candidates, companies, and administrators
- **Job Management**: Browse, search, and apply for job postings
- **Company Area**: Post and manage job vacancies
- **Admin Panel**: User, company, and job management with reporting
- **Messaging**: Internal messaging system and AI chat
- **Courses**: Training and course management with progress tracking
- **Authentication**: Login/logout with role-based access

## Project Architecture

### Applications
- `core`: Main application containing all views, URLs, and templates
- `talentmatch_project`: Django project settings and configuration

### Key Directories
- `templates/`: HTML templates for all pages
- `static/css/`: Stylesheets
- `core/`: Main app with models, views, and URLs
- `talentmatch_project/`: Project configuration

### Database
Currently using SQLite for development. The database is already initialized with migrations applied.

## Configuration

### Development
- Server runs on `0.0.0.0:5000`
- Debug mode enabled
- ALLOWED_HOSTS set to accept all hosts (for Replit proxy)
- CSRF trusted origins configured for Replit domains

### Deployment
- Uses Gunicorn WSGI server
- Configured for autoscale deployment
- Production-ready settings in place

## Running Locally
The Django development server is configured to run automatically via the workflow:
```bash
python manage.py runserver 0.0.0.0:5000
```

## Dependencies
- django==5.2.8
- gunicorn==23.0.0
- asgiref==3.10.0
- sqlparse==0.5.3

## Recent Changes
- **2025-11-18**: Initial project import and Replit environment setup
  - Installed Python 3.11 and Django
  - Configured settings for Replit environment (ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS)
  - Created workflow for development server on port 5000
  - Configured deployment with Gunicorn
  - Applied database migrations
  - Fixed CSS loading: Added {% load static %} and CSS links to all templates
  - Created .gitignore file for Python/Django projects
