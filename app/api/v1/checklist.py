from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import ChecklistItem
from app.schemas.checklist import ChecklistRead, ChecklistUpdate
from app.services.governance import delete_checklist_item, update_checklist_item

router = APIRouter(prefix="/checklist-items")


@router.put("/{item_id}", response_model=ChecklistRead)
def edit_checklist_item(item_id: int, payload: ChecklistUpdate, db: Session = Depends(get_db)):
    return update_checklist_item(db, item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_checklist_item(item_id: int, db: Session = Depends(get_db)):
    delete_checklist_item(db, item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
