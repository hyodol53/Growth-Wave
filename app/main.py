
from fastapi import FastAPI
from app.core.database import engine
from app.models import user, organization, external_account, project, project_member, praise, praise_limiter, strength, evaluation

from app.api.endpoints import auth, users, organizations, external_accounts, projects, praises, evaluations

# Create all tables in the database
# In a real application, you would use Alembic for migrations.
user.Base.metadata.create_all(bind=engine)
organization.Base.metadata.create_all(bind=engine)
external_account.Base.metadata.create_all(bind=engine)
project.Base.metadata.create_all(bind=engine)
project_member.Base.metadata.create_all(bind=engine)
praise.Base.metadata.create_all(bind=engine)
praise_limiter.Base.metadata.create_all(bind=engine)
strength.Base.metadata.create_all(bind=engine)
evaluation.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Growth-Wave: Dual-Track HR Platform",
    description="This is the API for the Growth-Wave platform, combining formal evaluations with a growth & culture platform.",
    version="0.1.0"
)

# API Routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(organizations.router, prefix="/api/v1/organizations", tags=["Organizations"])
app.include_router(external_accounts.router, prefix="/api/v1/external-accounts", tags=["External Accounts"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])
app.include_router(praises.router, prefix="/api/v1/praises", tags=["Praises & Strengths"])
app.include_router(evaluations.router, prefix="/api/v1/evaluations", tags=["Evaluations"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Growth-Wave API"}

