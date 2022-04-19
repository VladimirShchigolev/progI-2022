import tkinter

from src.widgets.products.product_create_window import ProductCreateWindow


class MainWindow(tkinter.Tk):
    def __init__(self, db_engine, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_engine = db_engine
        self.geometry("800x600")

        self.product_create_button = tkinter.Button(
            self, width=60, height=3, text="Create New Product",
            command=self.open_product_create_window
        )
        self.product_create_button.pack()

    def open_product_create_window(self):
        window = ProductCreateWindow(self.db_engine, self)
        window.mainloop()

