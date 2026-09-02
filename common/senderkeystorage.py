from sqlalchemy.orm import Session

from database.models import SenderKeyState

class SenderKeyStorage:
    def __init__(self, session: Session):
        self.session = session


    def save(
        self,
        sender: str,
        room_id: str,
        key_id: str,
        chain_key: bytes,
        message_index: int = 0,
    ) -> SenderKeyState:

        state = SenderKeyState(
            sender=sender,
            room_id=room_id,
            key_id=key_id,
            chain_key=chain_key,
            message_index=message_index,
        )

        self.session.add(state)
        self.session.commit()

        return state

    def get(
        self,
        sender: str,
        room_id: str,
        key_id: str,
    ) -> SenderKeyState | None:

        return (
            self.session.query(SenderKeyState)
            .filter_by(
                sender=sender,
                room_id=room_id,
                key_id=key_id,
            )
            .first()
        )

    def update(
        self,
        state: SenderKeyState,
        chain_key: bytes,
        message_index: int,
    ) -> SenderKeyState:

        state.chain_key = chain_key
        state.message_index = message_index

        self.session.commit()

        return state

