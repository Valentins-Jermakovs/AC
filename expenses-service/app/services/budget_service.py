from app.models.budget_model import Budget


# Create a new budget
async def create_budget(user_id: str, data):
    budget = Budget(
        user_id=user_id,
        month=data.month,
        category=data.category,
        planned_amount=data.planned_amount
    )

    await budget.save()
    return budget

# Get all budgets
async def get_budgets(user_id: str, month: str):
    return await Budget.find({
        "user_id": user_id,
        "month": month
    }).to_list()


# Update a budget
async def update_budget(budget_id: str, data):
    budget = await Budget.get(budget_id)

    if not budget:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(budget, field, value)

    await budget.save()

    return budget

# Delete budget
async def delete_budget(budget_id: str):
    budget = await Budget.get(budget_id)
    if budget:
        await budget.delete()