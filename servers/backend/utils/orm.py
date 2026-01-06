from sqlalchemy.ext.asyncio import AsyncResult

def convert_orm_to_tuple(orm_result: AsyncResult):
    """
    Converts the ORM results from a query to a list of values
    :param orm_result:
    :return:
    """
    return orm_result.scalars().all()
