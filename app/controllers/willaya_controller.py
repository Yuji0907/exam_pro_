from repositories.willaya_repo import WillayaRepository
from sqlalchemy.orm import Session
from models.willaya_model import WillayaModel


class WillayaController:

    def __init__(self, view, session: Session):
        self.view = view
        self.willaya_repo = WillayaRepository(session)

    def load_willayas(self):
        willayas = self.willaya_repo.get_all()
        self.view.load_willayas(willayas)

    def get_willayas(self):
        return self.willaya_repo.get_all()

    def load_willaya(self, willaya_id: int):
        willaya = self.willaya_repo.get_by_id(willaya_id)

        if willaya:
            self.view.display_willaya(willaya)
        else:
            self.view.show_error(
                f"No wilaya found with id={willaya_id}"
            )

    def create_willaya(self, willaya_id: int, willaya: str):
        try:
            new_willaya = self.willaya_repo.create(
                willaya_id,
                willaya
            )

            self.view.show_success(
                f"Wilaya created: {new_willaya.willaya}"
            )

            self.load_willayas()

        except Exception as e:
            self.view.show_error(str(e))

    def update_willaya(
        self,
        willaya: WillayaModel,
        name: str
    ):
        if name is not None:
            willaya.willaya = name

        try:
            self.willaya_repo.update(willaya)
            self.load_willayas()

        except Exception as e:
            self.view.show_error(str(e))

    def delete_willaya(self, willaya_id: int):
        try:
            self.willaya_repo.delete(willaya_id)
            self.load_willayas()

        except Exception as e:
            self.view.show_error(str(e))