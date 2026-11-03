from sqlalchemy.orm import Session

from repositories.candidate_repo import CandidateRepository
from repositories.code_format_repo import CodeFormatRepository
from repositories.code_repo import CodeRepository
from repositories.willaya_repo import WillayaRepository 
from repositories.subject_repo import SubjectRepository
from repositories.packet_repo import  PacketRepository

from models.candidate_model import CandidateModel



class AssigningController:
    def __init__(self,view,session: Session):
        self.view = view
        self.candidate_repo = CandidateRepository(session)
        self.code_repo = CodeRepository(session)
        self.willaya_repo = WillayaRepository(session)
        self.subject_repo = SubjectRepository(session)
        self.code_format_repo = CodeFormatRepository(session)
        self.packet_repo = PacketRepository(session)

    def check_file_number_integrity(
        self,
        file_number: int,
        code_bar:str
        ):

        self.old_code_bar=""
        packet_number = None
        old_record = None
        new_record = None
        self.status = "allowed"

        candidate = (
            self.candidate_repo
            .get_by_file_number(file_number)
            )

        
        if(candidate == None) :
            return

        
        code_exists = (
            self.code_repo.get_by_file_number(file_number)
        )   

        # --------------------------------------------------------------
        #   check willaya 
        # --------------------------------------------------------------
        new_record  = self.code_format_repo.get_by_code_bar(code_bar=code_bar)
        if not(candidate.willaya_id == new_record.willaya_id ):
            self.status = "willaya_error"
            self.view.display_candidate(
            candidate,"",self.status,"")
            return
        

        if not(code_exists):
            self.status="allowed"
            self.view.display_candidate(
                candidate,self.old_code_bar,self.status,""
                                        )
            return

        for code_ in code_exists:
            print("already exists code bar")
            print(code_.code)
            print(code_.packet_number)
            self.old_code_bar=code_.code
            packet_number =code_.packet_number
            old_record  = self.code_format_repo.get_by_code_bar(code_bar=code_.code)
            new_record  = self.code_format_repo.get_by_code_bar(code_bar=code_bar)
        if(
            old_record.willaya_id==new_record.willaya_id and
            old_record.subject_id==new_record.subject_id ):
                self.status = "edit"    
        else:
                self.status = "forbiden"    
                
        packet_name = self.packet_repo.get_by_id(
            old_record.willaya_id,
            old_record.subject_id,packet_number).name
        self.view.display_candidate(
            candidate,self.old_code_bar,self.status,packet_name
        )        

        

        
        
        


    def load_candidate_by_file_codeBar(
        self,
        code_bar: str
    ):
        res = self.candidate_repo.get_by_barCode(code_bar)
        codeBar = self.code_repo.get_by_code(code_bar)
        pakets = self.packet_repo.get_by_willaya_subject(codeBar.format_willaya_id,codeBar.format_subject_id)
        if len(res) <= 0 :
            self.view.display_candidate(
                None,
                "",
                "empty",
                ""
            )
            return

        res= res[0][0]
        self.view.load_packet_info(pakets)
        # code_exists = (self.code_repo.get_by_file_number(res.file_number))   
        # print(res)
        # print(code_bar)
        # old_record  = self.code_format_repo.get_by_code_bar(code_bar)
        # packet_number =code_exists[0].packet_number
        # packet_name = self.packet_repo.get_by_id(
        # old_record.willaya_id,
        # old_record.subject_id,packet_number).name
        self.view.display_candidate(
                res,
                "",
                "edit",
                ""
            )
        return





    def load_candidates_total(
        self,
        code_bar: str
    ):
        code = self.code_repo.get_by_code(code_bar)
        if(code is None):
            return
        willaya=code.format_willaya_id

        res = self.candidate_repo.get_by_willaya(willaya_id=willaya)
        print(len(res))
        self.view.setTotal(
                len(res),
            )

    def create_packets(
            self,
            code_bar,
            packets_number,
            total_number
    ):
        code = self.code_repo.get_by_code(code_bar)
        willaya=self.willaya_repo.get_by_id(code.format_willaya_id)
        subject=self.subject_repo.get_by_id(code.format_subject_id)
        for i in range(1,packets_number+1):
            if(i<10):
                i = str(f"0{i}")
            else:
                i = str(i)
            name =f"{willaya.willaya}_{subject.subject}{i}"
            print(name)
            res = self.packet_repo.create(
                willaya.id,
                subject.id,
                number=i,
                total_number=total_number,
                name=name
                )
            return res[0]
            
    def assign_packet(self,code_bar: str,file_number: int ):

        code = self.code_repo.get_by_code(code_bar)
        willaya=self.willaya_repo.get_by_id(code.format_willaya_id)
        subject=self.subject_repo.get_by_id(code.format_subject_id)
        print(willaya.id,subject.id)
        packets = self.packet_repo.get_by_willaya_subject(
            willaya.id,
            subject.id
            
            )
        print("----------packets----------")
        print(packets)
        packet  = packets[0]
        code.packet_number = packet.number
        self.code_repo.update(code)
        packet.current_count +=1
        self.packet_repo.update(packet)
        return packet.name

