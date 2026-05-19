# Interface Contracts - Module 6 Parallel Execution

## Agent 1: Comment Threads

CREATES:
- api/app/models.py (add Comment model)
- api/app/schemas.py (add CommentCreate, CommentResponse schemas)
- api/app/main.py (add comment endpoints)

READS (do not modify):
- api/app/models.py (Task model for reference)
- api/app/models.py (User model for author reference)

MODIFIES:
- api/app/models.py (add Comment model)
- api/app/schemas.py (add schemas)
- api/app/main.py (add routes)

DATA SHAPE — Comment model:
{
  id: UUID,
  task_id: UUID (FK to tasks.id),
  author_id: UUID (FK to users.id),
  body: string (1-5000 chars),
  parent_id: UUID | null,
  created_at: timestamp,
  updated_at: timestamp
}

API ENDPOINTS:
- POST /tasks/:task_id/comments
- GET /tasks/:task_id/comments
- PUT /tasks/:task_id/comments/:id
- DELETE /tasks/:task_id/comments/:id

EVENTS EMITTED:
- comment.created { commentId, taskId, authorId, timestamp }
- comment.updated { commentId, taskId, authorId, timestamp }
- comment.deleted { commentId, taskId, authorId, timestamp }

## Agent 2: @Mention Parsing and Notification

CREATES:
- api/app/utils/mention_parser.py
- api/app/services/mention_notification.py

READS (do not modify):
- api/app/models.py (User model to resolve @mentions)

MODIFIES:
- None (standalone utility + service)

DATA SHAPE — Parsed mention:
{
  raw: string,
  username: string,
  user_id: UUID | null,
  position: { start: number, end: number }
}

INTEGRATION POINT:
- mention_parser.parse(text) returns array
- mention_notification.notify() sends notifications
- Called by other features (comments, task descriptions)

EVENTS EMITTED:
- mention.notified { mentionedUserId, sourceType, sourceId, timestamp }

## Agent 3: Audit Log

CREATES:
- api/app/models.py (add AuditLog model)
- api/app/main.py (add audit middleware)

READS (do not modify):
- api/app/models.py (User model for actor reference)

MODIFIES:
- api/app/models.py (add AuditLog model)
- api/app/main.py (register middleware)

DATA SHAPE — AuditLog entry:
{
  id: UUID,
  action: string (create|update|delete),
  resource_type: string (task|team|member|comment),
  resource_id: UUID,
  actor_id: UUID,
  metadata: object,
  timestamp: timestamp
}

INTEGRATION POINT:
- Audit middleware intercepts POST, PUT, DELETE requests
- For non-HTTP events, call auditLog.record() explicitly

EVENTS CONSUMED:
- Listens for *.created, *.updated, *.deleted events if event bus exists
- Otherwise relies on middleware + explicit calls
