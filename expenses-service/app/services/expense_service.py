from datetime import datetime
from fastapi import HTTPException
from app.models.expense_model import Expense
from app.schemas.expenses.create_expense_schema import ExpenseCreateSchema
from app.schemas.expenses.update_expense_schema import ExpenseUpdateSchema
from app.schemas.expenses.expense_filters_schema import ExpenseFilter
from app.schemas.expenses.response_expense_schema import ExpenseResponse, PaginatedResponse
from app.schemas.expenses.expense_stats_schema import ExpenseStatsResponse
from bson import ObjectId
import math

# ========================
# CREATE
# ========================
async def create_expense(
    data: ExpenseCreateSchema, 
    user_id: str
) -> ExpenseResponse:
    
    # Validation
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")


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
    filters: ExpenseFilter,
    page: int = 1,
    limit: int = 10
) -> PaginatedResponse:

    if page < 1:
        page = 1

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    if filters.from_date and filters.to_date:
        if filters.from_date > filters.to_date:
            raise HTTPException(
                status_code=400,
                detail="from_date cannot be greater than to_date"
            )

    query = {"user_id": user_id}

    if filters.from_date:
        query["date"] = {"$gte": filters.from_date}

    if filters.to_date:
        query.setdefault("date", {})
        query["date"]["$lte"] = filters.to_date

    if filters.category:
        query["category"] = filters.category

    skip = (page - 1) * limit

    expenses = await Expense.find(query)\
        .sort("-date")\
        .skip(skip)\
        .limit(limit)\
        .to_list()

    items = [
        ExpenseResponse(
            id=str(expense.id),
            amount=expense.amount,
            category=expense.category,
            date=expense.date,
            description=expense.description,
        )
        for expense in expenses
    ]

    total_items = await Expense.find(query).count()
    total_pages = math.ceil(total_items / limit) if limit > 0 else 0

    return PaginatedResponse(
        items=items,
        total_items=total_items,
        limit=limit,
        page=page,
        total_pages=total_pages
    )


# ========================
# UPDATE
# ========================
async def update_expense(
    expense_id: str, 
    data: ExpenseUpdateSchema,
    user_id: str
) -> ExpenseResponse:
    
    if ObjectId.is_valid(expense_id) is False:
        raise HTTPException(status_code=400, detail="Invalid expense ID")
    
    expense = await Expense.get(expense_id)

    # validation
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    if not expense or expense.user_id != user_id:
        raise HTTPException(status_code=404, detail="Expense not found")
    

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
async def delete_expense(
    expense_id: str,
    user_id: str
):

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    if ObjectId.is_valid(expense_id) is False:
        raise HTTPException(status_code=400, detail="Invalid expense ID")

    expense = await Expense.get(expense_id)

    if not expense or expense.user_id != user_id:
        raise HTTPException(status_code=404, detail="Expense not found")

    await expense.delete()

    return {
        "message": "Expense deleted successfully"
    }


# ========================
# GET stats
# ========================
async def get_stats(
    user_id: str
) -> list[ExpenseStatsResponse]:
    
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    pipeline = [
        {"$match": {"user_id": user_id}},
        {
            "$group": {
                "_id": "$category",
                "total": {"$sum": "$amount"}
            }
        },
        {
            "$project": {
                "category": "$_id",
                "total": 1,
                "_id": 0
            }
        }
    ]

    stats = await Expense.aggregate(pipeline).to_list()

    return [ExpenseStatsResponse(**item) for item in stats]
