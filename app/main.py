
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
# Import all models to ensure they are registered with SQLAlchemy's metadata
from app.models import user, organization, external_account, project, project_member, praise, praise_limiter, strength, evaluation, collaboration
from app.api.endpoints import auth, users, organizations, external_accounts, projects, praises, evaluations, reports, retrospectives, collaborations

# Create all tables in the database
# In a real application, you would use Alembic for migrations.
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Growth-Wave: Dual-Track HR Platform",
    description="This is the API for the Growth-Wave platform, combining formal evaluations with a growth & culture platform.",
    version="0.1.0"
)

# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:5173",  # Frontend default port
    "http://localhost:8000",  # Backend default port (if frontend is served from here)
    "http://localhost:8001",  # Another common port
    # You might need to add other origins where your frontend is hosted
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(organizations.router, prefix="/api/v1/organizations", tags=["Organizations"])
app.include_router(external_accounts.router, prefix="/api/v1/external-accounts", tags=["External Accounts"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(praises.router, prefix="/api/v1/praises", tags=["Praises & Strengths"])
app.include_router(evaluations.router, prefix="/api/v1/evaluations", tags=["Evaluations"])
app.include_router(reports.router, prefix="/api/v1", tags=["Reports"])
app.include_router(retrospectives.router, prefix="/api/v1/retrospectives", tags=["Retrospectives"])
app.include_router(collaborations.router, prefix="/api/v1/collaborations", tags=["Collaborations"])



@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Growth-Wave API"}

