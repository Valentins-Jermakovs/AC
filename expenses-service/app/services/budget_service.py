from app.models.budget_model import Budget
from fastapi import HTTPException

# helper function
def to_response(budget: Budget):
    return {
        "id": str(budget.id),
        "month": budget.month,
        "category": budget.category,
        "planned_amount": budget.planned_amount
    }

# Create a new budget
async def create_budget(
    user_id: str, 
    data
) -> dict:

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")
    
    existing = await Budget.find_one({
        "user_id": user_id,
        "month": data.month,
        "category": data.category
    })

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Budget for this category already exists"
        )

    budget = Budget(
        user_id=user_id,
        month=data.month,
        category=data.category,
        planned_amount=data.planned_amount
    )

    await budget.save()
    return to_response(budget)

# Get all budgets
async def get_budgets(
    user_id: str, 
    month: str
) -> list[dict]:

    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    budgets = await Budget.find({
        "user_id": user_id,
        "month": month
    }).to_list()

    return [to_response(b) for b in budgets]


# Update a budget
async def update_budget(
    budget_id: str,
    user_id: str,
    data
):
    budget = await Budget.get(budget_id)

    if not budget or budget.user_id != user_id:
        raise HTTPException(status_code=404, detail="Budget not found")

    update_data = data.model_dump(exclude_unset=True)

    budget = budget.model_copy(update=update_data)

    await budget.save()

    return to_response(budget)

# Delete budget
async def delete_budget(
    budget_id: str,
    user_id: str
):
    budget = await Budget.get(budget_id)

    if not budget or budget.user_id != user_id:
        raise HTTPException(status_code=404, detail="Budget not found")

    await budget.delete()

    return {"message": "Budget deleted successfully"}