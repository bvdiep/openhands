import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.runner import run_task

# 1. Cấu hình
cwd = "/home/dd/work/codes/HP/hp-lms-be"

# 2. Nhiệm vụ
task_prompt = """
Your mission is to refactor the LessonVersionEntity to extract quiz data from the JSON column into a separate table.

## Context
I am refactoring the `LessonVersionEntity` in a NestJS + TypeORM + MySQL project. Currently, the lesson content (quizzes) is stored as a JSON array in the `quiz_schema` column. I want to extract this into a separate, generic table to improve data structure and queryability.

## Current Codebase Analysis

### Key Entities
- **`LessonVersionEntity`** (`src/entities/lesson.entity.ts`): Main lesson entity with `quiz_schema` as JSON column
- **`CourseVersionEntity`** (`src/entities/course-version.entity.ts`): Manages course versions with topics and lessons
- **`TopicEntity`**: Contains lessons for a specific course version
- **`UserLessonProgressEntity`**: Tracks user progress and quiz submissions

### Services to Update
1. **CoursesService** (`src/modules/courses/courses.service.ts`): Handles course version cloning
2. **LessonsService** (`src/modules/lessons/lessons.service.ts`): Manages lesson operations and quiz schema
3. **LessonsSqlService** (`src/modules/lessons/lessons-sql.service.ts`): SQL operations for lessons
4. **New Service**: LessonActivitiesSqlService for the new entity

### Important Methods to Consider
- `cloneCourseVersion()` in CoursesService: Handles course version cloning, which includes lessons
- `findOne()` and `findOnePublic()` in LessonsService: Modify quiz_schema before return

## Objective

1. **Rename & Generalize**: Instead of "Quiz", use the term **"Activity"** or **"LessonItem"** (Let's go with `LessonActivityEntity`).
2. **Database Migration**: Move data from the `quiz_schema` (JSON) column in the `lesson` table to a new `lesson_activities` table.
3. **Maintain Compatibility**: Ensure the existing API responses and logic still work by using TypeORM's `@AfterLoad` or a virtual getter to map the new relation back to the old `quiz_schema` format if necessary, or update the services/repositories to handle the new relation while maintaining the same DTO output.

## Technical Requirements

### 1. Create `LessonActivityEntity`
- **File**: `src/entities/lesson-activity.entity.ts`
- **Fields**:
  - `id` (Primary Key, UUID)
  - `lesson_id` (Foreign Key to LessonVersionEntity)
  - `type` (enum: 'single', 'multiple', 'true_false', 'sort')
  - `content` (text)
  - `options` (json)
  - `correct` (json)
  - `answer_text` (text, nullable)
  - `order_index` (int)
- **Relationships**:
  - `ManyToOne` to `LessonVersionEntity`
  - Establish proper TypeORM decorators

### 2. Update `LessonVersionEntity`
- **File**: `src/entities/lesson.entity.ts`
- Add `@OneToMany` relationship to `LessonActivityEntity`
- Keep the `quiz_schema` property but handle it as a virtual property/getter 
- Use `@Exclude()` decorator to exclude from direct serialization
- Implement logic to map `activities` relation to `quiz_schema` format for backward compatibility

### 3. Update Data Models
- **File**: `src/model/lesson.model.ts`
- Create `LessonActivityModel` class with appropriate properties
- Update `LessonModel` to include `activities` property
- Keep `quiz_schema` property for backward compatibility
- Ensure both properties are properly exposed via class-transformer decorators

### 4. Create SQL Service for Lesson Activities
- **File**: `src/modules/lessons/lesson-activities-sql.service.ts`
- Extend `BaseSqlService<LessonActivityEntity>`
- Implement basic CRUD operations
- Add methods to find activities by lesson ID

### 5. Update Lessons Service
- **File**: `src/modules/lessons/lessons.service.ts`
- Modify `create()` to handle activities instead of quiz_schema
- Modify `update()` to handle activities instead of quiz_schema  
- Update `findOne()` and `findOnePublic()` to shuffle options for activities
- Ensure quiz_schema fallback still works

### 6. Update Courses Service
- **File**: `src/modules/courses/courses.service.ts`
- Modify `cloneCourseVersion()` to also clone lesson activities
- When cloning lessons, ensure all associated activities are also cloned

### 7. Database Migration Strategy
- Create a TypeORM migration file that:
  - Creates the `lesson_activities` table
  - Reads existing JSON data from `lesson.quiz_schema`
  - Parses and inserts it into the new `lesson_activities` table
  - Keeps the old column for a short period or handles the fallback
  - Sets appropriate order_index for each activity

### 8. Update DTOs
- **Files**: `src/dtos/lessons/*.dto.ts`
- Update `CreateLessonVersionRequestDto` to accept activities instead of quiz_schema
- Update `UpdateLessonVersionRequestDto` to accept activities instead of quiz_schema
- Ensure the DTO structure matches the new entity

### 9. Update Controllers
- **File**: `src/modules/lessons/lessons.controller.ts`
- Ensure the endpoints accept and return the correct data structures
- Maintain backward compatibility if needed

## Constraints

- Do not delete the `quiz_schema` column until the migration and verification are complete.
- The `options` field in `LessonActivityEntity` should still store the `QuizOption[]` structure as JSON for now to minimize complexity, but it must be in a dedicated column.
- Follow the existing project's naming conventions and coding style.
- Ensure all relationships use lazy loading (`{ lazy: true }`) as in other entities.
- Maintain the existing functionality for quiz option shuffling in public endpoints.

## Implementation Steps

1. Analyze the current `LessonVersionEntity` and `LessonActivity` requirements.
2. Generate the new `LessonActivityEntity` file.
3. Update `LessonVersionEntity` to link them together.
4. Create the `LessonActivityModel` and update `LessonModel`.
5. Create the LessonActivitiesSqlService.
6. Update the LessonsService to handle the new relation.
7. Update the CoursesService to handle cloning of activities.
8. Update the DTOs and controllers.
9. Generate and run the migration script.
10. Test the changes to ensure backward compatibility.

## Key Considerations

### Cloning Mechanism
The `cloneCourseVersion()` method in CoursesService must be updated to properly clone lesson activities. When a course version is cloned:
1. All topics are cloned
2. All lessons are cloned 
3. All activities for each lesson must also be cloned
4. The new activities must reference the new lesson IDs

### Data Migration
The migration must properly parse the existing JSON data from `quiz_schema` and create individual activity records. Each activity should retain all the properties from the quiz schema.

### Backward Compatibility
The `quiz_schema` property should still be available on the API responses during the transition period. This can be achieved by:
1. Adding a virtual getter that maps the `activities` relation to the old quiz_schema format
2. Using `@Expose()` decorator to ensure it's included in the response
3. Implementing `@AfterLoad()` hook to handle the mapping

## Verification Steps

1. Test course version cloning with activities
2. Test lesson creation and update with activities
3. Test that existing API endpoints still work
4. Verify that quiz options are still shuffled for public users
5. Check that data is properly migrated from the old column to the new table
"""

# 3. Chạy nhiệm vụ
if __name__ == "__main__":
    run_task(
        task_prompt=task_prompt,
        workspace=cwd,
        model="openai/sonnet-4",
        api_key=os.getenv("LITELLM_KEY", "no-key"),
        base_url="http://localhost:4000/v1",
        success_message="Nhiệm vụ hoàn tất! Kiểm tra code"
    )
