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
- **Intelligent Matching**: Algorithm-based candidate-job matching with scoring (40% skills, 30% location, 20% experience, 10% salary)

## Project Architecture

### Applications
- `core`: Main application containing all views, URLs, and templates
- `talentmatch_project`: Django project settings and configuration

### Key Directories
- `templates/`: HTML templates for all pages
- `static/css/`: Stylesheets
- `core/`: Main app with models, views, URLs, and matching algorithm
  - `models.py`: Database models
  - `views.py`: View functions and API endpoints
  - `matching.py`: Intelligent matching algorithm
  - `admin.py`: Django admin configuration
  - `urls.py`: URL routing
- `talentmatch_project/`: Project configuration

### Database Models
Currently using SQLite for development. The database includes:
- **Candidato**: Candidate profiles with skills, experience, location, and salary expectations
- **Empresa**: Company profiles with sector, location, and description
- **Vaga**: Job postings with required skills, salary range, location, and type (remote/hybrid/on-site)
- **Match**: Candidate-job matches with compatibility scores (0-100)
- **Mensagem**: Internal messaging system
- **Curso**: Training courses catalog
- **ProgressoCurso**: Course progress tracking for candidates

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

## Matching API Endpoints
The platform provides REST API endpoints for matching:
- `GET /api/matches/candidato/<id>/` - Generate and retrieve matches for a candidate
- `GET /api/matches/vaga/<id>/` - Generate and retrieve matches for a job posting
- `POST /api/vaga/<id>/aplicar/` - Apply to a job posting
- `GET /api/meus-matches/` - Get matches for logged-in candidate

### Matching Algorithm
The matching score (0-100) is calculated based on:
- **Skills Match (40%)**: Percentage of required skills that candidate possesses
- **Location Match (30%)**: Same city (30pts), same state (15pts), remote (30pts)
- **Experience Match (20%)**: Years of experience vs. minimum required
- **Salary Match (10%)**: Alignment between candidate expectation and job offer

## Recent Changes
- **2025-11-18**: Initial project import and Replit environment setup
  - Installed Python 3.11 and Django
  - Configured settings for Replit environment (ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS)
  - Created workflow for development server on port 5000
  - Configured deployment with Gunicorn
  - Applied database migrations
  - Fixed CSS loading: Added {% load static %} and CSS links to all templates
  - Created .gitignore file for Python/Django projects
  - Fixed navigation redirects:
    - Updated cadastro view to redirect to dashboard_candidato after submission
    - Updated cadastro_empresa view to redirect to dashboard_empresa after submission
    - Updated login_view to redirect to dashboard_candidato after login
    - Fixed all landing page links to use proper Django URL tags
    - Corrected all navigation links throughout the application

- **2025-11-18**: Database and Matching System Implementation
  - Created complete database schema with 7 models (Candidato, Empresa, Vaga, Match, Mensagem, Curso, ProgressoCurso)
  - Implemented intelligent matching algorithm in `core/matching.py`
  - Created 4 API endpoints for matching functionality
  - Updated views to save candidate and company registrations to database
  - Registered all models in Django admin panel
  - Fixed bug in skills scoring to filter empty strings correctly
  - Tested matching with sample data showing accurate score calculations
