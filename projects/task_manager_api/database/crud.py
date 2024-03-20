from fastapi import Depends
from database.database import get_database_session


@task_router.get("/", status_code=status.HTTP_200_OK)
def get(db: Session = Depends(get_databse_session)):