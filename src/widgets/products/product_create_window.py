from tkinter import Toplevel, Label, Entry, StringVar, IntVar, Button, messagebox

from sqlalchemy.orm import Session

from src.models.models import Product


class ProductCreateWindow(Toplevel):
    def __init__(self, db_engine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_engine = db_engine
        self.geometry("800x600")

        self.columnconfigure(0, minsize=60, pad=10)
        self.columnconfigure(1, minsize=60, pad=10)
        for r in range(5):
            self.rowconfigure(r, minsize=20, pad=10)

        self.header = Label(self, text="Create New Product")
        self.header.grid(row=0, column=0, columnspan=2)

        self.name_label = Label(self, text="Name:", width=30)
        self.price_label = Label(self, text="Price:", width=30)
        self.amount_label = Label(self, text="Amount:", width=30)

        self.name_text = StringVar(self)
        self.name_entry = Entry(self, textvariable=self.name_text, width=50)
        self.price_text = StringVar(self)
        self.price_entry = Entry(self, textvariable=self.price_text, width=50)
        self.amount_text = IntVar(self)
        self.amount_entry = Entry(self, textvariable=self.amount_text, width=50)

        self.name_label.grid(row=1, column=0)
        self.price_label.grid(row=2, column=0)
        self.amount_label.grid(row=3, column=0)

        self.name_entry.grid(row=1, column=1)
        self.price_entry.grid(row=2, column=1)
        self.amount_entry.grid(row=3, column=1)

        self.create_button = Button(self, text="Create", width=20,
                                    command=self.create)

        self.cancel_button = Button(self, text="Cancel", width=20,
                                    command=self.close)

        self.create_button.grid(row=4, column=0)
        self.cancel_button.grid(row=4, column=1)

    def create(self):
        name = self.name_text.get()
        price = self.price_text.get()
        amount = self.amount_text.get()
        try:
            valid = Product.validate(name, price, amount, engine=self.db_engine)
        except TypeError as error:
            valid = False
            messagebox.showerror("Error!", error)

        if valid:
            with Session(self.db_engine) as session:
                new_product = Product(name=name, price=float(price), amount=int(amount))
                session.add(new_product)

                session.commit()

            self.close()

    def close(self):
        self.destroy()
        self.quit()
