# Learning Management System Database Schema

This document describes the database schema used for organizing lessons, units, and associated content in the repository structure.

## Core Tables

### `units`
- **id**: Integer (Primary Key)
- **title**: String (e.g., `Unit1-basic_chatcompletion`)
- **description**: Text (Optional: human-readable overview of the unit)
- **path**: File path on disk relative to the repository root
- **created_at**: Timestamp

### `lessons`
- **id**: Integer (Primary Key)
- **unit_id**: Integer (Foreign Key to `units.id`)
- **title**: String (e.g., `Lesson 2: API Setup`)
- **overview**: Text (Brief lesson summary)
- **path**: File path on disk relative to the unit directory

### `lesson_sections`
- **id**: Integer (Primary Key)
- **lesson_id**: Integer (Foreign Key to `lessons.id`)
- **section_order**: Integer (Sequential ordering of sections)
- **content**: Text (Processed markdown or plain text)

### `scripts`
- **id**: Integer (Primary Key)
- **lesson_id**: Integer (Foreign Key to `lessons.id`)
- **file_path**: String (Original path of script)
- **content**: Text (Full script code)

## Relationships

- One **unit** has many **lessons**
- One **lesson** has many **lesson_sections** (in order)
- One **lesson** has many **scripts**

## Example Queries

1. **Find all lessons in a unit**:
```sql
SELECT lessons.id, title 
FROM lessons 
WHERE unit_id = (SELECT id FROM units WHERE title = 'Unit3-advanced_agent_patterns');
```

2. **Get a lesson's full content**:
```sql
SELECT 
  units.title, 
  lessons.title, 
  GROUP_CONCAT(section.content || "\n\n", "") 
FROM lesson_sections section 
JOIN lessons ON lesson_id = lessons.id 
JOIN units ON unit_id = units.id 
WHERE lesson_id = 1
GROUP BY lessons.id;
```

3. **Find all scripts for a unit**:
```sql
SELECT 
  units.title AS unit, 
  lessons.title AS lesson, 
  scripts.file_path, 
  scripts.content 
FROM scripts 
JOIN lessons ON scripts.lesson_id = lessons.id 
JOIN units ON lessons.unit_id = units.id 
WHERE units.title = 'Unit2-basic_agent';
```

## How to Insert Lesson Content

When adding new lessons, follow these steps:
1. Create a new entry in `units` for the lesson's parent unit
2. Insert the core lesson into `lessons` with its overview
3. Add each content section to `lesson_sections` with an increasing order
4. Store any code files in `scripts` associated with the lesson

## Anticipated Improvements

Future versions may benefit from:
- A `metadata` table for tracking version history
- A `resources` table for media files (images, PDFs)
- A `quiz_questions` table for assessment content
- An `users` table for tracking student progress