from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from src.models.models import Client
from src.widgets.main_window import MainWindow


def main():
    engine = create_engine("sqlite:///db.sqlite", echo=False, future=True)

    with Session(engine) as session:
        clients = select(Client)

        for client in session.scalars(clients):
            print(client)

    main_window = MainWindow(engine)
    main_window.mainloop()


if __name__ == "__main__":
    main()
