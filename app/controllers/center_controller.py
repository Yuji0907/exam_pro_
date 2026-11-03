
from sqlalchemy.orm import Session

from repositories.center_repos import CenterRepository, CenterAssignmentRepository
from models.center_model import CenterModel, CenterAssignmentModel


class CenterController:

    def __init__(
        self,
        view,
        session: Session
    ):
        self.view = view
        self.session = session

        self.center_repo = CenterRepository(
            session
        )

        self.assignment_repo = CenterAssignmentRepository(
            session
        )

    # ==================================================
    # CENTERS
    # ==================================================

    # --------------------------------------------------
    # Load centers
    # --------------------------------------------------

    def load_centers(self):

        centers = self.center_repo.get_all()

        self.view.display_centers(
            centers
        )

    # --------------------------------------------------
    # Load one center
    # --------------------------------------------------

    def load_center(
        self,
        center_id: int
    ):

        center = self.center_repo.get(center_id)

        if center is None:

            print(
                f"No center found with id "
                f"{center_id}"
            )

            return

        self.view.display_center(
            center
        )

    # --------------------------------------------------
    # Create
    # --------------------------------------------------

    def create_center(
        self,
        name: str
    ):

        try:

            name = name.strip()

            if not name:

                self.view.show_error(
                    "Center name cannot be empty."
                )

                return

            center, already_exists = (
                self.center_repo.create(
                    name=name
                )
            )

            if already_exists:

                self.view.show_error(
                    f"Center already exists: "
                    f"{center.name}"
                )

                return

            self.session.commit()

            self.view.show_success(
                f"Center created: "
                f"{center.name}"
            )

            self.load_centers()

        except Exception as e:

            self.session.rollback()

            self.view.show_error(
                str(e)
            )

    # --------------------------------------------------
    # Update
    # --------------------------------------------------

    def update_center(
        self,
        center: CenterModel
    ):

        try:

            updated = (
                self.center_repo
                .update(center)
            )

            if updated is None:

                self.view.show_error(
                    "Center not found."
                )

                return

            self.session.commit()

            self.view.show_success(
                "Center updated."
            )

            self.load_centers()

        except Exception as e:

            self.session.rollback()

            self.view.show_error(
                str(e)
            )

    # --------------------------------------------------
    # Delete
    # --------------------------------------------------

    def delete_center(
        self,
        center_id: int
    ):

        try:

            # A center that still has assignments can't be deleted
            assignments = (
                self.assignment_repo
                .get_by_center(center_id)
            )

            if assignments:

                self.view.show_error(
                    f"This center still has "
                    f"{len(assignments)} assignment(s). "
                    f"Reassign or remove them first."
                )

                return

            deleted = (
                self.center_repo
                .delete(center_id)
            )

            if not deleted:

                self.view.show_error(
                    "Center not found."
                )

                return

            self.session.commit()

            self.view.show_success(
                "Center deleted."
            )

            self.load_centers()

        except Exception as e:

            self.session.rollback()

            self.view.show_error(
                str(e)
            )



    # --------------------------------------------------
    # Load assignments
    # --------------------------------------------------

    def load_assignments(self):

        assignments = self.assignment_repo.get_all()

        self.view.display_assignments(
            assignments
        )

    def load_assignments_by_center(
        self,
        center_id: int
    ):

        assignments = (
            self.assignment_repo
            .get_by_center(center_id)
        )

        self.view.display_assignments(
            assignments
        )

    def load_assignments_by_grade(
        self,
        grade_id: int
    ):

        assignments = (
            self.assignment_repo
            .get_by_grade(grade_id)
        )

        self.view.display_assignments(
            assignments
        )

    def load_assignments_by_willaya(
        self,
        willaya_id: int
    ):

        assignments = (
            self.assignment_repo
            .get_by_willaya(willaya_id)
        )

        self.view.display_assignments(
            assignments
        )

    # --------------------------------------------------
    # Load one assignment
    # --------------------------------------------------

    def load_assignment(
        self,
        grade_id: int,
        willaya_id: int
    ):

        assignment = (
            self.assignment_repo
            .get(grade_id, willaya_id)
        )

        if assignment is None:

            print(
                f"No assignment found for grade "
                f"{grade_id} and willaya {willaya_id}"
            )

            return

        self.view.display_assignment(
            assignment
        )

    # --------------------------------------------------
    # Find the center for a grade + willaya
    # --------------------------------------------------

    def load_center_for(
        self,
        grade_id: int,
        willaya_id: int
    ):

        center = (
            self.assignment_repo
            .get_center(grade_id, willaya_id)
        )

        if center is None:

            print(
                f"No center assigned for grade "
                f"{grade_id} and willaya {willaya_id}"
            )

            return

        self.view.display_center(
            center
        )

    # --------------------------------------------------
    # Create
    # --------------------------------------------------

    def create_assignment(
        self,
        grade_id: int,
        willaya_id: int,
        center_id: int
    ):

        try:

            assignment, already_exists = (
                self.assignment_repo.create(
                    grade_id=grade_id,
                    willaya_id=willaya_id,
                    center_id=center_id
                )
            )

            if already_exists:

                self.view.show_error(
                    f"Assignment already exists for grade "
                    f"{grade_id} and willaya {willaya_id}"
                )

                return

            self.session.commit()

            self.view.show_success(
                "Assignment created."
            )

            self.load_assignments()

        except Exception as e:

            self.session.rollback()

            self.view.show_error(
                str(e)
            )

    # --------------------------------------------------
    # Update (move to another center)
    # --------------------------------------------------

    def update_assignment(
        self,
        assignment: CenterAssignmentModel
    ):

        try:

            updated = (
                self.assignment_repo
                .update(assignment)
            )

            if updated is None:

                self.view.show_error(
                    "Assignment not found."
                )

                return

            self.session.commit()

            self.view.show_success(
                "Assignment updated."
            )

            self.load_assignments()

        except Exception as e:

            self.session.rollback()

            self.view.show_error(
                str(e)
            )

    # --------------------------------------------------
    # Assign (create, or move if it already exists)
    # --------------------------------------------------

    def assign_center(
        self,
        grade_id: int,
        willaya_id: int,
        center_id: int
    ):

        try:

            self.assignment_repo.assign(
                grade_id=grade_id,
                willaya_id=willaya_id,
                center_id=center_id
            )

            self.session.commit()

            self.view.show_success(
                "Center assigned."
            )

            self.load_assignments()

        except Exception as e:

            self.session.rollback()

            self.view.show_error(
                str(e)
            )

    # --------------------------------------------------
    # Move every assignment from one center to another
    # --------------------------------------------------

    def reassign_center(
        self,
        old_center_id: int,
        new_center_id: int
    ):

        try:

            if old_center_id == new_center_id:

                self.view.show_error(
                    "Source and target centers are the same."
                )

                return

            moved = (
                self.assignment_repo
                .reassign_center(
                    old_center_id,
                    new_center_id
                )
            )

            self.session.commit()

            self.view.show_success(
                f"{moved} assignment(s) moved."
            )

            self.load_assignments()

        except Exception as e:

            self.session.rollback()

            self.view.show_error(
                str(e)
            )

    # --------------------------------------------------
    # Delete
    # --------------------------------------------------

    def delete_assignment(
        self,
        grade_id: int,
        willaya_id: int
    ):

        try:

            deleted = (
                self.assignment_repo
                .delete(grade_id, willaya_id)
            )

            if not deleted:

                self.view.show_error(
                    "Assignment not found."
                )

                return

            self.session.commit()

            self.view.show_success(
                "Assignment deleted."
            )

            self.load_assignments()

        except Exception as e:

            self.session.rollback()

            self.view.show_error(
                str(e)
            )

    def delete_assignments_by_center(
        self,
        center_id: int
    ):

        try:

            count = (
                self.assignment_repo
                .delete_by_center(center_id)
            )

            self.session.commit()

            self.view.show_success(
                f"{count} assignment(s) deleted."
            )

            self.load_assignments()

        except Exception as e:

            self.session.rollback()

            self.view.show_error(
                str(e)
            )