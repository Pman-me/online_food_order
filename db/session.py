from db.connection import session_maker


# async def get_db_session():
#     session = async_session()
#     try:
#         yield session
#     finally:
#         await session.close()
#     or
#     async with async_session() as session:
#         yield session


def get_db_session():
    session = session_maker()
    try:
        yield session
    finally:
        session.close()
