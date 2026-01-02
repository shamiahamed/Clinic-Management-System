from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Create the async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False, # Set to False in production
    pool_size=20,
    max_overflow=10
)

# Create the session factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# DB Dependency used in our Routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
        await session.commit() # Ensure changes are saved