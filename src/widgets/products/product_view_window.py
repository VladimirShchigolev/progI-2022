import tkinter
from tkinter import Toplevel, Label, Entry, StringVar, Button

from sqlalchemy.orm import Session

from src.widgets.products.product_edit_window import ProductEditWindow


class ProductViewWindow(Toplevel):
    def __init__(self, db_engine, product, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_engine = db_engine
        self.product = product
        self.geometry("800x600")

        self.columnconfigure(0, minsize=60, pad=10)
        self.columnconfigure(1, minsize=60, pad=10)
        for r in range(5):
            self.rowconfigure(r, minsize=20, pad=10)

        self.header = Label(self, text="View Product")
        self.header.grid(row=0, column=0, columnspan=2)

        self.name_label = Label(self, text="Name:", width=30)
        self.price_label = Label(self, text="Price:", width=30)
        self.amount_label = Label(self, text="Amount:", width=30)

        self.name_text = StringVar()
        self.name_text.set(self.product.name)
        self.name_entry = Entry(self, state=tkinter.DISABLED, textvariable=self.name_text, width=50)

        self.price_text = StringVar()
        self.price_text.set(str(self.product.price))
        self.price_entry = Entry(self, state=tkinter.DISABLED, textvariable=self.price_text, width=50)

        self.amount_text = StringVar()
        self.amount_text.set(str(self.product.amount))
        self.amount_entry = Entry(self, state=tkinter.DISABLED, textvariable=self.amount_text, width=50)

        self.name_label.grid(row=1, column=0)
        self.price_label.grid(row=2, column=0)
        self.amount_label.grid(row=3, column=0)

        self.name_entry.grid(row=1, column=1)
        self.price_entry.grid(row=2, column=1)
        self.amount_entry.grid(row=3, column=1)

        self.edit_button = Button(self, text="Edit", width=20,
                                  command=self.open_product_edit_window)

        self.delete_button = Button(self, text="Delete", width=20,
                                    command=self.delete_product)

        self.back_button = Button(self, text="Back", width=20,
                                  command=self.close)

        self.edit_button.grid(row=4, column=0)
        self.delete_button.grid(row=5, column=0)
        self.back_button.grid(row=4, column=1)

    def delete_product(self):
        with Session(self.db_engine) as session:
            session.delete(self.product)
            session.commit()

        self.master.update_product_list()
        self.close()

    def open_product_edit_window(self):
        window = ProductEditWindow(self.db_engine, self.product, self.master)
        self.close()
        window.mainloop()

    def close(self):
        self.destroy()
        self.quit()
