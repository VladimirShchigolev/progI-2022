import tkinter

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.models import Product
from src.widgets.products.product_create_window import ProductCreateWindow


class MainWindow(tkinter.Tk):
    def __init__(self, db_engine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_engine = db_engine
        self.geometry("800x600")

        self.title_label = tkinter.Label(self, text="Products", font=("Arial", 32))

        self.product_list = tkinter.Listbox(self, selectmode=tkinter.SINGLE,
                                            width=50, height=15, font=('Arial', 18))
        self.update_product_list()

        self.product_create_button = tkinter.Button(
            self, width=60, height=3, text="Create New Product",
            command=self.open_product_create_window
        )

        self.title_label.pack()
        self.product_list.pack()
        self.product_create_button.pack()

    def update_product_list(self):
        self.product_list.delete(1, self.product_list.size())

        with Session(self.db_engine) as session:
            products = select(Product).order_by(Product.name)
            products = session.scalars(products).all()

        print(products)
        for product in products:
            self.product_list.insert(self.product_list.size()+1, product)

        self.product_list.update()
        self.update()


    def open_product_create_window(self):
        window = ProductCreateWindow(self.db_engine, self)
        window.mainloop()
        self.update_product_list()


