# Architecture Diagrams

Generated from repository inspection on 2026-06-08.

## High-Level Architecture

```mermaid
flowchart LR
  Operator["IMD/CWC Reviewer or Forecaster"] --> UI["Vite React Workstation"]
  UI --> API["FastAPI Operational Backend"]
  API --> Sounding["Wyoming / Cached Sounding Ingestion"]
  API --> Engines["Thermodynamic, Forecast, Verification, Research Engines"]
  API --> DB["Supabase PostgreSQL"]
  API --> Files["CSV/XLS/XLSX Upload and Export Workflows"]
  Engines --> Outputs["Nowcast, Verification, Registry, Bulletins, District Impacts"]
```

## Component Architecture

```mermaid
flowchart TB
  App["frontend/src/App.jsx"] --> Sidebar["Sidebar Navigation"]
  App --> Radar["RadarConsole"]
  App --> Predictor["PredictorEngine"]
  App --> Analytics["AnalyticsDeck"]
  App --> Research["ResearchHub"]
  App --> Phase3["Phase3OpsModule"]
  App --> Health["HealthConsole"]
  Research --> Archive["Historical Thunderstorm Archive"]
  Research --> Simulator["Forecast Simulator"]
  Research --> Verify["Forecast Verification"]
  Phase3 --> Andhra["Coastal Thunderstorm Monitoring Center"]
  Phase3 --> Bulletin["Auto IMD Bulletin Generator"]
```

## Deployment Architecture

```mermaid
flowchart LR
  Render["Single Render Web Service"] --> Build["Build: pip install + npm install + npm run build"]
  Build --> Dist["frontend/dist"]
  Render --> Uvicorn["uvicorn backend.main:app"]
  Uvicorn --> Static["FastAPI serves /assets and SPA fallback"]
  Uvicorn --> API["FastAPI API routes"]
  API --> Supabase["Supabase PostgreSQL"]
```

## Authentication Flow

```mermaid
sequenceDiagram
  participant User
  participant React
  participant FastAPI
  participant DB as Supabase users table
  User->>React: Enter login credentials
  React->>FastAPI: POST /auth/login
  FastAPI->>DB: Lookup user by email
  DB-->>FastAPI: User record
  FastAPI-->>React: Bearer token and profile
  React->>FastAPI: Authenticated requests with Authorization header
  FastAPI-->>React: Protected operational outputs
```

## Forecast Pipeline

```mermaid
flowchart TD
  Cycle["00Z / 12Z Cycle Lock"] --> Sounding["Sounding Fetch and Cache"]
  Sounding --> Thermo["Thermodynamic Solver"]
  Thermo --> Indices["CAPE, CIN, LI, PWAT, SWEAT, K-index"]
  Indices --> Prob["Probabilistic Forecast Engine"]
  Indices --> Lifecycle["Convective Lifecycle Engine"]
  Prob --> Decision["Operational Decision Support"]
  Lifecycle --> Decision
  Decision --> Bulletin["Bulletin / Watch / Advisory Outputs"]
  Decision --> Verification["Verification and Trust Scoring"]
```

