from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.plan import PlanBrief
from app.schemas.subscription import SubscriptionBrief
from app.schemas.tenants import TenantsListItem
from app.services.tenants_service import TenantsService


class TenantsController:
    @staticmethod
    async def list(db: AsyncSession, page: int, page_size: int, status: str | None, q: str | None):
        tenants, total = await TenantsService.tenants_list(db, page, page_size, status, q)
        ids = [t.id for t in tenants]
        counts = await TenantsService.user_counts(db, ids)
        subs = await TenantsService.latest_subscriptions(db, ids)

        items = []
        for tenant in tenants:
            subscription_data = subs.get(tenant.id)
            subscription = None
            if subscription_data is not None:
                subscription_row, plan = subscription_data
                subscription = SubscriptionBrief(
                    id=subscription_row.id,
                    status=subscription_row.status,
                    seats=subscription_row.seats,
                    current_period_end=subscription_row.current_period_end,
                    plan=PlanBrief.model_validate(plan),
                )

            items.append(
                TenantsListItem(
                    id=tenant.id,
                    name=tenant.name,
                    slug=tenant.slug,
                    status=tenant.status,
                    owner_user_id=tenant.owner_user_id,
                    default_language=tenant.default_language,
                    user_count=counts.get(tenant.id, 0),
                    subscription=subscription,
                )
            )

        return items, {"page": page, "page_size": page_size, "total": total}
