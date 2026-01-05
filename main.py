import tkinter as tk
from tkinter import ttk, messagebox

def calculate_time():
    try:
        # קבלת נתונים מהממשק
        temp_str = entry_temp.get()
        if not temp_str:
            messagebox.showerror("שגיאה", "נא להזין טמפרטורה")
            return
            
        core_temp = float(temp_str)
        is_poultry = var_type.get() == "poultry"
        is_ground = var_texture.get() == "ground"

        # לוגיקה עסקית (Safety Logic)
        if core_temp < 55:
            lbl_result.config(text="סכנה! טמפרטורה נמוכה מ-55°C\nלא מתבצעת השמדת חיידקים.", foreground="red")
            return

        # הגדרת פרמטרים לפי סוג הבשר (כפי שסיכמנו)
        if is_poultry:
            # עוף: מחמיר ביותר (סלמונלה)
            ref_temp = 70.0
            ref_time_minutes = 1.0  
            z_value = 8.0 # Z נמוך יותר = מחמיר יותר בטמפרטורות נמוכות
            product_name = "בעלי כנף (עוף/הודו)"
        elif is_ground:
            # בקר טחון
            ref_temp = 70.0
            ref_time_minutes = 0.5 
            z_value = 10.0
            product_name = "בקר/אחר (טחון)"
        else:
            # נתח שלם
            ref_temp = 70.0
            ref_time_minutes = 0.25
            z_value = 10.0
            product_name = "בקר/אחר (נתח שלם)"

        # חישוב F-value
        delta_temp = ref_temp - core_temp
        log_factor = delta_temp / z_value
        required_time = ref_time_minutes * (10 ** log_factor)

        # עיצוב התוצאה
        minutes = int(required_time)
        seconds = int((required_time - minutes) * 60)
        
        result_text = f"מוצר: {product_name}\n"
        result_text += f"טמפרטורת ליבה: {core_temp}°C\n\n"
        result_text += f"זמן המתנה נדרש לבטיחות:\n{minutes} דקות ו-{seconds} שניות"
        
        lbl_result.config(text=result_text, foreground="green")

    except ValueError:
        messagebox.showerror("שגיאה", "נא להזין מספר תקין בטמפרטורה")

# --- בניית ה-GUI ---
root = tk.Tk()
root.title("מחשבון בטיחות מזון - פסטור")
root.geometry("500x550")
root.resizable(False, False)

# סגנון (Style) לניראות מודרנית יותר
style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', font=('Arial', 11))
style.configure('TButton', font=('Arial', 12, 'bold'))
style.configure('TRadiobutton', font=('Arial', 11))

# כותרת
header = ttk.Label(root, text="מחשבון זמן פסטור (F-Value)", font=('Arial', 16, 'bold'))
header.pack(pady=15)

# מסגרת ראשית
main_frame = ttk.Frame(root, padding="20")
main_frame.pack(fill=tk.BOTH, expand=True)

# 1. סוג בשר
ttk.Label(main_frame, text="1. בחר את סוג המוצר:", font=('Arial', 12, 'bold')).pack(anchor='e', pady=(10, 5))
ttk.Label(main_frame, text="עוף דורש השמדת סלמונלה (7-log) ולכן הזמן ארוך יותר.", foreground="gray").pack(anchor='e')

var_type = tk.StringVar(value="meat")
frame_type = ttk.Frame(main_frame)
frame_type.pack(anchor='e', pady=5)
ttk.Radiobutton(frame_type, text="בקר / חזיר / אחר", variable=var_type, value="meat").pack(side=tk.RIGHT, padx=10)
ttk.Radiobutton(frame_type, text="בעלי כנף (עוף/הודו)", variable=var_type, value="poultry").pack(side=tk.RIGHT, padx=10)

# 2. מרקם
ttk.Label(main_frame, text="2. בחר את מרקם המוצר:", font=('Arial', 12, 'bold')).pack(anchor='e', pady=(15, 5))
ttk.Label(main_frame, text="בשר טחון מסוכן יותר כי חיידקים חודרים פנימה.", foreground="gray").pack(anchor='e')

var_texture = tk.StringVar(value="whole")
frame_texture = ttk.Frame(main_frame)
frame_texture.pack(anchor='e', pady=5)
ttk.Radiobutton(frame_texture, text="נתח שלם (Whole Muscle)", variable=var_texture, value="whole").pack(side=tk.RIGHT, padx=10)
ttk.Radiobutton(frame_texture, text="טחון / מעובד (Ground)", variable=var_texture, value="ground").pack(side=tk.RIGHT, padx=10)

# 3. טמפרטורה
ttk.Label(main_frame, text="3. טמפרטורת ליבה נמדדת (°C):", font=('Arial', 12, 'bold')).pack(anchor='e', pady=(15, 5))
ttk.Label(main_frame, text="הטמפרטורה הכי נמוכה שנמדדה במרכז המוצר.", foreground="gray").pack(anchor='e')

entry_temp = ttk.Entry(main_frame, justify='center', font=('Arial', 14))
entry_temp.pack(pady=5, ipadx=5, ipady=5)

# כפתור חישוב
btn_calc = ttk.Button(main_frame, text="חשב זמן בטיחות", command=calculate_time)
btn_calc.pack(pady=20, fill=tk.X)

# אזור תוצאה
lbl_result = ttk.Label(main_frame, text="הזן נתונים ולחץ על חישוב", font=('Arial', 14, 'bold'), justify='center', background="#f0f0f0", relief="sunken")
lbl_result.pack(fill=tk.BOTH, expand=True, ipady=10)

# הפעלה
root.mainloop()
