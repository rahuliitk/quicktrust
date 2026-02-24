from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.training import TrainingCourse, TrainingAssignment
from app.schemas.training import (
    TrainingCourseCreate, TrainingCourseUpdate,
    TrainingAssignmentCreate, TrainingAssignmentUpdate,
)


# === Courses ===

async def list_courses(
    db: AsyncSession,
    org_id: UUID,
    is_active: bool | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[TrainingCourse], int]:
    base_q = select(TrainingCourse).where(TrainingCourse.org_id == org_id)
    count_q = select(func.count()).select_from(TrainingCourse).where(TrainingCourse.org_id == org_id)

    if is_active is not None:
        base_q = base_q.where(TrainingCourse.is_active == is_active)
        count_q = count_q.where(TrainingCourse.is_active == is_active)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(TrainingCourse.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_course(db: AsyncSession, org_id: UUID, data: TrainingCourseCreate) -> TrainingCourse:
    course = TrainingCourse(org_id=org_id, **data.model_dump())
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return course


async def get_course(db: AsyncSession, org_id: UUID, course_id: UUID) -> TrainingCourse:
    result = await db.execute(
        select(TrainingCourse).where(TrainingCourse.id == course_id, TrainingCourse.org_id == org_id)
    )
    course = result.scalar_one_or_none()
    if not course:
        raise NotFoundError(f"Training course {course_id} not found")
    return course


async def update_course(
    db: AsyncSession, org_id: UUID, course_id: UUID, data: TrainingCourseUpdate
) -> TrainingCourse:
    course = await get_course(db, org_id, course_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return course


async def delete_course(db: AsyncSession, org_id: UUID, course_id: UUID) -> None:
    course = await get_course(db, org_id, course_id)
    await db.delete(course)
    await db.commit()


# === Assignments ===

async def list_assignments(
    db: AsyncSession,
    org_id: UUID,
    course_id: UUID | None = None,
    status: str | None = None,
    page: int = 1,
    page_size: int = 50,
) -> tuple[list[TrainingAssignment], int]:
    base_q = select(TrainingAssignment).where(TrainingAssignment.org_id == org_id)
    count_q = select(func.count()).select_from(TrainingAssignment).where(TrainingAssignment.org_id == org_id)

    if course_id:
        base_q = base_q.where(TrainingAssignment.course_id == course_id)
        count_q = count_q.where(TrainingAssignment.course_id == course_id)
    if status:
        base_q = base_q.where(TrainingAssignment.status == status)
        count_q = count_q.where(TrainingAssignment.status == status)

    total = (await db.execute(count_q)).scalar() or 0
    q = base_q.offset((page - 1) * page_size).limit(page_size).order_by(TrainingAssignment.created_at.desc())
    result = await db.execute(q)
    return list(result.scalars().all()), total


async def create_assignment(
    db: AsyncSession, org_id: UUID, data: TrainingAssignmentCreate, assigned_by_id: UUID | None = None
) -> TrainingAssignment:
    assignment = TrainingAssignment(
        org_id=org_id,
        course_id=data.course_id,
        user_id=data.user_id,
        due_date=data.due_date,
        assigned_by_id=assigned_by_id,
    )
    db.add(assignment)
    await db.commit()
    await db.refresh(assignment)
    return assignment


async def update_assignment(
    db: AsyncSession, org_id: UUID, assignment_id: UUID, data: TrainingAssignmentUpdate
) -> TrainingAssignment:
    result = await db.execute(
        select(TrainingAssignment).where(
            TrainingAssignment.id == assignment_id, TrainingAssignment.org_id == org_id
        )
    )
    assignment = result.scalar_one_or_none()
    if not assignment:
        raise NotFoundError(f"Assignment {assignment_id} not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(assignment, field, value)

    # Auto-set completed_at when status changes to completed
    if "status" in update_data and update_data["status"] == "completed" and not assignment.completed_at:
        assignment.completed_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(assignment)
    return assignment


# === Stats ===

async def get_training_stats(db: AsyncSession, org_id: UUID) -> dict:
    courses_count = (await db.execute(
        select(func.count()).select_from(TrainingCourse).where(TrainingCourse.org_id == org_id)
    )).scalar() or 0

    result = await db.execute(
        select(TrainingAssignment).where(TrainingAssignment.org_id == org_id)
    )
    assignments = list(result.scalars().all())

    assigned = len(assignments)
    completed = sum(1 for a in assignments if a.status == "completed")
    overdue = sum(1 for a in assignments if a.status == "overdue")

    return {
        "total_courses": courses_count,
        "assigned": assigned,
        "completed": completed,
        "overdue": overdue,
        "completion_rate_pct": round((completed / assigned * 100), 1) if assigned else 0.0,
    }
