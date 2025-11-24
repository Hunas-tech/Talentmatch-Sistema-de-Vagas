# TalentMatch - Plataforma Inteligente de Matching de Vagas

## Overview
TalentMatch is a comprehensive Django web platform designed for intelligent matching between job candidates and vacancies. The system leverages compatibility algorithms, AI for career guidance, and provides an intuitive, interactive interface for candidates, companies, and administrators. Its core purpose is to connect talent with opportunities efficiently, aiming to be a leading solution in the job market by offering personalized experiences and advanced matching capabilities.

## User Preferences
- **Coding Style**: I prefer a clean, readable, and well-commented codebase. Follow Python's PEP 8 guidelines.
- **Workflow**: I prefer an iterative development approach, focusing on delivering functional components incrementally. Please break down complex tasks into smaller, manageable steps.
- **Interaction**: Ask for clarification if any instructions are unclear. Before making significant architectural changes or adding new major features, please propose the plan for review.
- **Language**: All responses, explanations, and code comments should be in Portuguese (pt-br).
- **Project Scope**: Do not make changes to the existing file structure in `talentmatch_project/talentmatch_project/` directory unless absolutely necessary for core functionality.
- **Commit Messages**: Use descriptive commit messages.

## System Architecture
TalentMatch is built on Django 5.2.8 with Python 3.11, utilizing PostgreSQL (Neon-backed) as its database. The frontend employs TailwindCSS via CDN for a modern and responsive UI. The system is designed with a clear separation of concerns, featuring dedicated apps and modules for core functionalities.

### UI/UX Decisions
- **Design System**: Modern and professional visual identity with a vibrant color palette (primary blue, secondary purple, accent pink), gradients, and professional iconography (Lucide icons).
- **Templates**: Redesigned authentication pages (login, candidate registration, company registration) with visual banners and statistical highlights. Dashboards feature colorful "Stat-Cards" with gradient backgrounds and blur effects. Job listing pages include enhanced search bars, visually appealing job cards with gradient logos, and clear match percentage indicators.
- **Responsiveness**: All templates maintain responsiveness across various devices.

### Technical Implementations
- **Core Application (`core/`)**: Contains models, views, URLs, the matching algorithm, and Django Admin configurations.
- **Database Models**: Key models include `Candidato`, `Empresa`, `Vaga`, `Match`, `Candidatura`, `Mensagem`, `Curso`, `ProgressoCurso`, and `Notificacao`, ensuring a robust data structure for all platform functionalities.
- **Matching Algorithm**: Calculates a compatibility score (0-100) based on weighted criteria: Skills (40%), Experience (20%), Location (20%), and Salary (15%). Weights are configurable via `settings.MATCHING_WEIGHTS` and are null-safe.
- **APIs**: Comprehensive set of RESTful APIs for matching, applications, AI chat, notifications, and messaging, all with robust input validation, permission checks, and error handling.
- **Authentication**: Full user authentication system with email and password validation, secure hashing, and intelligent redirection.
- **Admin Panel**: Django's built-in admin panel (`/gerenciador/`) for managing users, companies, and jobs.
- **Robustness**: Includes safeguards against data corruption, null-safe operations, and error handling with appropriate HTTP status codes.
- **Performance**: Optimized database queries using `select_related`/`prefetch_related`, caching for dashboard counters, and database indexing on critical fields.

### Feature Specifications
- **Candidates**: Complete registration/login, personalized dashboard, detailed profile management, job exploration with filters, real-time compatibility score for applications, AI career assistant, course tracking, internal messaging, and notifications.
- **Companies**: CNPJ-validated registration, enterprise dashboard, job posting with detailed requirements, automatic candidate matching, and application management.
- **Administrators**: Comprehensive administrative dashboard, user/company/job management with filters, and platform analytics/reports.

## External Dependencies
- **PostgreSQL**: Primary database, configured via `DATABASE_URL`.
- **OpenAI API**: Used for the AI career assistant feature (GPT-4o-mini model), requiring `OPENAI_API_KEY`.
- **TailwindCSS**: Frontend styling and utility-first CSS framework, integrated via CDN.
- **Python Libraries**:
    - `django>=5.2.8`
    - `gunicorn>=23.0.0`
    - `psycopg2-binary>=2.9.10`
    - `dj-database-url>=2.3.0`
    - `openai>=1.58.1`