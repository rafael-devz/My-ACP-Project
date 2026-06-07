from customtkinter import *
from tkinter import messagebox, ttk
from PIL import Image
from datetime import datetime
import textwrap

# COLOR DESIGN SECTION
ocean_blue = "#286FB3"
sky_blue = "#3399FF"
midnight_navy = "#1F2A44"
warm_golden_orange = "#FDB44B"
dark_golden = "#E68600"
window_bg_light = "#B3E5FC"
white_blue = "#E1F5FE"
color_light = "#FFF"
color_dark = "#000"
light_gray = "#D8D8D8"
muted_gray = "#737373"
charcoal_gray = "#4C4C4C"
error_color = "#FF0000"
dark_error = "#DB0000"
success_color = "#008000"

# File Paths
users_file = "AD_comprog/sem_proj/data/acc.txt"
product_file = "AD_comprog/sem_proj/data/product.txt"
img_folder = "AD_comprog/sem_proj/img/"
orders_file = "AD_comprog/sem_proj/data/orders.txt"
receipt_file = "AD_comprog/sem_proj/data/receipts.txt"

cart = {} # Storage for all items in cart
current_user = {
    "username" : "",
    "email" : "",
    "contact" : ""
}
cart_count_label = None
main_win = None
page_switcher = None

# Helper to clear page content
def clear_content(parent):
    for widget in parent.winfo_children():
        widget.destroy()

# Opening product.txt
def open_product_file():
    products = []

    with open(product_file, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            category, name, price, img = line.split(", ")

            products.append({
                "category": category,
                "name": name,
                "price": int(price),
                "img": img
            })

    return products

# -----------------------------------------------------------------------------------------------

# Function for adding product in cart
def add_to_cart(product_name, price):
    if product_name in cart:
        cart[product_name]["qty"] += 1
    else:
        cart[product_name] = {"qty" : 1, "price" : price}
        
    messagebox.showinfo("Cart", f"{product_name} is added to cart!")
    
    if cart_count_label:
        total_qty = 0
        for details in cart.values():
            total_qty += details["qty"]
        cart_count_label.configure(text=f"Cart ({total_qty})")
    
# Function for getting the product by using their names
def get_product(product_name, price):
    def add():
        add_to_cart(product_name, price)
    return add

# Make a menu function
def build_menu(parent_frame, products, category, limit=None):
    categ_product = []
    for product in products:
        if product["category"] == category:
            categ_product.append(product)
            
    if limit is not None:
        categ_product = categ_product[:limit]

    # Section container
    menu_container = CTkFrame(parent_frame, fg_color="transparent")
    menu_container.pack(pady=10, fill="x", expand=True)

    # Section Header
    CTkLabel(menu_container, text=f"{category.title()}s", font=("Helvetica", 25, "bold"), text_color=color_dark).grid(row=0, column=0, pady=5)
    CTkFrame(menu_container, width=100, height=3, fg_color=warm_golden_orange).grid(row=1, column=0)
    
    # Product grid
    product_container = CTkFrame(menu_container, fg_color="transparent")
    product_container.grid(row=2, column=0, pady=10, sticky="nsew")
    
    columns = 3
    for index, product in enumerate(categ_product):
        row = index // columns
        col = index % columns
        
        # Product card
        display_container = CTkFrame(
            product_container,
            width=200,
            height=200,
            fg_color=color_light,
            border_color=charcoal_gray,
            border_width=2
        )
        display_container.grid(row=row, column=col, padx=10, pady=10)
        display_container.pack_propagate(False)
    
        # Product img
        img = CTkImage(light_image=Image.open(img_folder + product["img"]), size=(110, 100))
        CTkLabel(display_container, image=img, text="").pack(pady=(15, 5))
        
        # Product name
        CTkLabel(display_container, text=product["name"], font=("Helvetica", 12, "bold"), text_color=color_dark, wraplength=180).pack()
        
        # Product price
        CTkLabel(display_container, text=f"₱{product['price']}", font=("Helvetica", 15, "bold"), text_color=muted_gray).place(x=30, y=160)
        
        # Add to cart btn
        add_btn = CTkButton(
            display_container,
            text="Add to cart",
            fg_color=warm_golden_orange,
            hover_color=dark_golden,
            width=70,
            height=30,
            font=("Helvetica", 12, "bold"),
            command=get_product(product["name"], product["price"])
        )
        add_btn.place(x=100, y=160)

# Footer function
def footer(root):
    footer_frame = CTkFrame(root, width=1200, height=350, fg_color=window_bg_light, corner_radius=0)
    footer_frame.pack(fill="x", pady=(30, 0))
    
    CTkLabel(footer_frame, text="Grill Bite", font=("Helvetica", 50, "bold"), text_color=color_dark).place(x=485, y=30)
    
    footer_info_frame = CTkFrame(footer_frame, fg_color="transparent", width=600, height=150)
    footer_info_frame.place(x=265, y=130)
    
    info1_frame = CTkFrame(footer_info_frame, fg_color="transparent", height=200)
    info1_frame.grid(row=0, column=0, pady=10, padx=20)
    
    CTkLabel(info1_frame, text="Get In Touch", font=("Helvetica", 20, "bold"), text_color=color_dark).pack(pady=10, padx=10, anchor="e")
    CTkLabel(info1_frame, text="Lumbangan, Nasugbu, Batangas", font=("Helvetica", 15), text_color=color_dark).pack(padx=10, anchor="e")
    CTkLabel(info1_frame, text="0912-345-6789", font=("Helvetica", 15), text_color=color_dark).pack(padx=10, anchor="e")
    
    border_frame = CTkFrame(footer_info_frame, fg_color=color_dark, width=2, height=100)
    border_frame.grid(row=0, column=1, padx=50, pady=10)
    
    info2_frame = CTkFrame(footer_info_frame, fg_color="transparent", width=200, height=200)
    info2_frame.grid(row=0, column=2, pady=10, padx=20)
    
    CTkLabel(info2_frame, text="Opening Hours", font=("Helvetica", 20, "bold"), text_color=color_dark).pack(pady=10, padx=10, anchor="w")
    CTkLabel(info2_frame, text="Mon - Fri, at 8AM - 6PM", font=("Helvetica", 15), text_color=color_dark).pack(padx=10, anchor="w")
    CTkLabel(info2_frame, text="Sat and Sun: Closed", font=("Helvetica", 15), text_color=color_dark).pack(padx=10, anchor="w")
    
    CTkLabel(footer_frame, text="©️ Grill Bite. All Right Reserved. Designed by John Rafael B. Ortega",
            text_color=color_dark).place(x=380, y=300)

# -----------------------------------------------------------------------------------------------

# Navigation function
def navigation(root, window):
    nav_frame = CTkFrame(window, width=1200, height=60, corner_radius=0, fg_color=white_blue)
    nav_frame.pack(side=TOP, fill="x")
    
    CTkLabel(nav_frame, text="Grill Bite", font=("Helvetica", 25, "bold"), text_color=sky_blue).place(x=15, y=15)
    
    def make_nav(page):
        def goto_nav():
            if page_switcher:
                page_switcher(page)
        return goto_nav
            
    # Home Nav
    nav_home = CTkButton(
        nav_frame, 
        text="Home",
        width=60, 
        font=("Helvetica", 15), 
        text_color=color_dark, 
        fg_color="transparent", 
        hover=False, 
        command=make_nav("home"))
    nav_home.place(x=669, y=15)
    
    # About Nav
    nav_about = CTkButton(
        nav_frame, 
        text="About", 
        width=60, 
        font=("Helvetica", 15), 
        text_color=color_dark, 
        fg_color="transparent", 
        hover=False, 
        command=make_nav("about"))
    nav_about.place(x=746, y=15)
    
    # Menu Nav
    nav_menu = CTkButton(
        nav_frame, 
        text="Menu",
        width=60, 
        font=("Helvetica", 15), 
        text_color=color_dark, 
        fg_color="transparent", 
        hover=False, 
        command=make_nav("menu"))
    nav_menu.place(x=821, y=15)
    
    # History Nav
    nav_gallery = CTkButton(
        nav_frame, 
        text="History", 
        width=60, 
        font=("Helvetica", 15), 
        text_color=color_dark, 
        fg_color="transparent", 
        hover=False, 
        command=make_nav("history"))
    nav_gallery.place(x=900, y=15)
    
    # View cart function
    def open_viewcart_win():
        viewcart_win = CTkToplevel(window)
        viewcart_win.title("Cart")
        viewcart_win.geometry("500x600")
        viewcart_win.resizable(False, False)
        viewcart_win.grab_set()
        viewcart_win.configure(fg_color=color_light)
        
        cart_label_frame = CTkFrame(viewcart_win, fg_color=window_bg_light, height=60, corner_radius=0)
        cart_label_frame.pack(fill="x")
        CTkLabel(cart_label_frame, text="Your Cart", text_color=color_dark, font=("Helvetica", 25, "bold")).pack(pady=10)
        
        cart_order_frame = CTkScrollableFrame(viewcart_win, height=400, fg_color=color_light)
        cart_order_frame.pack(fill="x", pady=10, padx=10)
        
        total_label = CTkLabel(viewcart_win, text="Total: ₱0", text_color=color_dark, font=("Helvetica", 15, "bold"))
        total_label.pack(pady=10)
        
        cart_btn_frame = CTkFrame(viewcart_win, width=500, fg_color="transparent", corner_radius=0)
        cart_btn_frame.pack()
        
# -----------------------------------------------------------------------------------------------
        
        # Checkout funtion
        def open_checkout_win():
            checkout_win = CTkToplevel(window)
            checkout_win.title("Checkout")
            checkout_win.geometry("500x500")
            checkout_win.resizable(False, False)
            checkout_win.grab_set()
            checkout_win.configure(fg_color=color_light)
            
            # Title label with frame
            checkout_label_frame = CTkFrame(checkout_win, fg_color=window_bg_light, height=60, corner_radius=0)
            checkout_label_frame.pack(fill="x")
            CTkLabel(checkout_label_frame, text="Checkout", text_color=color_dark, font=("Helvetica", 25, "bold")).pack(pady=10)
            
            # Checkout main frame
            checkout_main_frame = CTkScrollableFrame(checkout_win, height=350, fg_color=color_light)
            checkout_main_frame.pack(fill="x")
            
            # Information frame
            customer_info_frame = CTkFrame(checkout_main_frame, fg_color=color_light)
            customer_info_frame.pack(fill="x")
            
            CTkLabel(
                customer_info_frame, 
                text="Customer Information", 
                font=("Helvetica", 15, "bold"), 
                text_color=color_dark
                ).grid(row=0, column=0, pady=10, padx=10, sticky="w")
            
            # Customer info
            CTkLabel(
                customer_info_frame,
                text=f"Name: {current_user['username']}",
                font=("Helvetica", 12),
                text_color=color_dark
            ).grid(row=1, column=0, padx=10, sticky="w")
            
            CTkLabel(
                customer_info_frame,
                text=f"Email: {current_user['email']}",
                font=("Helvetica", 12),
                text_color=color_dark
            ).grid(row=2, column=0, padx=10, sticky="w")
            
            CTkLabel(
                customer_info_frame,
                text=f"Contact: {current_user['contact']}",
                font=("Helvetica", 12),
                text_color=color_dark
            ).grid(row=3, column=0, padx=10, sticky="w")
            
            # Order Summary Frame
            order_summary_frame = CTkFrame(checkout_main_frame, fg_color=color_light)
            order_summary_frame.pack(fill="x")
            
            CTkLabel(
                order_summary_frame, 
                text="Order Summary",
                font=("Helvetica", 15, "bold"),
                text_color=color_dark
            ).grid(row=0, column=0, pady=10, padx=10, sticky="w")
            
            total = 0
            for index, (product, details) in enumerate(cart.items(), start=1):
                qty = details["qty"]
                price = details["price"]
                subtotal = price * qty
                total += subtotal
                
                CTkLabel(
                    order_summary_frame,
                    text=f"{qty} x {product} = ₱{subtotal}",
                    font=("Helvetica", 12),
                    text_color=color_dark 
                    ).grid(row=index, column=0, padx=10, sticky="w")
                
            CTkLabel(
                order_summary_frame, 
                text=f"Total: {total}", 
                font=("Helvetica", 13, "bold"), 
                text_color=color_dark
                ).grid(row=len(cart)+1, column=0, padx=10, pady=5, sticky="w")
            
            # Payment Method
            payment_frame = CTkFrame(checkout_main_frame, fg_color=color_light)
            payment_frame.pack(fill="x")
            
            CTkLabel(payment_frame, text="Payment Method", font=("Helvetica", 15, "bold"), text_color=color_dark).grid(row=0, column=0, padx=10, pady=10, sticky="w")
            
            payment_method = StringVar(value="")
            
            def show_payment():
                cod_frame.pack_forget()
                gcash_frame.pack_forget()
                bank_frame.pack_forget()
                
                selected = payment_method.get()
                payment_info_frames.configure(height=0)
                
                if selected == "COD":
                    payment_info_frames.configure(height=130)
                    cod_frame.pack(padx=10, pady=10, anchor="w")
                    
                elif selected == "Gcash":
                    payment_info_frames.configure(height=150)
                    gcash_frame.pack(padx=10, pady=10, anchor="w")
                    
                elif selected == "Bank":
                    payment_info_frames.configure(height=120)
                    bank_frame.pack(padx=10, pady=10, anchor="w")
            
            
            CTkRadioButton(
                payment_frame,
                text="Cash on Delivery",
                variable=payment_method,
                value="COD",
                radiobutton_width=15,
                radiobutton_height=15,
                border_color=charcoal_gray,
                border_width_checked=5,
                border_width_unchecked=3,
                fg_color=charcoal_gray,
                font=("Helvetica", 12),
                text_color=color_dark,
                command=show_payment
            ).grid(row=1, column=0, padx=10, pady=5, sticky="w")
            
            CTkRadioButton(
                payment_frame,
                text="Gcash",
                variable=payment_method,
                value="Gcash",
                radiobutton_width=15,
                radiobutton_height=15,
                border_color=charcoal_gray,
                border_width_checked=5,
                border_width_unchecked=3,
                fg_color=charcoal_gray,
                font=("Helvetica", 12),
                text_color=color_dark,
                command=show_payment
            ).grid(row=1, column=1, pady=5, padx=10, sticky="w")
            
            CTkRadioButton(
                payment_frame,
                text="Bank Transfer",
                variable=payment_method,
                value="Bank",
                radiobutton_width=15,
                radiobutton_height=15,
                border_color=charcoal_gray,
                border_width_checked=5,
                border_width_unchecked=3,
                fg_color=charcoal_gray,
                font=("Helvetica", 12),
                text_color=color_dark,
                command=show_payment
            ).grid(row=1, column=2, padx=10, pady=5, sticky="w")
            
            payment_info_frames = CTkFrame(payment_frame, fg_color=color_light, height=0)
            payment_info_frames.grid(row=2, column=0, columnspan=3, sticky="w")
            payment_info_frames.grid_propagate(False)
            
            # COD Frame
            cod_frame = CTkFrame(payment_info_frames, fg_color=color_light)
            
            CTkLabel(cod_frame, text="Delivery Address", font=("Helvetica", 13, "bold"),text_color=color_dark).pack(pady=10, anchor="w")
            
            customer_address = CTkEntry(
                cod_frame,
                placeholder_text="Enter your address",
                placeholder_text_color=muted_gray,
                width=200,
                height=25,
                fg_color=light_gray,
                border_color=charcoal_gray,
                text_color=muted_gray
            )
            customer_address.pack(pady=(0, 10), anchor="w")
            
            CTkLabel(
                cod_frame, 
                text="Please prepare the exact amount.\nOur rider will contact you before delivery", 
                font=("Helvetica", 12), 
                text_color=color_dark,
                justify="left"
                ).pack(anchor="w")
            
            # Gcash Frame
            gcash_frame = CTkFrame(payment_info_frames, fg_color=color_light)
            
            CTkLabel(gcash_frame, text="GCash Mobile Number", font=("Helvetica", 13, "bold"), text_color=color_dark).pack(pady=(5, 2), anchor="w")
            gcash_entry = CTkEntry(
                gcash_frame,
                placeholder_text="09*********",
                placeholder_text_color=muted_gray,
                width=200,
                height=25,
                fg_color=light_gray,
                border_color=charcoal_gray,
                font=("Helvetica", 12),
                text_color=muted_gray
            )
            gcash_entry.pack(pady=(0, 10), anchor="w")
            
            CTkLabel(gcash_frame, text="Payment Amount", font=("Helvetica", 13, "bold"), text_color=color_dark).pack(pady=(5, 2), anchor="w")
            gcash_amount_entry = CTkEntry(
                gcash_frame,
                placeholder_text="Enter the amount",
                placeholder_text_color=muted_gray,
                width=200,
                height=25,
                fg_color=light_gray,
                border_color=charcoal_gray,
                font=("Helvetica", 12),
                text_color=muted_gray
                )
            gcash_amount_entry.pack(anchor="w")
            
            # Bank Frame
            bank_frame = CTkFrame(payment_info_frames, fg_color=color_light)
            
            CTkLabel(bank_frame, text="Bank Account Number", font=("Helvetica", 12), text_color=color_dark).pack(pady=5, anchor="w")
            
            bank_entry = CTkEntry(
                bank_frame,
                placeholder_text="1234 5678 9101 1121",
                placeholder_text_color=muted_gray,
                width=200,
                height=25,
                fg_color=light_gray,
                border_color=charcoal_gray,
                font=("Helvetica", 12),
                text_color=muted_gray
            )
            bank_entry.pack(pady=(0, 5), anchor="w")
            
            CTkLabel(bank_frame, text="Payment Amount", font=("Helvetica", 13, "bold"), text_color=color_dark).pack(pady=(5, 2), anchor="w")
            bank_amount_entry = CTkEntry(
                bank_frame,
                placeholder_text="Enter the amount",
                placeholder_text_color=muted_gray,
                width=200,
                height=25,
                fg_color=light_gray,
                border_color=charcoal_gray,
                font=("Helvetica", 12),
                text_color=muted_gray
            )
            bank_amount_entry.pack(anchor="w")
            
            # Not show all the frame
            cod_frame.pack_forget()
            gcash_frame.pack_forget()
            bank_frame.pack_forget()
            
            checkout_btn_frame = CTkFrame(checkout_win, width=500, fg_color="transparent", corner_radius=0)
            checkout_btn_frame.pack(pady=15)
            
            # Checkout confirm order function
            def confirm_order():
                cart_total = 0
                for details in cart.values():
                    cart_total += details["qty"] * details["price"]
                    
                selected = payment_method.get()
                
                if selected == "":
                    messagebox.showerror("Error", "Please select your payment.")
                    return
                
                # COD Validation
                if selected == "COD":
                    address = customer_address.get()
                    
                    if address == "":
                        messagebox.showerror("Error", "You must input your address.")
                        customer_address.configure(border_color=error_color)
                        customer_address.focus_set()
                        return
                    else:
                        customer_address.configure(border_color=charcoal_gray)
                
                # Gcash validations
                elif selected == "Gcash":
                    gcash = gcash_entry.get()
                    
                    if gcash == "":
                        messagebox.showerror("Error", "You must input your gcash number.")
                        gcash_entry.configure(border_color=error_color)
                        gcash_entry.focus_set()
                        return
                    else:
                        gcash_entry.configure(border_color=charcoal_gray)
                        
                    if not gcash.isdigit():
                        messagebox.showerror("Error", "GCash number must contain digits only.")
                        gcash_entry.configure(border_color=error_color)
                        gcash_entry.focus_set()
                        return
                    
                    if len(gcash) != 11:
                        messagebox.showerror("Error", "Gcash number must be 11 digits.")
                        gcash_entry.configure(border_color=error_color)
                        gcash_entry.focus_set()
                        return
                    else:
                        gcash_entry.configure(border_color=charcoal_gray)
                        
                    # Amount validation
                    if gcash_amount_entry.get() == "":
                        messagebox.showerror("Error", "You must input the amount of money")
                        gcash_amount_entry.configure(border_color=error_color)
                        gcash_amount_entry.focus_set()
                        return
                    else:
                        gcash_amount_entry.configure(border_color=charcoal_gray)
                        
                    if not gcash_amount_entry.get().isdigit():
                        messagebox.showerror("Error", "Amount must be digits only.")
                        gcash_amount_entry.configure(border_color=error_color)
                        gcash_amount_entry.focus_set()
                        return
                        
                    if int(gcash_amount_entry.get()) != cart_total:
                        messagebox.showerror("Amount Error", "Invalid amount. Please enter the correct amount for payment")
                        gcash_amount_entry.configure(border_color=error_color)
                        gcash_amount_entry.focus_set()
                        return
                    
                # Bank Validations
                elif selected == "Bank":
                    bank = bank_entry.get().replace(" ", "")
                    
                    if bank == "":
                        messagebox.showerror("Error", "You must input your account number.")
                        bank_entry.configure(border_color=error_color)
                        bank_entry.focus_set()
                        return
                    else:
                        bank_entry.configure(border_color=charcoal_gray)
                        
                    if not bank.isdigit():
                        messagebox.showerror("Error", "Account number must contain digits only.")
                        bank_entry.configure(border_color=error_color)
                        bank_entry.focus_set()
                        return
                        
                    if len(bank) != 16:
                        messagebox.showerror("Error", "Account number must be 16 digits.")
                        bank_entry.configure(border_color=error_color)
                        bank_entry.focus_set()
                        return
                    else:
                        bank_entry.configure(border_color=charcoal_gray)
                        
                    # Amount Validation
                    if bank_amount_entry.get() == "":
                        messagebox.showerror("Error", "You must input the amount of money")
                        bank_amount_entry.configure(border_color=error_color)
                        bank_amount_entry.focus_set()
                        return
                    else:
                        bank_amount_entry.configure(border_color=charcoal_gray)
                        
                    if not bank_amount_entry.get().isdigit():
                        messagebox.showerror("Error", "Amount must be digits only.")
                        bank_amount_entry.configure(border_color=error_color)
                        bank_amount_entry.focus_set()
                        return
                        
                    if int(bank_amount_entry.get()) != cart_total:
                        messagebox.showerror("Amount Error", "Invalid amount. Please enter the correct amount for payment")
                        bank_amount_entry.configure(border_color=error_color)
                        bank_amount_entry.focus_set()
                        return
                        
                date_time = datetime.now().strftime("%Y-%m-%d %H:%M %p")
                items_list = []
                total = 0
                total_qty = 0
                
                for product, details in cart.items():
                    qty = details["qty"]
                    price = details["price"]
                    subtotal = qty * price
                    total += subtotal
                    total_qty += qty
                    
                    items_list.append(f"{qty} x {product}")
                items = " | ".join(items_list)
                
                with open(orders_file, "a") as file:
                    file.write(f"{date_time}, {current_user['username']}, {selected}, {total_qty}, {items}, {total}\n")

                # receipt
                payment_info = ""
                
                if selected == "COD":
                    payment_info = customer_address.get()
                elif selected == "Gcash":
                    payment_info = gcash_entry.get()
                elif selected == "Bank":
                    payment_info = bank_entry.get()
                    
                messagebox.showinfo(
                    "Receipt",
                    textwrap.dedent(f"""
                    =============== Receipt ===============\n
                    ----- Personal Informations -----
                    Date/Time: {date_time}
                    Customer: {current_user['username']}
                    Contact: {current_user['contact']}
                    
                    ----- Items Ordered -----
                    Items: {items}
                    Payment: {selected}
                    Payment Info: {payment_info}
                    
                    ----- Totals -----
                    Total QTY: {total_qty}
                    Overall Total: ₱{total}
                    
                    Thank you, {current_user['username']}!
                    
                    ==================================
                    """
                ))

                with open(receipt_file, "a") as file:
                    file.write("----------------------------------------\n")
                    file.write(f"Date/Time: {date_time}\n")
                    file.write(f"Customer: {current_user['username']}\n")
                    file.write(f"Email: {current_user['email']}\n")
                    file.write(f"Contact: {current_user['contact']}\n")
                    file.write(f"Payment Method: {selected}\n")
                    if payment_info:
                        file.write(f"Payment Info: {payment_info}\n")
                    file.write(f"Items: {items}\n")
                    file.write(f"Total Qty: {total_qty}\n")
                    file.write(f"Overall total: {total:.2f}\n")
                    file.write("----------------------------------------\n")
                
                cart.clear()
                if cart_count_label:
                    cart_count_label.configure(text="View Cart")
                checkout_win.destroy()
                viewcart_win.destroy()
            
            checkout_confirm_btn = CTkButton(
                checkout_btn_frame,
                text="Confirm Order",
                text_color=color_light, 
                fg_color=success_color,
                font=("Helvetica", 12, "bold"),
                command=confirm_order
                )
            checkout_confirm_btn.grid(row=0, column=0, pady=5, padx=(0, 30))
            
            # Checkout cancel order function
            def cancel_order():
                cancellation = messagebox.askyesno("Cancel Checkout", "Are you sure you want to cancel your order/s?")
                if cancellation:
                    messagebox.showinfo("Cancelled", "Your checkout has been cancelled")
                    checkout_win.destroy()
            
            checkout_cancel_btn = CTkButton(
                checkout_btn_frame,
                text="Cancel Order",
                text_color=color_light,
                font=("Helvetica", 12, "bold"),
                fg_color=error_color,
                command=cancel_order
            )
            checkout_cancel_btn.grid(row=0, column=1, pady=5)
        
        checkout_btn = CTkButton(
            cart_btn_frame, 
            text="Checkout", 
            text_color=color_light, 
            font=("Helvetica", 12, "bold"), 
            fg_color=success_color, 
            command=open_checkout_win)
        checkout_btn.grid(row=0, column=0, pady=5, padx=(0, 30))
        
        # Clear function
        def clear_cart():
            confirm = messagebox.askyesno("Clear confirmation", "Are you sure you want to clear your cart?")
            if confirm:
                cart.clear()
                if cart_count_label:
                    cart_count_label.configure(text="View Cart")
                order_display()
        
        clear_btn = CTkButton(
            cart_btn_frame, 
            text="Clear Cart", 
            text_color=color_light, 
            font=("Helvetica", 12, "bold"), 
            fg_color=error_color,
            command=clear_cart)
        clear_btn.grid(row=0, column=1, pady=5)
        
        # Displaying order function
        def order_display():
            for widget in cart_order_frame.winfo_children():
                widget.destroy()
                
            if not cart:
                CTkLabel(cart_order_frame, text="Your cart is empty", font=("Helvetica", 15), text_color=muted_gray).pack(pady=20)
                total_label.configure(text="Total: ₱0")
                checkout_btn.configure(state="disabled")
                clear_btn.configure(state="disabled")
                return
            
            # Return the state of the checkout and rmove btn
            checkout_btn.configure(state="normal")
            clear_btn.configure(state="normal")
            
            heading_order_frame = CTkFrame(cart_order_frame, fg_color=light_gray, corner_radius=5)
            heading_order_frame.pack(fill="x", pady=2, padx=2)
            heading_order_frame.grid_columnconfigure(0, weight=2, uniform="col")
            heading_order_frame.grid_columnconfigure((1, 2, 3, 4), weight=1, uniform="col")
            
            CTkLabel(heading_order_frame, text="Product", font=("Helvetica", 13, "bold"), text_color=color_dark).grid(row=0, column=0, pady=5, sticky="ew")
            CTkLabel(heading_order_frame, text="Quantity", font=("Helvetica", 13, "bold"), text_color=color_dark).grid(row=0, column=1, pady=5, sticky="ew")
            CTkLabel(heading_order_frame, text="Price", font=("Helvetica", 13, "bold"), text_color=color_dark).grid(row=0, column=2, pady=5, sticky="ew")
            CTkLabel(heading_order_frame, text="+Qty", font=("Helvetica", 13, "bold"), text_color=color_dark).grid(row=0, column=3, pady=5)
            CTkLabel(heading_order_frame, text="-Qty", font=("Helvetica", 13, "bold"), text_color=color_dark).grid(row=0, column=4, pady=5)
            
            # Function fotr updating qty of product
            def update_cart_qty(product, qty):
                if product in cart:
                    cart[product]["qty"] += qty

                    if cart[product]["qty"] <= 0:
                        del cart[product]

                # update nav cart count label
                try:
                    if cart_count_label:
                        total_qty = 0
                        for details in cart.values():
                            total_qty += details["qty"]
                        if total_qty > 0:
                            cart_count_label.configure(text=f"Cart ({total_qty})")
                        else:
                            cart_count_label.configure(text="View Cart")
                except:
                    pass

                order_display()

            # Function for increasing qty
            def increase_qty(product):
                def increase():
                    update_cart_qty(product, 1)
                return increase
            
                            
            # Function for decreasing qty
            def decrease_qty(product):
                def decrease():
                    update_cart_qty(product, -1)
                return decrease
            
            total = 0
            for product, details in cart.items(): # product : {"qty" : ..., "price" : ....}
                qty = details["qty"]
                price = details["price"]
                subtotal = price * qty
                total += subtotal
                
                order_frame = CTkFrame(cart_order_frame, fg_color="transparent")
                order_frame.pack(fill="x", pady=2, padx=2)
                order_frame.grid_columnconfigure(0, weight=2, uniform="col")
                order_frame.grid_columnconfigure((1, 2, 3, 4), weight=1, uniform="col")
                
                CTkLabel(order_frame, text=product, font=("Helvetica", 12), text_color=color_dark).grid(row=0, column=0, pady=5)
                CTkLabel(order_frame, text=qty, font=("Helvetica", 12), text_color=color_dark).grid(row=0, column=1, pady=5)
                CTkLabel(order_frame, text=f"₱{price:.2f}", font=("Helvetica", 12), text_color=color_dark).grid(row=0, column=2, pady=5)
                
                CTkButton(
                    order_frame, 
                    text="+", 
                    font=("Helvetica", 15), 
                    text_color=color_dark, 
                    fg_color=warm_golden_orange,
                    width=30,
                    corner_radius=50,
                    hover_color=dark_golden,
                    command=increase_qty(product)
                    ).grid(row=0, column=3, pady=5)
                
                CTkButton(
                    order_frame, 
                    text="-", 
                    font=("Helvetica", 15), 
                    text_color=color_dark, 
                    fg_color=warm_golden_orange,
                    width=30,
                    corner_radius=50,
                    hover_color=dark_golden,
                    command=decrease_qty(product)
                    ).grid(row=0, column=4, pady=5)
                
            total_label.configure(text=f"Total: ₱{total:.2f}")
            
        order_display()
        
        def oncart_close():
            confirm = messagebox.askyesno(
                "Close Cart",
                "Do you want to close your cart?"
            )

            if confirm:
                viewcart_win.destroy()
                
        viewcart_win.protocol("WM_DELETE_WINDOW", oncart_close)
        
    # View Cart Btn
    nav_cart_btn = CTkButton(
        nav_frame, 
        text="View Cart", 
        font=("Helvetica", 15, "bold"), 
        corner_radius=5, 
        fg_color=warm_golden_orange, 
        width=80, 
        height=42,
        hover_color=dark_golden,
        command=open_viewcart_win
        )
    nav_cart_btn.place(x=1000, y=9)
    global cart_count_label
    cart_count_label = nav_cart_btn
    
    if cart:
        total_qty = 0
        for details in cart.values():
            total_qty += details["qty"]
        cart_count_label.configure(text=f"Cart ({total_qty})")
    
    # Logout function
    def logout():
        confirm = messagebox.askyesno("Confirm Logout", "Are you sure you want to logout?")
        
        if confirm:
            cart.clear()
            if cart_count_label:
                cart_count_label.configure(text="View Cart")
            window.destroy()
            root.deiconify()
            entry_log_username.delete(0, END)
            entry_log_password.delete(0, END)
            entry_log_username.focus_set()
    
    # Logout
    CTkButton(
        nav_frame, 
        text="Log Out",
        font=("Helvetica", 15, "bold"),
        text_color=color_light,
        fg_color=error_color,
        width=80,
        height=42,
        hover_color=dark_error,
        command=logout
        ).place(x=1100, y=9)
    
    def onclosing():
        confirm = messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?")
        
        if confirm:
            window.destroy()
            root.deiconify()
            entry_log_username.focus_set()
            
    window.protocol("WM_DELETE_WINDOW", onclosing)

# -----------------------------------------------------------------------------------------------

# HISTORY PAGE SECTION
def open_history_win(parent):
    history_scroll_frame = CTkScrollableFrame(parent, fg_color=color_light, width=1200, height=720, corner_radius=0,)
    history_scroll_frame.pack(fill="both", expand=True)
    
    # History frame
    history_frame = CTkFrame(history_scroll_frame, width=1200, height=350, fg_color=window_bg_light, corner_radius=0)
    history_frame.pack(fill="x")
    
    # History Image
    history_img = CTkImage(dark_image=Image.open(img_folder + "icon2.png"), size=(400, 320))
    CTkLabel(history_frame, image=history_img, text="").place(x=800, y=20)
    
    # History labels
    CTkLabel(
        history_frame, 
        text="History", 
        text_color=color_dark, 
        font=("Helvetica", 60, "bold"),
        justify="left",
        anchor="w"
        ).place(x=40, y=135)
    
    table_container = CTkFrame(history_scroll_frame, fg_color=color_light)
    table_container.pack(fill="x", padx=20, pady=20)
    
    CTkLabel(table_container, text="Order History Table", font=("helvetica", 30, "bold"), text_color=sky_blue).pack(pady=(30, 0))
    CTkFrame(table_container, width=200, height=10, fg_color=warm_golden_orange, corner_radius=0, border_color=charcoal_gray, border_width=2).pack(pady=20)
    
    table_frame = CTkFrame(table_container)
    table_frame.pack(fill="x")
    
    columns = ("Date/Time", "Name", "Payment", "QTY", "Product", "Total")
    
    order_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
    scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=order_table.yview)
    order_table.configure(yscrollcommand=scroll_y.set)
    
    for col in columns:
        order_table.heading(col, text=col, anchor="center")
        if col == "Date/Time":
            order_table.column(col, width=180, anchor="center")
        elif col == "Name":
            order_table.column(col, width=180, anchor="center")
        elif col == "Payment":
            order_table.column(col, width=100, anchor="center")
        elif col == "QTY":
            order_table.column(col, width=70, anchor="center")
        elif col == "Product":
            order_table.column(col, width=450, anchor="center")
        elif col == "Total":
            order_table.column(col, width=70, anchor="center")
    
    scroll_y.pack(side="right", fill="y")
    order_table.pack(fill="x")
    
    footer(history_scroll_frame)
    
    try:
        with open(orders_file, "r") as file:
            for line in file:
                data = line.strip().split(", ")
                
                date_time = data[0]
                name = data[1]
                payment = data[2]
                qty = data[3]
                product = data[4].split(" | ")
                total = data[-1]
                product = ", ".join(data[4:-1])
                
                order_table.insert("", END, values=(date_time, name, payment, qty, product, total))
    
    except FileNotFoundError:
        pass
# -----------------------------------------------------------------------------------------------

# MENU PAGE SECTION
def open_menu_win(parent):
    menu_scroll_frame = CTkScrollableFrame(parent, fg_color=color_light, width=1200, height=720, corner_radius=0,)
    menu_scroll_frame.pack(fill="both", expand=True)
    
    # Menu frame
    menu_frame = CTkFrame(menu_scroll_frame, width=1200, height=350, fg_color=window_bg_light, corner_radius=0)
    menu_frame.pack()
    
    # Menu Image
    menu_img = CTkImage(dark_image=Image.open(img_folder + "icon2.png"), size=(400, 320))
    CTkLabel(menu_frame, image=menu_img, text="").place(x=800, y=20)
    
    # Menu labels
    CTkLabel(
        menu_frame, 
        text="Menu", 
        text_color=color_dark, 
        font=("Helvetica", 60, "bold"),
        justify="left",
        anchor="w"
        ).place(x=40, y=135)
    
    # Menu Section
    menus_container = CTkFrame(menu_scroll_frame, width=1200, height=400, fg_color=color_light, corner_radius=0)
    menus_container.pack()
    
    CTkLabel(
        menus_container, 
        text="Our Delicious Menu", 
        font=("Helvetica", 30, "bold"),
        text_color=sky_blue,
        ).pack(pady=30)
    CTkFrame(menus_container, width=200, height=10, fg_color=warm_golden_orange, corner_radius=0, border_color=charcoal_gray, border_width=2).pack()
    CTkLabel(
        menus_container,
        text="Discover a variety of tasty dishes,\nfrom savory meals to sweet treats made just for you.",
        font=("Helvetica", 20),
        text_color=color_dark,
        justify="center"
        ).pack(pady=20)
    
    product = open_product_file()
    build_menu(menus_container, product, "burger")
    build_menu(menus_container, product, "chicken")
    build_menu(menus_container, product, "pizza")
    build_menu(menus_container, product, "drink")
    footer(menu_scroll_frame)
    
# -----------------------------------------------------------------------------------------------

# ABOUT PAGE SECTION
def open_about_win(parent):
    about_scroll_frame = CTkScrollableFrame(parent, fg_color=color_light, width=1200, height=720, corner_radius=0,)
    about_scroll_frame.pack(fill="both", expand=True)
    
    # About frame
    about_frame = CTkFrame(about_scroll_frame, width=1200, height=350, fg_color=window_bg_light, corner_radius=0)
    about_frame.pack(fill="x")
    
    # About Image
    about_img = CTkImage(dark_image=Image.open(img_folder + "icon2.png"), size=(400, 320))
    CTkLabel(about_frame, image=about_img, text="").place(x=800, y=20)
    
    # About labels
    CTkLabel(
        about_frame, 
        text="About", 
        text_color=color_dark, 
        font=("Helvetica", 60, "bold"),
        justify="left",
        anchor="w"
        ).place(x=40, y=135)
    
    # About main frame
    about_main_frame = CTkFrame(about_scroll_frame, fg_color=color_light)
    about_main_frame.pack(fill="x")
    
    CTkLabel(about_main_frame, text="About Us", font=("Helvetica", 30, "bold"), text_color=sky_blue).pack(pady=(30, 20))
    CTkLabel(about_main_frame, text="Welcome to Grill Bite", font=("Helvetica", 40, "bold"), text_color=color_dark).pack()
    CTkFrame(about_main_frame, width=200, height=8, fg_color=warm_golden_orange, corner_radius=0, border_color=charcoal_gray, border_width=1).pack(pady=10)
    
    CTkLabel(about_main_frame, text="Healthy Grilled Meals", font=("Helvetica", 25, "bold"), text_color=color_dark).pack(pady=20)
    CTkLabel(
        about_main_frame, 
        text="Enjoy freshly prepared meals made with quality ingredients, perfectly cooked\nto satisfy your cravings while keeping every bite flavorful and balanced",
        font=("Helvetica", 20),
        text_color=color_dark,
        justify="center"
        ).pack(pady=10)
    
    # About info Frame
    about_info_frame = CTkFrame(about_main_frame, fg_color=color_light)
    about_info_frame.pack(pady=40)
    
    # Info1
    info_refresh = CTkFrame(about_info_frame, fg_color=color_light, border_color=charcoal_gray, border_width=2, width=250, height=250)
    info_refresh.grid(row=0, column=0, pady=5)
    info_refresh.pack_propagate(False)
    
    refresh_img = CTkImage(light_image=Image.open(img_folder + "cold-drink.png"), size=(80, 80))
    CTkLabel(info_refresh, image=refresh_img, text="").pack(pady=20)
    
    CTkLabel(info_refresh, text="Refreshing Cold Drinks", font=("Helvetica", 15, "bold"), text_color=color_dark).pack()
    CTkLabel(
        info_refresh,
        text="Complete your meal with our refreshing\ncold drinks,perfectly served to keep every\nbite cool,satisfying and enjoyable",
        font=("Helvetica", 12),
        text_color=muted_gray
        ).pack(pady=10)
    
    # Info2
    info_service = CTkFrame(about_info_frame, fg_color=color_light, border_color=charcoal_gray, border_width=2, width=250, height=250)
    info_service.grid(row=0, column=1, pady=5, padx=30)
    info_service.pack_propagate(False)
    
    service_img = CTkImage(light_image=Image.open(img_folder + "support.png"), size=(80, 80))
    CTkLabel(info_service, image=service_img, text="").pack(pady=20)
    
    CTkLabel(info_service, text="Fresh & Fast Service", font=("Helvetica", 15, "bold"), text_color=color_dark).pack()
    CTkLabel(
        info_service,
        text="Order your favorite dishes quickly and\nconveniently with a smooth and hassle-free\nfood ordering experience",
        font=("Helvetica", 12),
        text_color=muted_gray
        ).pack(pady=10)
    
    # Info3
    info_favorites = CTkFrame(about_info_frame, fg_color=color_light, border_color=charcoal_gray, border_width=2, width=250, height=250)
    info_favorites.grid(row=0, column=2, pady=5)
    info_favorites.pack_propagate(False)
    
    fav_img = CTkImage(light_image=Image.open(img_folder + "heart.png"), size=(80, 80))
    CTkLabel(info_favorites, image=fav_img, text="").pack(pady=20)
    
    CTkLabel(info_favorites, text="Crispy & Juicy Favorites", font=("Helvetica", 15, "bold"), text_color=color_dark).pack()
    CTkLabel(
        info_favorites,
        text="From golden fried chicken to cheesy pizzas\nand loaded burgers, Grill Bite servers\ncomfort food made to delight every appetite",
        font=("Helvetica", 12),
        text_color=muted_gray
        ).pack(pady=10)
    
    footer(about_scroll_frame)
    
# -----------------------------------------------------------------------------------------------

# HOME/MAIN PAGE SECTION
def open_home_win(parent):
    # Function to go menu
    def goto_menu():
        if page_switcher:
            page_switcher("menu")
    
    #----------------------------------------------------------------------------------------------------
    # Scroll frame
    home_scroll_frame = CTkScrollableFrame(parent, fg_color=color_light, width=1200, height=720, corner_radius=0,)
    home_scroll_frame.pack(fill="both", expand=True)
    
    # Home frame
    home_frame = CTkFrame(home_scroll_frame, width=1200, height=550, fg_color=window_bg_light, corner_radius=0)
    home_frame.pack(fill="x")
    
    # Home Image
    home_img = CTkImage(dark_image=Image.open(img_folder + "icon2.png"), size=(550, 425))
    CTkLabel(home_frame, image=home_img, text="").place(x=650, y=100)
    
    # Home labels
    CTkLabel(
        home_frame, 
        text="Hungry? Browse the menu and\nplace your order with", 
        text_color=color_dark, 
        font=("Helvetica", 40, "bold"),
        justify="left",
        anchor="w"
        ).place(x=40, y=180)
    CTkLabel(home_frame, text="Grill Bite", text_color=sky_blue, font=("Helvetica", 40, "bold")).place(x=452, y=229)
    
    CTkLabel(
        home_frame, 
        text="A fast and simple food ordering system - pick your meals, place\nyour order and let the kitchen handle the rest.", 
        text_color=color_dark, 
        font=("Helvetica", 20),
        justify="left",
        anchor="w"
        ).place(x=40, y=310)
    
    # Explore menu btn
    explore_menu_btn = CTkButton(
        home_frame, 
        text="Explore Menu",
        fg_color=warm_golden_orange,
        corner_radius=5,
        font=("Helvetica", 15, "bold"),
        width=160,
        height=42,
        hover_color=dark_golden,
        command=goto_menu
        )
    explore_menu_btn.place(x=40, y=400)
    
    #----------------------------------------------------------------------------------------------------
    
    # Recommend main frame
    home_recommend = CTkFrame(home_scroll_frame, width=1200, fg_color=color_light, corner_radius=0)
    home_recommend.pack(fill="both")
    
    CTkLabel(home_recommend, text="Our Recomendations", text_color=sky_blue, font=("Helvetica", 30, "bold")).pack(pady=30)
    CTkFrame(home_recommend, width=200, height=8, fg_color=warm_golden_orange, corner_radius=0, border_color=charcoal_gray, border_width=1).pack()
    CTkLabel(
        home_recommend, 
        text="Explore top-rated dishes from our kitchen,\nfrom juicy burgers to cripy chicken and cheesy pizzas",
        font=("Helvetica", 20),
        text_color=color_dark,
        justify="center",
        ).pack(pady=20)
    
    # Recommend item frame
    recom_content = CTkFrame(home_recommend, fg_color="transparent", corner_radius=0)
    recom_content.pack()
    
    product = open_product_file()
    build_menu(recom_content, product, "burger", limit=3)
    build_menu(recom_content, product, "chicken", limit=3)
    build_menu(recom_content, product, "pizza", limit=3)
    
    # See more btn
    CTkButton(
        home_recommend, 
        text="See More", 
        font=("Helvetica", 15, "bold"),
        text_color=color_light,
        fg_color=warm_golden_orange,
        hover_color=dark_golden,
        width=70,
        height=42,
        command=goto_menu
        ).pack(pady=10)
    
    # Footer
    footer(home_scroll_frame)
    
# -----------------------------------------------------------------------------------------------

win_pages = {
    "home" : open_home_win,
    "about" : open_about_win,
    "menu" : open_menu_win,
    "history" : open_history_win,
}

# -----------------------------------------------------------------------------------------------
# MAIN APPLICATION WINDOW

def open_main_window():
    global main_win, page_switcher
    root.withdraw()
    main_win = CTkToplevel(root)
    main_win.title("Grill Bite")
    main_win.geometry("1200x720")
    main_win.resizable(False, False)
    main_win.configure(fg_color=color_light)

    navigation(root, main_win)

    content_frame = CTkFrame(main_win, fg_color="transparent")
    content_frame.pack(fill="both", expand=True)

    def switch_page(page):
        clear_content(content_frame)
        if page in win_pages:
            win_pages[page](content_frame)

    page_switcher = switch_page
    page_switcher("home")

# -----------------------------------------------------------------------------------------------
# REGISTRATION SECTION
def open_register_win():
    root.withdraw() # TEMPORARY HIDE THE ROOT LOGIN
    
    # ANOTHER WINDOW FOR REGISTRATION
    register_win = CTkToplevel(root)
    register_win.title("Registration Page")
    register_win.geometry("1000x700")
    register_win.resizable(False, False)
    register_win.configure(fg_color=midnight_navy)
    
    CTkLabel(register_win, text="Join", font=("Helvetica", 35, "bold"), text_color=color_light).place(x=210, y=200)
    CTkLabel(register_win, text="Grill Bite", font=("Helvetica", 50, "bold"), text_color=sky_blue).place(x=150, y=260)
    CTkLabel(register_win, text="today", font=("Helvetica", 35, "bold"), text_color=color_light).place(x=210, y=350)
    
    # -----------------------------------------------------------------------------------------------
    
    # REGISTER FRAME
    register_frame = CTkScrollableFrame(register_win, width=480, height=700, corner_radius=0, fg_color=color_light)
    register_frame.pack(side=RIGHT)
    
    register_frame.grid_columnconfigure(0, weight=1) # Use to center grid
    
    # REGISTER LABELS
    CTkLabel(register_frame, text="Register", text_color=color_dark, font=("Helvetica", 50, "bold")
    ).grid(row=0, column=0, pady=(60, 30)) # pady(top, bottom) tuple
    CTkLabel(register_frame, text="Kindly fill in this form to register", text_color=color_dark, font=("Helvetica", 18)
    ).grid(row=1, column=0, pady=(0, 30))
    
    # FIRST NAME
    CTkLabel(register_frame, text="First Name:", text_color=color_dark, font=("Helvetica", 15, "bold")
    ).grid(row=2, column=0, pady=(0, 10), padx=60, sticky="w")
    
    reg_firstname = CTkEntry(
        register_frame,
        placeholder_text="Enter firstname",
        placeholder_text_color=muted_gray,
        width=350,
        height=40,
        fg_color=light_gray,
        border_color=charcoal_gray,
        font=("Helvetica", 12),
        text_color=muted_gray
    )
    reg_firstname.grid(row=3, column=0, padx=30)
    
    # LAST NAME
    CTkLabel(register_frame, text="Last Name:", text_color=color_dark, font=("Helvetica", 15, "bold")
    ).grid(row=4, column=0, pady=(10, 10), padx=60, sticky="w") 
    
    reg_lastname = CTkEntry(
        register_frame,
        placeholder_text="Enter lastname",
        placeholder_text_color=muted_gray,
        width=350,
        height=40,
        fg_color=light_gray,
        border_color=charcoal_gray,
        font=("Helvetica", 12),
        text_color=muted_gray,
    )
    reg_lastname.grid(row=5, column=0, padx=30)
    
    # USERNAME
    CTkLabel(register_frame, text="Username:", text_color=color_dark, font=("Helvetica", 15, "bold")
    ).grid(row=6, column=0, pady=(10, 10), padx=60, sticky="w") 
    
    reg_username = CTkEntry(
        register_frame,
        placeholder_text="Enter username",
        placeholder_text_color=muted_gray,
        width=350,
        height=40,
        fg_color=light_gray,
        border_color=charcoal_gray,
        font=("Helvetica", 12),
        text_color=muted_gray,
    )
    reg_username.grid(row=7, column=0, padx=30)
    
    # EMAIL
    CTkLabel(register_frame, text="Email:", text_color=color_dark, font=("Helvetica", 15, "bold")
    ).grid(row=8, column=0, pady=(10, 10), padx=60, sticky="w") 
    
    reg_email = CTkEntry(
        register_frame,
        placeholder_text="Enter email",
        placeholder_text_color=muted_gray,
        width=350,
        height=40,
        fg_color=light_gray,
        border_color=charcoal_gray,
        font=("Helvetica", 12),
        text_color=muted_gray
    )
    reg_email.grid(row=9, column=0, padx=30)
    
    # PASSWORD
    CTkLabel(register_frame, text="Password:", text_color=color_dark, font=("Helvetica", 15, "bold")
    ).grid(row=10, column=0, pady=(10, 10), padx=60, sticky="w") 
    
    reg_password = CTkEntry(
        register_frame,
        placeholder_text="Enter password",
        placeholder_text_color=muted_gray,
        width=350,
        height=40,
        fg_color=light_gray,
        border_color=charcoal_gray,
        font=("Helvetica", 12),
        text_color=muted_gray,
        show="*"
    )
    reg_password.grid(row=11, column=0, padx=30)
    
    def toggle_reg_password():
        if reg_password.cget("show") == "*":
            reg_password.configure(show="")
            reg_show_password_btn.configure(text="hide")
        else:
            reg_password.configure(show="*")
            reg_show_password_btn.configure(text="show")
    
    reg_show_password_btn = CTkButton(
    register_frame,
    text="show",
    width=35,
    height=30,
    fg_color=light_gray,
    hover_color=light_gray,
    corner_radius=0,
    border_color=light_gray,
    text_color=muted_gray,
    command=toggle_reg_password
    )
    reg_show_password_btn.place(x=370, y=605)
    
    # RETYPE_PASS
    CTkLabel(register_frame, text="Repeat password", text_color=color_dark, font=("Helvetica", 15, "bold")
    ).grid(row=12, column=0, pady=(10, 10), padx=60, sticky="w")
    
    reg_repeat_pass = CTkEntry(
        register_frame,
        placeholder_text="Repeat password",
        placeholder_text_color=muted_gray,
        width=350,
        height=40,
        fg_color=light_gray,
        border_color=charcoal_gray,
        font=("Helvetica", 12),
        text_color=muted_gray,
        show="*"
    )
    reg_repeat_pass.grid(row=13, column=0, padx=30)
    
    # Function for showing password
    def toggle_repeat_password():
        if reg_repeat_pass.cget("show") == "*":
            reg_repeat_pass.configure(show="")
            reg_show_repass_btn.configure(text="hide")
        else:
            reg_repeat_pass.configure(show="*")
            reg_show_repass_btn.configure(text="show")
    
    reg_show_repass_btn = CTkButton(
    register_frame,
    text="show",
    width=35,
    height=30,
    fg_color=light_gray,
    hover_color=light_gray,
    corner_radius=0,
    border_color=light_gray,
    text_color=muted_gray,
    command=toggle_repeat_password
    )
    reg_show_repass_btn.place(x=370, y=693)
    
    # CONTACT
    CTkLabel(register_frame, text="Contact", text_color=color_dark, font=("Helvetica", 15, "bold")
    ).grid(row=14, column=0, pady=(10, 10), padx=60, sticky="w") 
    
    reg_contact = CTkEntry(
        register_frame,
        placeholder_text="Enter phone number",
        placeholder_text_color=muted_gray,
        width=350,
        height=40,
        fg_color=light_gray,
        border_color=charcoal_gray,
        font=("Helvetica", 12),
        text_color=muted_gray
    )
    reg_contact.grid(row=15, column=0, padx=30)
    
    # GENDER
    CTkLabel(register_frame, text="Gender", text_color=color_dark, font=("Helvetica", 15, "bold")
    ).grid(row=16, column=0, pady=(10, 10), padx=60, sticky="w") 
    
    gender_menu = ["Male", "Female", "Others"]
    gender_var = StringVar(value="Select Gender")
    
    reg_gender = CTkComboBox(register_frame,
                            variable=gender_var,
                            values=gender_menu,
                            text_color=muted_gray,
                            width=350,
                            height=40,
                            fg_color=light_gray,
                            border_color=charcoal_gray,
                            font=("Helvetica", 12),
                            button_color=charcoal_gray,
                            button_hover_color=light_gray,
                            dropdown_fg_color=light_gray,
                            dropdown_hover_color=charcoal_gray,
                            dropdown_text_color=muted_gray,
                            dropdown_font=("Helvetica", 12),
                            state="readonly"
                            )
    reg_gender.grid(row=17, column=0, padx=30)
    
    # -----------------------------------------------------------------------------------------------
    
    # SUBMIT BTN
    def register():
        input_fields = [
            (reg_firstname, "Firstname"),  
            (reg_lastname, "Lastname"), 
            (reg_username, "Username"),
            (reg_email, "Email"),
            (reg_password, "Password"),
            (reg_repeat_pass, "Repeat password"), 
            (reg_contact, "Contact")
        ]
    
        for widget, name in input_fields:
            value = widget.get().strip()
            
            if value == "":
                widget.configure(border_color=error_color, placeholder_text_color=error_color)
                messagebox.showerror("Error", f"Opssie! {name} is missing. Please fill it in.")
                widget.focus_set()
                return
            else:
                widget.configure(border_color=charcoal_gray, placeholder_text_color=muted_gray)
                
        firstname = reg_firstname.get().title()
        lastname = reg_lastname.get().title()
        username = reg_username.get()
        email = reg_email.get()
        password = reg_password.get()
        repeat_pass = reg_repeat_pass.get()
        contact = reg_contact.get()
        gender = gender_var.get()
        
        # EMAIL VALIDATION
        if "@" not in email or not email.endswith(".com"):
            reg_email.configure(border_color=error_color, placeholder_text_color=error_color)
            messagebox.showerror("Error", "Please enter a valid email address.")
            reg_email.focus_set()
            return
        
        # PASSWORD VALIDATIONS
        if password != repeat_pass:
            reg_password.configure(border_color=error_color, placeholder_text_color=error_color)
            reg_repeat_pass.configure(border_color=error_color, placeholder_text_color=error_color)
            messagebox.showerror("Error", "Passwords do not match.")
            reg_repeat_pass.delete(0, END)
            reg_repeat_pass.focus_set()
            return
        
        if len(password) < 8 or len(password) > 16:
            reg_password.configure(border_color=error_color, placeholder_text_color=error_color)
            messagebox.showerror("Error", "Password must be between 8-16 characters long.")
            reg_repeat_pass.delete(0, END)
            reg_repeat_pass.focus_set()
            return
        
        # CONTACT VALIDATIONS
        if not contact.isdigit():
            reg_contact.configure(border_color=error_color, placeholder_text_color=error_color)
            messagebox.showerror("Error", "Contact must be contain digits only.")
            reg_contact.delete(0, END)
            reg_contact.focus_set()
            return
        
        if len(contact) != 11:
            reg_contact.configure(border_color=error_color, placeholder_text_color=error_color)
            messagebox.showerror("Error", "Contact must be at least 11 digits.")
            reg_contact.delete(0, END)
            reg_contact.focus_set()
            return
        
        # GENDER VALIDATION
        if gender not in gender_menu:
            reg_gender.configure(border_color=error_color)
            messagebox.showerror("Error", "Please select gender.")
            return
        else:
            reg_gender.configure(border_color=charcoal_gray)
        
        try:
            with open(users_file, "r") as file:
                for line in file:
                    stored_username = line.strip().split(",")[2]
                    stored_email = line.strip().split(",")[3]
                    
                    if username == stored_username:
                        reg_username.configure(border_color=error_color, placeholder_text_color=error_color)
                        messagebox.showerror("Error", "Username is already exist. Please try another one.")
                        reg_username.focus_set()
                        return
                    
                    if email == stored_email:
                        reg_email.configure(border_color=error_color, placeholder_text_color=error_color)
                        messagebox.showerror("Error", "Email is already exist. Please try another one.")
                        reg_email.focus_set()
                        return
                    
        except FileNotFoundError:
            pass
        
        with open(users_file, "a") as file:
            file.write(f"{firstname}, {lastname}, {username}, {email}, {password}, {contact}, {gender}\n")

        messagebox.showinfo(f"Registration Successful!", "Your account has been created successfully. You can now login.")
        register_win.destroy()
        root.deiconify()
    
    # REGISTER BTN
    reg_btn = CTkButton(register_frame,
                        text="Submit",
                        width=350,
                        height=40,
                        fg_color=ocean_blue,
                        hover_color=sky_blue,
                        text_color=color_light,
                        font=("Helvetica", 15, "bold"),
                        command=register
                        )
    reg_btn.grid(row=18, column=0, padx=30, pady=40)
    
    already_acc_frame = CTkFrame(register_frame, fg_color="transparent")
    already_acc_frame.grid(row=19, column=0, padx=30, pady=(0, 20))
    
    CTkLabel(already_acc_frame, text="Already have an account?", font=("Helvetica", 15), text_color=color_dark).grid(row=0, column=0)
    
    def goto_login_page():
        register_win.destroy()
        root.deiconify()
    
    already_acc_btn = CTkButton(
        already_acc_frame,
        text="Log in",
        width=100,
        font=("Helvetica", 15), 
        text_color=sky_blue, 
        fg_color="transparent",
        hover=False,
        command=goto_login_page
        )
    already_acc_btn.grid(row=0, column=1)

# -----------------------------------------------------------------------------------------------
# LOGIN SECTION
root = CTk()
root.title("Login Page")
root.geometry("1000x700")
root.resizable(False, False)
root.configure(fg_color=midnight_navy)

CTkLabel(root, text="Welcome back\n\nto", font=("Helvetica", 35, "bold")).place(x=130, y=200)
CTkLabel(root, text="Grill Bite", font=("Helvetica", 50, "bold"), text_color=sky_blue).place(x=150, y=350)

# LOGIN FRAME (RIGHT SIDE)
login_frame = CTkFrame(root, fg_color=color_light, width=480, height=700, corner_radius=0)
login_frame.pack(side=RIGHT)

CTkLabel(login_frame, text="Login", font=("Helvetica", 50, "bold"), text_color=color_dark).place(x=175, y=100)

# USERNAME ENTRY
entry_log_username = CTkEntry(login_frame,
                            placeholder_text="👤 Username",
                            placeholder_text_color=muted_gray,
                            width=350,
                            height=40,
                            fg_color=light_gray,
                            border_color=charcoal_gray,
                            font=("Helvetica", 12),
                            text_color=muted_gray,
                            )
entry_log_username.place(x=65, y=200)

# PASSWORD ENTRY
entry_log_password = CTkEntry(login_frame,
                            placeholder_text="🔒 Password",
                            placeholder_text_color=muted_gray,
                            width=350,
                            height=40,
                            fg_color=light_gray,
                            border_color=charcoal_gray,
                            font=("Helvetica", 12),
                            text_color=muted_gray,
                            show="*"
                            )
entry_log_password.place(x=65, y=270)

def toggle_login_password():
    if entry_log_password.cget("show") == "*":
        entry_log_password.configure(show="")
        show_password_btn.configure(text="hide")
    else:
        entry_log_password.configure(show="*")
        show_password_btn.configure(text="show")

show_password_btn = CTkButton(
    login_frame,
    text="show",
    width=35,
    height=30,
    fg_color=light_gray,
    hover_color=light_gray,
    corner_radius=0,
    border_color=light_gray,
    text_color=muted_gray,
    command=toggle_login_password
)
show_password_btn.place(x=370, y=275)

# LOGIN FUNCTION
def login():
    entry_log = [(entry_log_username, "Username"), (entry_log_password, "Password")]
    
    for entry, name in entry_log:
        value = entry.get()
        if value == "":
            entry.configure(border_color=error_color, placeholder_text_color=error_color)
            messagebox.showerror("Error", f"Opssie! {name} is missing. Please fill it in.")
            entry.focus_set()
            return
        else:
            entry.configure(border_color=charcoal_gray, placeholder_text_color=muted_gray)
            
    username = entry_log_username.get()
    password = entry_log_password.get()
    
    try:
        with open(users_file, "r") as file:
            for line in file:
                stored_username = line.strip().split(", ")[2]
                stored_email = line.strip().split(", ")[3]
                stored_password = line.strip().split(", ")[4]
                stored_contact = line.strip().split(", ")[5]
                
                if username == stored_username and password == stored_password:
                    
                    # Save the information to current user
                    current_user["username"] = stored_username
                    current_user["email"] = stored_email
                    current_user["contact"] = stored_contact
                    
                    messagebox.showinfo("Welcome Back", f"Login Successful! Welcome, {username}")
                    open_main_window()
                    return
                
        messagebox.showerror("Login Failed", "Invalid username or password.")
        entry_log_username.configure(border_color=error_color)
        entry_log_password.configure(border_color=error_color)
        entry_log_password.delete(0, END)
        entry_log_username.focus_set()
        
    except FileNotFoundError:
        pass
            
# LOGIN BUTTON
login_btn = CTkButton(login_frame,
                    text="Login",
                    text_color=color_light,
                    width=350,
                    height=40,
                    fg_color=ocean_blue,
                    font=("Helvetica", 15, "bold"),
                    hover_color=sky_blue,
                    command=login
                    )
login_btn.place(x=65, y=350) 

CTkLabel(login_frame, text="or", text_color=color_dark, font=("Helvetica", 15)).place(x=240, y=430)
CTkLabel(login_frame, text="Don't have an account?", text_color=color_dark, font=("Helvetica", 15)).place(x=100, y=500)

# REGISTER BUTTON
register_label = CTkButton(login_frame, 
                        text="Register now",
                        width=100,
                        font=("Helvetica", 15), 
                        text_color=sky_blue, 
                        fg_color="transparent",
                        hover=False,
                        command=open_register_win
                        )
register_label.place(x=270, y=500)

root.mainloop()
