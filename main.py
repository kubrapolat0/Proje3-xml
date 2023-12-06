from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import xml.etree.ElementTree as ET

class BookViewer:
    def __init__(self, master):
        self.master = master
        self.master.title("ZÜLFÜ LİVANELİ KİTAPLARI")
        self.master.geometry("500x700")

        self.navigasyon = 0
        self.books = self.load_books_from_xml("veriseti.xml")

        self.forward_button = Button(self.master, text="İleri", command=self.go_forward, width=15, height=2)
        self.forward_button.grid(row=0, column=1, pady=20)

        self.backward_button = Button(self.master, text="Geri", command=self.go_backward, width=15, height=2)
        self.backward_button.grid(row=0, column=0, pady=20)

        self.image_label = Label(self.master)
        self.image_label.grid(row=1, column=0, columnspan=2, pady=20)

        self.show_details_button = Button(self.master, text="Detayları Göster", command=self.show_details, width=30, height=2)
        self.show_details_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.show_other_books_button = Button(self.master, text="Diğer Kitapları", command=self.show_other_books, width=30, height=2)
        self.show_other_books_button.grid(row=3, column=0, columnspan=2, pady=20)

        self.load_book_data(self.navigasyon)

    def load_books_from_xml(self, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        books = []

        for book_elem in root.findall("kitap"):
            title = book_elem.find("baslik").text
            author = book_elem.find("yazar").text
            image_path = book_elem.find("resim").text
            release_date = book_elem.find("yayin_tarihi").text
            language = book_elem.find("dil").text

            books.append({"title": title, "author": author, "image_path": image_path,
                          "release_date": release_date, "language": language})

        return books

    def load_book_data(self, index):
        if 0 <= index < len(self.books):
            book = self.books[index]
            image = Image.open(book["image_path"])
            image = image.resize((300, 400), Image.BICUBIC)
            photo = ImageTk.PhotoImage(image)

            self.image_label.config(image=photo)
            self.image_label.image = photo
        else:
            print("Geçersiz index")

    def go_forward(self):
        self.navigasyon += 1
        if self.navigasyon >= len(self.books):
            self.navigasyon = 0
        self.load_book_data(self.navigasyon)

    def go_backward(self):
        self.navigasyon -= 1
        if self.navigasyon < 0:
            self.navigasyon = len(self.books) - 1
        self.load_book_data(self.navigasyon)

    def show_details(self):
        if 0 <= self.navigasyon < len(self.books):
            book = self.books[self.navigasyon]
            details = f"Kitap adı: {book['title']}\nYazar: {book['author']}\nYayın Tarihi: {book['release_date']}\nDil: {book['language']}"
            messagebox.showinfo("Kitap Detayları", details)
        else:
            print("Geçersiz index")

    def show_other_books(self):
        other_books = "\n".join([book['title'] for book in self.books])
        messagebox.showinfo("Diğer Kitaplar", other_books)

if __name__ == "__main__":
    root = Tk()
    app = BookViewer(root)
    root.mainloop()

