import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os

class Student:
    def __init__(self, student_number, name, coursework_marks, exam_mark):
        self.student_number = student_number
        self.name = name
        self.coursework_marks = coursework_marks
        self.exam_mark = exam_mark
        
    def calculate_total_coursework(self):
        return sum(self.coursework_marks)
    
    def calculate_overall_percentage(self):
        total_coursework = self.calculate_total_coursework()
        total_marks = total_coursework + self.exam_mark
        return (total_marks / 160) * 100
    
    def calculate_grade(self):
        percentage = self.calculate_overall_percentage()
        if percentage >= 70:
            return 'A'
        elif percentage >= 60:
            return 'B'
        elif percentage >= 50:
            return 'C'
        elif percentage >= 40:
            return 'D'
        else:
            return 'F'
    
    def get_formatted_result(self):
        total_coursework = self.calculate_total_coursework()
        percentage = self.calculate_overall_percentage()
        grade = self.calculate_grade()
        
        return (f"Name: {self.name}\n"
                f"Student Number: {self.student_number}\n"
                f"Total Coursework: {total_coursework}/60\n"
                f"Exam Mark: {self.exam_mark}/100\n"
                f"Overall Percentage: {percentage:.1f}%\n"
                f"Grade: {grade}")

class StudentManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Marks Management System")
        self.root.geometry("900x700")
      
        self.students = []
        self.load_data()
        
        self.create_menu()
        self.create_main_frame()
    
    def load_data(self):
        try:
            file_path = "Exercise 3\studentMarks.txt"
            if not os.path.exists(file_path):
                messagebox.showerror("Error", f"Failed to load data")
                return
            
            with open(file_path, 'r') as file:
                lines = file.readlines()
                
            num_students = int(lines[0].strip())
            
            for i in range(1, num_students + 1):
                if i < len(lines):
                    data = lines[i].strip().split(',')
                    if len(data) >= 6:
                        student_number = data[0]
                        name = data[1]
                        coursework_marks = [int(data[2]), int(data[3]), int(data[4])]
                        exam_mark = int(data[5])
                        
                        student = Student(student_number, name, coursework_marks, exam_mark)
                        self.students.append(student)
                        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data")
    
    
# Main Application Frame (View Details Buttons)
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="All Student Records", command=self.view_all_students)
        view_menu.add_separator()
        view_menu.add_command(label="Highest Overall Mark", command=self.show_highest_mark)
        view_menu.add_command(label="Lowest Overall Mark", command=self.show_lowest_mark)
    
    
# Main Application Frame (Display Screen)
    def create_main_frame(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)
        
        # Title
        self.title_label = ttk.Label(self.main_frame, text="Student Marks Management System", 
                                   font=('Arial', 16, 'bold'))
        self.title_label.grid(row=0, column=0, pady=(0, 20))
        
        # A canvas and scrollbar for the student boxes
        self.canvas = tk.Canvas(self.main_frame, bg='white')
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set(f"Loaded {len(self.students)} student records")
        status_bar = ttk.Label(self.main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Configure grid weights for scrolling
        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
    
    def clear_display(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
    
    def create_student_box(self, parent, student, index, clickable=False):
        # Create a frame for the student box with border
        box_frame = ttk.LabelFrame(parent, text=f"Student {index + -1}", padding="10")
        box_frame.grid(row=index, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        box_frame.columnconfigure(1, weight=1)
        
        if clickable:

            box_frame.bind("<Enter>", lambda e, frame=box_frame: self.on_box_enter(frame))
            box_frame.bind("<Leave>", lambda e, frame=box_frame: self.on_box_leave(frame))
            box_frame.bind("<Button-1>", lambda e, s=student: self.show_individual_student(s))
            
            for child in box_frame.winfo_children():
                child.bind("<Button-1>", lambda e, s=student: self.show_individual_student(s))
        
        # Get student data
        total_coursework = student.calculate_total_coursework()
        percentage = student.calculate_overall_percentage()
        grade = student.calculate_grade()
        
        # Show color based on grade
        color = self.get_grade_color(grade)
        
        # Student information
        name_label = ttk.Label(box_frame, text="Name:", font=('Arial', 9, 'bold'))
        name_label.grid(row=0, column=0, sticky=tk.W, pady=2)
        name_value = ttk.Label(box_frame, text=student.name, font=('Arial', 9))
        name_value.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        number_label = ttk.Label(box_frame, text="Student Number:", font=('Arial', 9, 'bold'))
        number_label.grid(row=1, column=0, sticky=tk.W, pady=2)
        number_value = ttk.Label(box_frame, text=student.student_number, font=('Arial', 9))
        number_value.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # Show Total Coursework
        total_cw_label = ttk.Label(box_frame, text="Total Coursework:", font=('Arial', 9, 'bold'))
        total_cw_label.grid(row=2, column=0, sticky=tk.W, pady=2)
        total_cw_value = ttk.Label(box_frame, text=f"{total_coursework}/60", font=('Arial', 9))
        total_cw_value.grid(row=2, column=1, sticky=tk.W, pady=2)
        
        exam_label = ttk.Label(box_frame, text="Exam Mark:", font=('Arial', 9, 'bold'))
        exam_label.grid(row=3, column=0, sticky=tk.W, pady=2)
        exam_value = ttk.Label(box_frame, text=f"{student.exam_mark}/100", font=('Arial', 9))
        exam_value.grid(row=3, column=1, sticky=tk.W, pady=2)
        
        percentage_label = ttk.Label(box_frame, text="Overall Percentage:", font=('Arial', 9, 'bold'))
        percentage_label.grid(row=4, column=0, sticky=tk.W, pady=2)
        percentage_value = ttk.Label(box_frame, text=f"{percentage:.1f}%", font=('Arial', 9))
        percentage_value.grid(row=4, column=1, sticky=tk.W, pady=2)
        
        grade_label = ttk.Label(box_frame, text="Grade:", font=('Arial', 9, 'bold'))
        grade_label.grid(row=5, column=0, sticky=tk.W, pady=2)
        grade_value = ttk.Label(box_frame, text=grade, font=('Arial', 11, 'bold'), foreground=color)
        grade_value.grid(row=5, column=1, sticky=tk.W, pady=2)
        
        if clickable:
            for widget in [name_label, name_value, number_label, number_value, 
                          total_cw_label, total_cw_value,
                          exam_label, exam_value, percentage_label, percentage_value,
                          grade_label, grade_value]:
                widget.bind("<Enter>", lambda e, frame=box_frame: self.on_box_enter(frame))
                widget.bind("<Leave>", lambda e, frame=box_frame: self.on_box_leave(frame))
                widget.bind("<Button-1>", lambda e, s=student: self.show_individual_student(s))
    
    def on_box_enter(self, frame):
        frame.configure(style='Hover.TLabelframe')
    
    def on_box_leave(self, frame):
        frame.configure(style='TLabelframe')
    
    # Giving color depending on grades
    def get_grade_color(self, grade):
        colors = {
            'A': 'green',
            'B': 'blue',
            'C': 'orange',
            'D': 'purple',
            'F': 'red'
        }
        return colors.get(grade, 'black')
    
    
# Show All student Records
    def view_all_students(self):
        self.clear_display()
        self.title_label.config(text="Student Marks Management System - All Student Records")
        
        # Title
        title_label = ttk.Label(self.scrollable_frame, text="ALL STUDENT RECORDS", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Instruction for clickable boxes
        instruction_label = ttk.Label(self.scrollable_frame, 
                                     text="Click on any student box to view individual record", 
                                     font=('Arial', 10), foreground='red')
        instruction_label.grid(row=1, column=0, pady=(0, 15))
        
        # Create boxes for each student
        for i, student in enumerate(self.students):
            self.create_student_box(self.scrollable_frame, student, i + 2, clickable=True)
        
        # Summary frame
        summary_frame = ttk.LabelFrame(self.scrollable_frame, text="CLASS SUMMARY", padding="15")
        summary_frame.grid(row=len(self.students) + 3, column=0, sticky=(tk.W, tk.E), padx=10, pady=20)
        summary_frame.columnconfigure(0, weight=1)
        
        # Calculate summary statistics
        total_percentage = sum(student.calculate_overall_percentage() for student in self.students)
        average_percentage = total_percentage / len(self.students)
        
        # Grade distribution
        grade_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        for student in self.students:
            grade = student.calculate_grade()
            grade_count[grade] += 1
        
        # Summary labels
        ttk.Label(summary_frame, text=f"Total Students: {len(self.students)}", 
                 font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=3)
        
        ttk.Label(summary_frame, text=f"Average Percentage: {average_percentage:.1f}%", 
                 font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, pady=3)
        
        ttk.Label(summary_frame, text="Grade Distribution:", 
                 font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=3)
        
        # Grade distribution details
        grade_text = f"A: {grade_count['A']} | B: {grade_count['B']} | C: {grade_count['C']} | D: {grade_count['D']} | F: {grade_count['F']}"
        ttk.Label(summary_frame, text=grade_text, 
                 font=('Arial', 9)).grid(row=3, column=0, sticky=tk.W, pady=2)
        
        # Update canvas scroll region
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(0)  # Scroll to top
        
        self.status_var.set(f"Displayed all {len(self.students)} student records. Click any box to view individual record.")
    

    # Show More Individual Records
    def show_individual_student(self, student):
        self.clear_display()
        self.title_label.config(text=f"Student Marks Management System")
        
        # Title
        title_label = ttk.Label(self.scrollable_frame, text="INDIVIDUAL STUDENT RECORD", 
                               font=('Arial', 14, 'bold'))
        title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Create a more detailed box for the individual student
        detailed_frame = ttk.LabelFrame(self.scrollable_frame, text="Student Details", padding="15")
        detailed_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=20, pady=10)
        detailed_frame.columnconfigure(1, weight=1)
        
        # Get student data
        total_coursework = student.calculate_total_coursework()
        percentage = student.calculate_overall_percentage()
        grade = student.calculate_grade()
        color = self.get_grade_color(grade)
        
        # Individual Information
        info_rows = [
            ("Student Name:", student.name),
            ("Student Number:", student.student_number),
            ("Total Coursework:", f"{total_coursework}/60"),
            ("Exam Mark:", f"{student.exam_mark}/100"),
            ("Overall Percentage:", f"{percentage:.1f}%"),
            ("Final Grade:", grade)
        ]
        
        for i, (label, value) in enumerate(info_rows):
            ttk.Label(detailed_frame, text=label, font=('Arial', 10, 'bold')).grid(
                row=i, column=0, sticky=tk.W, pady=8)
            
            if label == "Final Grade:":
                ttk.Label(detailed_frame, text=value, font=('Arial', 12, 'bold'), 
                         foreground=color).grid(row=i, column=1, sticky=tk.W, pady=8)
            else:
                ttk.Label(detailed_frame, text=value, font=('Arial', 10)).grid(
                    row=i, column=1, sticky=tk.W, pady=8)
        
        # Back button
        back_button = ttk.Button(self.scrollable_frame, text="Back to All Students",
                                command=self.view_all_students)
        back_button.grid(row=2, column=0, pady=20)
        
        # Update canvas
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(0)
        
        self.status_var.set(f"Displaying detailed record for {student.name}")
    
    
    # Show Highest Mark
    def show_highest_mark(self):
        if not self.students:
            messagebox.showwarning("No Data", "No student records available.")
            return
        
        highest_student = max(self.students, key=lambda s: s.calculate_overall_percentage())
        self.show_individual_student(highest_student)
        self.title_label.config(text=f"Student Marks Management System - Highest Mark")
        
        header_label = ttk.Label(self.scrollable_frame, text="Student With Highest Overall Mark", 
                                 font=('Arial', 14, 'bold'), foreground='darkgreen')
        header_label.grid(row=0, column=0, pady=(0, 20))
    

    # Show Lowest Mark
    def show_lowest_mark(self):
        if not self.students:
            messagebox.showwarning("No Data", "No student records available.")
            return
        
        lowest_student = min(self.students, key=lambda s: s.calculate_overall_percentage())
        self.show_individual_student(lowest_student)
        self.title_label.config(text=f"Student Marks Management System - Lowest Mark")
        
        header_label = ttk.Label(self.scrollable_frame, text="Student With Lowest Overall Mark", 
                                 font=('Arial', 14, 'bold'), foreground='darkred')
        header_label.grid(row=0, column=0, pady=(0, 20))

def main():
    root = tk.Tk()
    
    # Hover effect
    style = ttk.Style()
    style.configure('Hover.TLabelframe', background='#f0f0f0')
    
    app = StudentManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()