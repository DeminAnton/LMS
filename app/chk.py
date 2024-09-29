import asyncio
from sqlalchemy import text
from db import db_helper  # Import the db_helper from your db.py file

async def test_db_connection():
    # Use the session_getter from the DataBaseHelper class to check the connection
    try:
        async with db_helper.session_factory() as session:
            # Execute a simple query to check the connection
            result = await session.execute(text("SELECT 1"))
            print(f"Connection successful, result: {result.scalar()}")
    except Exception as e:
        print(f"Error occurred while connecting to the database: {e}")
    finally:
        # Dispose of the engine after testing the connection
        await db_helper.dispose()

# Run the test
if __name__ == "__main__":
    asyncio.run(test_db_connection())
