import aiomysql

async def create_db_pool(host, port, user, password, database):
    """
    Creates and returns an aiomysql connection pool.
    """
    try:
        pool = await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=database,
            autocommit=True, # Ensure changes are committed immediately
            charset='utf8mb4', # Recommended for broader character support
            cursorclass=aiomysql.cursors.DictCursor # Return results as dictionaries
        )
        print("Database connection pool created successfully.")
        return pool
    except aiomysql.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

async def close_db_pool(pool):
    """
    Closes the database connection pool.
    """
    if pool:
        pool.close()
        await pool.wait_closed()
        print("Database connection pool closed.")