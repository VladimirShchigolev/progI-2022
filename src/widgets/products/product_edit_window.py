from tkinter import Toplevel, Label, Entry, StringVar, IntVar, Button, messagebox

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.models import Product
import src.widgets.products.product_view_window


class ProductEditWindow(Toplevel):
    def __init__(self, db_engine, product, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_engine = db_engine
        self.product = product
        self.geometry("800x600")

        self.columnconfigure(0, minsize=60, pad=10)
        self.columnconfigure(1, minsize=60, pad=10)
        for r in range(5):
            self.rowconfigure(r, minsize=20, pad=10)

        self.header = Label(self, text="Edit Product")
        self.header.grid(row=0, column=0, columnspan=2)

        self.name_label = Label(self, text="Name:", width=30)
        self.price_label = Label(self, text="Price:", width=30)
        self.amount_label = Label(self, text="Amount:", width=30)

        self.name_text = StringVar(self)
        self.name_text.set(self.product.name)
        self.name_entry = Entry(self, textvariable=self.name_text, width=50)

        self.price_text = StringVar(self)
        self.price_text.set(str(self.product.price))
        self.price_entry = Entry(self, textvariable=self.price_text, width=50)

        self.amount_text = IntVar(self)
        self.amount_text.set(self.product.amount)
        self.amount_entry = Entry(self, textvariable=self.amount_text, width=50)

        self.name_label.grid(row=1, column=0)
        self.price_label.grid(row=2, column=0)
        self.amount_label.grid(row=3, column=0)

        self.name_entry.grid(row=1, column=1)
        self.price_entry.grid(row=2, column=1)
        self.amount_entry.grid(row=3, column=1)

        self.save_button = Button(self, text="Save", width=20,
                                  command=self.save)

        self.cancel_button = Button(self, text="Cancel", width=20,
                                    command=self.close)

        self.save_button.grid(row=4, column=0)
        self.cancel_button.grid(row=4, column=1)

    def save(self):
        name = self.name_text.get()
        price = self.price_text.get()
        amount = self.amount_text.get()

        if name != self.product.name:
            used_engine = self.db_engine
        else:
            used_engine = None

        try:
            valid = Product.validate(name, price, amount, engine=used_engine)
        except TypeError as error:
            valid = False
            messagebox.showerror("Error!", error)

        if valid:
            with Session(self.db_engine) as session:
                edited_product = select(Product).where(Product.name == self.product.name)
                edited_product = session.scalars(edited_product).one()

                edited_product.name = name
                edited_product.price = price
                edited_product.amount = amount

                session.commit()

                product = select(Product).where(Product.name == name)
                product = session.scalars(product).one()

            self.close()
            self.master.update_product_list()
            window = src.widgets.products.product_view_window.ProductViewWindow(self.db_engine, product, self.master)
            window.mainloop()

    def close(self):
        self.destroy()
        self.quit()
