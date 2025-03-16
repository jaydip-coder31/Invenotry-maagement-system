from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import mysql.connector

class productClass:
    def __init__(self,root):
        self.root=root
        self.root.geometry("1100x500+320+220")
        self.root.title("Inventory Management System | Jaydip Solanki")
        self.root.config(bg="white")
        self.root.resizable(False,False)
        self.root.focus_force()
        #---------------------------------------
        #----------- variables -------------
        self.var_cat=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()
        self.var_pid=StringVar()
        self.var_sup=StringVar()
        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()

        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=480)

        #------------ title --------------
        title=Label(product_Frame,text="Manage Product Details",font=("goudy old style",18),bg="#0f4d7d",fg="white").pack(side=TOP,fill=X)

        lbl_category=Label(product_Frame,text="Category",font=("goudy old style",18),bg="white").place(x=30,y=60)
        lbl_supplier=Label(product_Frame,text="Supplier",font=("goudy old style",18),bg="white").place(x=30,y=110)
        lbl_product_name=Label(product_Frame,text="Name",font=("goudy old style",18),bg="white").place(x=30,y=160)
        lbl_price=Label(product_Frame,text="Price",font=("goudy old style",18),bg="white").place(x=30,y=210)
        lbl_qty=Label(product_Frame,text="Quantity",font=("goudy old style",18),bg="white").place(x=30,y=260)
        lbl_status=Label(product_Frame,text="Status",font=("goudy old style",18),bg="white").place(x=30,y=310)

        cmb_cat=ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_cat.place(x=150,y=60,width=200)
        cmb_cat.current(0)

        cmb_sup=ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_sup.place(x=150,y=110,width=200)
        cmb_sup.current(0)

        txt_name=Entry(product_Frame,textvariable=self.var_name,font=("goudy old style",15),bg="lightyellow").place(x=150,y=160,width=200)
        txt_price=Entry(product_Frame,textvariable=self.var_price,font=("goudy old style",15),bg="lightyellow").place(x=150,y=210,width=200)
        txt_qty=Entry(product_Frame,textvariable=self.var_qty,font=("goudy old style",15),bg="lightyellow").place(x=150,y=260,width=200)

        cmb_status=ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=150,y=310,width=200)
        cmb_status.current(0)

        #-------------- buttons -----------------
        btn_add=Button(product_Frame,text="Save",command=self.add,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_update=Button(product_Frame,text="Update",command=self.update,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_delete=Button(product_Frame,text="Delete",command=self.delete,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_clear=Button(product_Frame,text="Clear",command=self.clear,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)

        #---------- Search Frame -------------
        SearchFrame=LabelFrame(self.root,text="Search Product",font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        #------------ options ----------------
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_search=Entry(SearchFrame,textvariable=self.var_searchtxt,font=("goudy old style",15),bg="lightyellow").place(x=200,y=10)
        btn_search=Button(SearchFrame,text="Search",command=self.search,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #------------ product details -------------
        product_frame=Frame(self.root,bd=3,relief=RIDGE)
        product_frame.place(x=480,y=100,width=600,height=390)

        scrolly=Scrollbar(product_frame,orient=VERTICAL)
        scrollx=Scrollbar(product_frame,orient=HORIZONTAL)\
        
        self.ProductTable=ttk.Treeview(product_frame,columns=("pid","Category","Supplier","name","price","qty","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.ProductTable.xview)
        scrolly.config(command=self.ProductTable.yview)
        self.ProductTable.heading("pid",text="P ID")
        self.ProductTable.heading("Category",text="Category")
        self.ProductTable.heading("Supplier",text="Suppler")
        self.ProductTable.heading("name",text="Name")
        self.ProductTable.heading("price",text="Price")
        self.ProductTable.heading("qty",text="Quantity")
        self.ProductTable.heading("status",text="Status")
        self.ProductTable["show"]="headings"
        self.ProductTable.column("pid",width=90)
        self.ProductTable.column("Category",width=100)
        self.ProductTable.column("Supplier",width=100)
        self.ProductTable.column("name",width=100)
        self.ProductTable.column("price",width=100)
        self.ProductTable.column("qty",width=100)
        self.ProductTable.column("status",width=100)
        
        self.ProductTable.pack(fill=BOTH,expand=1)
        self.ProductTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
        self.fetch_cat_sup()
#-----------------------------------------------------------------------------------------------------
    def fetch_cat_sup(self):
     try:
        
        self.cat_list = ["Empty"]
        self.sup_list = ["Empty"]

        
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jaydip@1234",
            database="ims"
        )
        cur = con.cursor()

        
        cur.execute("SELECT name FROM category")
        cat = cur.fetchall()
        if cat:
            self.cat_list = ["Select"] + [i[0] for i in cat]

        
        cur.execute("SELECT name FROM supplier")
        sup = cur.fetchall()
        if sup:
            self.sup_list = ["Select"] + [i[0] for i in sup]

     except mysql.connector.Error as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

     finally:
        cur.close()
        con.close()

    
    
    def add(self):
     try:
       
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jaydip@1234",
            database="ims"
        )
        cur = con.cursor()

        
        if self.var_cat.get() == "Select" or self.var_cat.get() == "Empty" or self.var_sup.get() == "Select" or self.var_sup.get() == "Empty":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        
        cur.execute("SELECT * FROM product WHERE name = %s", (self.var_name.get(),))
        row = cur.fetchone()

        if row is not None:
            messagebox.showerror("Error", "Product already present", parent=self.root)
        else:
            
            cur.execute("""
                INSERT INTO product (Category, Supplier, name, price, qty, status) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                self.var_cat.get(),
                self.var_sup.get(),
                self.var_name.get(),
                self.var_price.get(),
                self.var_qty.get(),
                self.var_status.get(),
            ))

            con.commit()
            messagebox.showinfo("Success", "Product Added Successfully", parent=self.root)
            self.clear()
            self.show()

     except mysql.connector.Error as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

     finally:
        cur.close()
        con.close()
     
    def show(self):
     try:
       
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jaydip@1234",
            database="ims"
        )
        cur = con.cursor()

       
        cur.execute("SELECT * FROM product")
        rows = cur.fetchall()

       
        self.ProductTable.delete(*self.ProductTable.get_children())
        for row in rows:
            self.ProductTable.insert('', END, values=row)

     except mysql.connector.Error as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

     finally:
        cur.close()
        con.close()


    def get_data(self,ev):
        f=self.ProductTable.focus()
        content=(self.ProductTable.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[1])
        self.var_sup.set(row[2])
        self.var_name.set(row[3])
        self.var_price.set(row[4])
        self.var_qty.set(row[5])
        self.var_status.set(row[6])

    def update(self):
     try:
       
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jaydip@1234",
            database="ims"
        )
        cur = con.cursor()

       
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Please select a product from the list", parent=self.root)
            return

        
        cur.execute("SELECT * FROM product WHERE pid = %s", (self.var_pid.get(),))
        row = cur.fetchone()

        if row is None:
            messagebox.showerror("Error", "Invalid Product", parent=self.root)
        else:
            
            cur.execute("""
                UPDATE product 
                SET Category = %s, Supplier = %s, name = %s, price = %s, qty = %s, status = %s 
                WHERE pid = %s
            """, (
                self.var_cat.get(),
                self.var_sup.get(),
                self.var_name.get(),
                self.var_price.get(),
                self.var_qty.get(),
                self.var_status.get(),
                self.var_pid.get(),
            ))

            con.commit()
            messagebox.showinfo("Success", "Product Updated Successfully", parent=self.root)
            self.show()

     except mysql.connector.Error as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

     finally:
        cur.close()
        con.close()
    def delete(self):
     try:
        
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jaydip@1234",
            database="ims"
        )
        cur = con.cursor()

        
        if self.var_pid.get() == "":
            messagebox.showerror("Error", "Select a product from the list", parent=self.root)
            return

        
        cur.execute("SELECT * FROM product WHERE pid = %s", (self.var_pid.get(),))
        row = cur.fetchone()

        if row is None:
            messagebox.showerror("Error", "Invalid Product", parent=self.root)
        else:
            op = messagebox.askyesno("Confirm", "Do you really want to delete?", parent=self.root)
            if op:
                
                cur.execute("DELETE FROM product WHERE pid = %s", (self.var_pid.get(),))
                con.commit()
                messagebox.showinfo("Delete", "Product Deleted Successfully", parent=self.root)
                self.clear() 
     except mysql.connector.Error as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

     finally:
        cur.close()
        con.close()

    def clear(self):
        self.var_cat.set("Select")
        self.var_sup.set("Select")
        self.var_name.set("")
        self.var_price.set("")
        self.var_qty.set("")
        self.var_status.set("Active")
        self.var_pid.set("")
        self.var_searchby.set("Select")
        self.var_searchtxt.set("")
        self.show()

    
    def search(self):
     try:
        
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jaydip@1234",
            database="ims"
        )
        cur = con.cursor()

        
        if self.var_searchby.get() == "Select":
            messagebox.showerror("Error", "Select Search By option", parent=self.root)
            return

        
        if self.var_searchtxt.get() == "":
            messagebox.showerror("Error", "Search input should be required", parent=self.root)
            return

       
        query = f"SELECT * FROM product WHERE {self.var_searchby.get()} LIKE %s"
        search_value = "%" + self.var_searchtxt.get() + "%"
        cur.execute(query, (search_value,))

        rows = cur.fetchall()

        if rows:
            self.ProductTable.delete(*self.ProductTable.get_children())
            for row in rows:
                self.ProductTable.insert('', END, values=row)
        else:
            messagebox.showerror("Error", "No record found!!!", parent=self.root)

     except mysql.connector.Error as ex:
        messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

     finally:
        cur.close()
        con.close()
 

if __name__=="__main__":
    root=Tk()
    obj=productClass(root)
    root.mainloop()