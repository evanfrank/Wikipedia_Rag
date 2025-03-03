from dagster import (
    AssetSelection,
    Definitions,
    ScheduleDefinition,
    load_assets_from_modules
    # ConfigurableResource
)
from wikipidea_rag import assets

from .resources import postgres_con

all_assets = load_assets_from_modules([assets])


surifng_schdule = ScheduleDefinition(
    name="surifng_schdule",
    target=AssetSelection.all(),
    cron_schedule="0 0 * * *",  # every day
)

defs = Definitions(
    assets=all_assets,
    schedules=[surifng_schdule],
    resources={
        "localDB": postgres_con(password="password1")
    }
)
