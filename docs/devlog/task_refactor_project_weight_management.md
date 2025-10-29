# Task: Refactor Project Weight Management

**Date:** 2025-10-29

## 1. Problem Summary

The existing implementation for managing project participation weights (**FR-A-1.3**) was incorrect. The requirement is that the sum of weights for a single **user** across all their projects must equal 100%.

The previous implementation incorrectly enforced that the sum of weights of all **members** within a single **project** must equal 100%.

## 2. Solution

The entire feature was refactored to be **user-centric** instead of project-centric. This involved a significant change in both the backend API and the frontend UI/UX.

A new workflow was created:

1.  A new page, **Member Weight Management**, was created for managers (e.g., Department Heads) to see a list of their subordinates.
2.  From this page, a manager can select a user to open a new **User Project Weights Dialog**.
3.  This dialog fetches and displays all projects for that specific user, allowing the manager to adjust their participation weights.
4.  The dialog validates that the sum of weights for that user is exactly 100 before saving the changes via the new backend API.

## 3. Summary of File Changes

### Backend API

- The old project-centric API (`POST /projects/members/weights`) was removed.
- New user-centric APIs were introduced:
  - `GET /api/v1/users/{user_id}/project-weights`
  - `PUT /api/v1/users/{user_id}/project-weights`

### Frontend

- **Modified: `frontend/src/services/api.ts`**
  - Removed the old `setProjectMemberWeights` function.
  - Added new `getUserProjectWeights` and `updateUserProjectWeights` functions to align with the new API.

- **Deleted: `frontend/src/components/Admin/ProjectMemberDialog.tsx`**
  - This component contained the incorrect project-centric UI and was no longer needed.

- **Modified: `frontend/src/pages/Admin/ProjectManagementPage.tsx`**
  - Removed the "Manage Members" button and all related state and handler logic for the old, incorrect workflow.

- **Created: `frontend/src/pages/Admin/MemberWeightManagementPage.tsx`**
  - A new page that displays a list of a manager's subordinates, serving as the entry point for the new user-centric workflow.

- **Created: `frontend/src/components/Admin/UserProjectWeightsDialog.tsx`**
  - A new dialog component that allows editing the project weights for a single selected user, ensuring the total sums to 100%.
