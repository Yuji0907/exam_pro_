class CandidateModel:
    def __init__(
        self,
        file_number: int,
        first_name: str,
        last_name: str,
        willaya_id: int | None = None,
        # willaya_center_id: int | None = None
    ):
        self.file_number = file_number
        self.first_name = first_name
        self.last_name = last_name
        self.willaya_id = willaya_id
        # self.willaya_center_id = willaya_center_id