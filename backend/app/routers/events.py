import json
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.event_schemas import Event, EventCreate, EventOption, EventUpdate, EventResponse, EventLLMGenerateRequest, EventLLMGenerateResponse
from app.crud import event_crud
from typing import List
from app.models.events import GameEvent
from app.models.options import GameOption
import random
from fastapi import Body
from app.schemas.option_schemas import AttributeChange, OptionCreate
from app.utils.llm_helper import call_llm
from app.crud import option_crud
from fastapi.responses import JSONResponse
from fastapi import FastAPI


router = APIRouter(prefix="/events", tags=["events"])

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@router.post("/", response_model=EventResponse)
def create_new_event_with_options(event: EventCreate, db: Session = Depends(get_db)):
    try:
        db_event = event_crud.create_event(db, event)
        if hasattr(event, 'options') and event.options:
            for option_data in event.options:
                option_data.event_id = db_event.id
                option_crud.create_option(db, OptionCreate(**option_data.dict()))
        db.commit()
        db.refresh(db_event)
        return db_event
    except ValidationError as e:
        print("Validation Error:", e)
        return JSONResponse(status_code=422, content={"detail": e.errors()})

@router.get("/{event_id}", response_model=Event)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = event_crud.get_event(db, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, updated_event: EventUpdate, db: Session = Depends(get_db)):
    print("接收到的数据:", updated_event)

    db_event = db.query(GameEvent).filter(GameEvent.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="事件不存在")

    if updated_event.title is not None:
        db_event.title = updated_event.title
    if updated_event.description is not None:
        db_event.description = updated_event.description
    if updated_event.range_condition is not None:
        db_event.range_condition = updated_event.range_condition.dict()

    db.commit()
    db.refresh(db_event)
    return db_event


@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    success = event_crud.delete_event(db, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return {"ok": True}

@router.get("/", response_model=List[Event])
def read_events_by_game(game_id: int = Query(...), db: Session = Depends(get_db)):
    """
    获取指定游戏的所有事件
    """
    events = event_crud.get_events_by_game(db, game_id)
    return events

@router.post("/random")
def get_random_event(
    game_id: int = Query(...),
    player_attributes: dict = Body(...),
    occurred_events: list[int] = Body(...),  # 新增参数：已发生事件的ID列表
    db: Session = Depends(get_db)
):
    # 解包玩家属性
    player_attributes = player_attributes.get("player_attributes", {})

    # 确保事件ID和occurred_events类型一致
    occurred_events = [int(event_id) for event_id in occurred_events]
    # print(f"所有事件: {[event.id for event in db.query(GameEvent).filter(GameEvent.game_id == game_id).all()]}")
    # print(f"已发生事件: {occurred_events}")

    # 获取所有事件，并排除已发生的事件
    events = db.query(GameEvent).filter(GameEvent.game_id == game_id).all()
    events = [event for event in events if int(event.id) not in occurred_events]

    # 筛选符合玩家属性条件的事件
    valid_events = []
    for event in events:
        if not event.range_condition:
            valid_events.append(event)
            continue
        condition = event.range_condition
        attr_value = player_attributes.get(condition["attribute"], 0)

        # 检查属性是否满足事件的范围条件
        if (condition.get("min_value", float('-inf')) <= attr_value <= condition.get("max_value", float('inf'))):
            valid_events.append(event)

    # 如果没有符合条件的事件，返回 None
    if not valid_events:
        # print("没有符合条件的事件或所有事件已发生")
        return None

    # 随机选择一个事件
    selected_event = random.choice(valid_events)
    # print(f"选中的事件ID: {selected_event.id}")

    # 加载选中的事件的选项
    options = db.query(GameOption).filter(GameOption.event_id == selected_event.id).all()
    # print(f"Selected event ID: {selected_event.id}")
    # print(f"Loaded options: {[o.text for o in options]}")

    # 处理选项数据
    valid_options = []
    for o in options:
        parsed_changes = []
        if o.result_attribute_changes:
            try:
                # 判断 result_attribute_changes 类型并处理
                changes = o.result_attribute_changes if isinstance(o.result_attribute_changes, list) else json.loads(o.result_attribute_changes)
                parsed_changes = [AttributeChange(**change).dict() for change in changes]
            except Exception as e:
                print(f"解析 AttributeChange 失败: {e}, 数据: {o.result_attribute_changes}")
        
        valid_options.append({
            "text": o.text,
            "result_attribute_changes": parsed_changes,
            "impact_description": o.impact_description,
            "triggers_ending": o.triggers_ending,
            "ending_description": o.ending_description
        })


    # 返回选中的事件及其选项
    return {
        "id": selected_event.id,  # 返回事件ID以便前端记录
        "game_id": game_id,
        "title": selected_event.title,
        "description": selected_event.description,
        "options": valid_options
    }


@router.post("/llm_generate", response_model=EventLLMGenerateResponse)
def llm_generate(data: EventLLMGenerateRequest):
    """
    使用 LLM 生成事件扩展描述和选项。
    """
    try:
        # 调用 LLM 生成扩展描述和选项
        extended_description, raw_options = call_llm(data.title, data.description, data.background)
        
        # 将 raw_options 转换为符合 EventOption 格式的列表
        options = [
            EventOption(
                text=option["text"],
                impact_description=option["impact_description"],
                result_attribute_changes=option.get("result_attribute_changes", {})
            )
            for option in raw_options
        ]

        # 返回结果
        return EventLLMGenerateResponse(
            extended_description=extended_description,
            options=options
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating content: {str(e)}")
