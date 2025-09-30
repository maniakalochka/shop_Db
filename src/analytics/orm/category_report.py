from sqlalchemy import func, select

from models.category import Category


def category_children_count(only_roots: bool = False):
    """
    Найти количество дочерних элементов первого уровня вложенности для категорий
    :param only_roots: если True — только для корневых категорий
    """
    child = Category.__table__.alias("ch")

    stmt = (
        select(Category.id, Category.name, func.count(child.c.id).label("child_count"))
        .join(child, child.c.parent_id == Category.id, isouter=True)
        .group_by(Category.id, Category.name)
        .order_by(Category.name)
    )

    if only_roots:
        stmt = stmt.where(Category.parent_id.is_(None))

    return stmt
