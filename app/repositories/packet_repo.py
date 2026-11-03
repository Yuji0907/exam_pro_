from sqlalchemy.orm import Session
from sqlalchemy import select,and_
from database.orm_models import Packet as PacketORM
from models.packet_model import Packet as PacketModel


class PacketRepository:

    def __init__(self, session: Session):
        self.session = session

    # --------------------------------------------------
    # ORM -> Domain
    # --------------------------------------------------

    def _to_model(
        self,
        packet: PacketORM
    ) -> PacketModel:

        return PacketModel(
            willaya_id=packet.willaya_id,
            subject_id=packet.subject_id,
            number=packet.number,
            total_number=packet.total_number,
            current_count=packet.current_count,
            name=packet.name,
        )

    # --------------------------------------------------
    # Get all
    # --------------------------------------------------

    def get_all(self) -> list[PacketModel]:

        packets = (
            self.session
            .query(PacketORM)
            .all()
        )

        return [
            self._to_model(packet)
            for packet in packets
        ]

    # --------------------------------------------------
    # Get by ID
    # --------------------------------------------------

    def get_by_id(
        self,
        willaya_id: int,
        subject_id: int,
        number: int,
    ) -> PacketModel | None:

        code = self.session.get(
            PacketORM,
            (willaya_id,
                subject_id,
                number)
        )

        if code is None:
            return None

        return self._to_model(code)
    
    def get_by_id_orm(
        self,
        willaya_id: int,
        subject_id: int,
        number: int,
    ) -> PacketORM | None:

        packet = self.session.get(
            PacketORM,
            (willaya_id,
                subject_id,
                number)
        )

        if packet is None:
            return None

        return packet
    
    def get_by_willaya_subject(
        self,
        willaya_id: int,
        subject_id: int
    ) -> list[PacketModel] | None:

        packets = self.session.scalars(
            select(PacketORM).where(
                and_(
                PacketORM.willaya_id == willaya_id,
                PacketORM.subject_id == subject_id,
                PacketORM.total_number > PacketORM.current_count
                )
            )
        ).all()

        if packets is None:
            return []

        return [
            self._to_model(paket)
            for paket in packets
        ]

    def get_by_id(
        self,
        willaya_id: int,
        subject_id: int,
        number: int,
    ) -> PacketModel | None:

        code = self.session.get(
            PacketORM,
            (willaya_id,
                subject_id,
                number)
        )

        if code is None:
            return None

        return self._to_model(code)


    # --------------------------------------------------
    # Create
    # --------------------------------------------------

    def create(
        self,
        willaya_id: int,
        subject_id: int,
        number: int,
        total_number:int,
        name: str,
    ) -> tuple[PacketModel, bool]:

        existing = self.get_by_id(willaya_id,subject_id,number)

        if existing:
            return existing, True

        packet_orm = PacketORM(
            willaya_id=willaya_id,
            subject_id=subject_id,
            number=number,
            total_number=total_number,
            name=name,
            current_count=0
        )

        self.session.add(packet_orm)
        self.session.commit()
        self.session.refresh(packet_orm)

        return self._to_model(packet_orm), False

    # --------------------------------------------------
    # update
    # --------------------------------------------------

    def update(
        self,packet : PacketModel ) -> PacketModel:
        orm_packet = self.get_by_id_orm(willaya_id=packet.willaya_id,
                                        subject_id=packet.subject_id,
                                        number=packet.number)
        print("===================")
        if not orm_packet:
            raise ValueError(
                f"No code found for id={packet.id}, "
            )

        orm_packet.number = packet.number
        orm_packet.subject_id = packet.subject_id
        orm_packet.willaya_id = packet.willaya_id
        orm_packet.current_count = packet.current_count
        orm_packet.name = packet.name
        orm_packet.total_number = packet.total_number

        self.session.commit()
        self.session.refresh(orm_packet)
        return self._to_model(orm_packet)
    

    # --------------------------------------------------
    # Delete
    # --------------------------------------------------

    def delete(
        self,
        willaya_id: int,
        subject_id: int,
        number: int,
    ) -> bool:

        # code_orm = (
        #     self.session
        #     .query(PacketORM)
        #     .filter(
        #         PacketORM.code == code
        #     )
        #     .first()
        # )

        # if code_orm is None:
        #     return False

        # self.session.delete(code_orm)
        # self.session.commit()

        return True