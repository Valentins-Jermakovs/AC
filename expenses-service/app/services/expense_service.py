from datetime import datetime

from app.models.expense_model import Expense
from app.schemas.create_schema import ExpenseCreateSchema
from app.schemas.update_schema import ExpenseUpdateSchema
from app.schemas.filters_schema import ExpenseFilter
from app.schemas.response_schema import ExpenseResponse

# ========================
# CREATE
# ========================
async def create_expense(
    data: ExpenseCreateSchema, 
    user_id: str
) -> Expense:
    
    expense = Expense(
        user_id=user_id,
        amount=data.amount,
        category=data.category,
        description=data.description,
        date=datetime.now()
    )

    await expense.save()
    return ExpenseResponse(
        id=str(expense.id),
        amount=expense.amount,
        category=expense.category,
        date=expense.date,
        description=expense.description,
    )


# ========================
# GET with filters
# ========================
async def get_expenses(
    user_id: str,
    filters: ExpenseFilter
) -> list[Expense]:
    
    query = {
        "user_id": user_id
    }

    if filters.from_date:
        query["date"] = {"$gte": filters.from_date}

    if filters.to_date:
        query.setdefault("date", {})
        query["date"]["$lte"] = filters.to_date

    if filters.category:
        query["category"] = filters.category

    expenses = await Expense.find(query).sort("-date").to_list()

    return [
        ExpenseResponse(
            id=str(expense.id),
            amount=expense.amount,
            category=expense.category,
            date=expense.date,
            description=expense.description,
        )
        for expense in expenses
    ]


# ========================
# UPDATE
# ========================
async def update_expense(expense_id: str, data: ExpenseUpdateSchema):
    expense = await Expense.get(expense_id)

    if not expense:
        return None

    update_data = data.model_dump(exclude_unset=True)

    expense = expense.model_copy(update=update_data)

    await expense.save()
    return ExpenseResponse(
        id=str(expense.id),
        amount=expense.amount,
        category=expense.category,
        date=expense.date,
        description=expense.description,
    )


# ========================
# DELETE
# ========================
async def delete_expense(expense_id: str):
    expense = await Expense.get(expense_id)
    await expense.delete()


# ========================
# GET stats
# ========================
async def get_stats(user_id: str):
    pipeline = [
        {"$match": {"user_id": user_id}},
        {
            "$group": {
                "_id": "$category",
                "total": {"$sum": "$amount"}
            }
        }
    ]

    return await Expense.aggregate(pipeline).to_list()
