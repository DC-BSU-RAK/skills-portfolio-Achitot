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
            file_path = "Exercise 3/studentMarks.txt"
            if not os.path.exists(file_path):
                messagebox.showwarning("Warning", f"File not found.")
                return
            
            with open(file_path, 'r') as file:
                lines = file.readlines()
                
            if not lines:
                return
                
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
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    # Saving New Data
    def save_data(self):
        try:
            file_path = "Exercise 3/studentMarks.txt"
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w') as file:
                # Write the number of students
                file.write(f"{len(self.students)}\n")
                
                # Write student's data
                for student in self.students:
                    coursework_str = ','.join(str(mark) for mark in student.coursework_marks)
                    file.write(f"{student.student_number},{student.name},{coursework_str},{student.exam_mark}\n")
                    
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
            return False

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
        
        # Sort menu
        sort_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Sort", menu=sort_menu)
        sort_menu.add_command(label="Sort by Name (Ascending)", command=lambda: self.sort_students('name', True))
        sort_menu.add_command(label="Sort by Name (Descending)", command=lambda: self.sort_students('name', False))
        sort_menu.add_command(label="Sort by Student Number (Ascending)", command=lambda: self.sort_students('number', True))
        sort_menu.add_command(label="Sort by Student Number (Descending)", command=lambda: self.sort_students('number', False))
        
        # Manage menu
        manage_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Manage", menu=manage_menu)
        manage_menu.add_command(label="Add Student", command=self.add_student)
        manage_menu.add_command(label="Delete Student", command=self.delete_student)
        manage_menu.add_command(label="Update Student", command=self.update_student)
    
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
    
    # Sorting Student Records
    def sort_students(self, sort_by, ascending=True):
        if not self.students:
            messagebox.showwarning("No Data", "No student records available to sort.")
            return
        
        if sort_by == 'name':
            self.students.sort(key=lambda s: s.name.lower(), reverse=not ascending)
        elif sort_by == 'number':
            self.students.sort(key=lambda s: s.student_number, reverse=not ascending)
        
        # Save the sorted data
        self.save_data()
        
        # Refresh the display
        self.view_all_students()
        
        order = "ascending" if ascending else "descending"
        self.status_var.set(f"Sorted students by {sort_by} in {order} order")
    
    # Adding a student record
    def add_student(self):
        # Create a dialog window for adding a new student
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Student")
        dialog.geometry("400x350")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Add New Student", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Input fields
        ttk.Label(dialog, text="Student Number:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        number_entry = ttk.Entry(dialog, width=30)
        number_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Name:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Coursework 1 (0-20):").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        cw1_entry = ttk.Entry(dialog, width=30)
        cw1_entry.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Coursework 2 (0-20):").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        cw2_entry = ttk.Entry(dialog, width=30)
        cw2_entry.grid(row=4, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Coursework 3 (0-20):").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        cw3_entry = ttk.Entry(dialog, width=30)
        cw3_entry.grid(row=5, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Exam Mark (0-100):").grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
        exam_entry = ttk.Entry(dialog, width=30)
        exam_entry.grid(row=6, column=1, padx=10, pady=5)
        
        def validate_and_add():
            try:
                # Validate inputs
                student_number = number_entry.get().strip()
                name = name_entry.get().strip()
                
                if not student_number or not name:
                    messagebox.showerror("Error", "Student number and name are required.")
                    return
                
                # Check if student number already exists
                if any(s.student_number == student_number for s in self.students):
                    messagebox.showerror("Error", "Student number already exists.")
                    return
                
                coursework_marks = [
                    int(cw1_entry.get().strip()),
                    int(cw2_entry.get().strip()),
                    int(cw3_entry.get().strip())
                ]
                
                # Validate coursework marks
                for mark in coursework_marks:
                    if mark < 0 or mark > 20:
                        messagebox.showerror("Error", "Coursework marks must be between 0 and 20.")
                        return
                
                exam_mark = int(exam_entry.get().strip())
                if exam_mark < 0 or exam_mark > 100:
                    messagebox.showerror("Error", "Exam mark must be between 0 and 100.")
                    return
                
                # Create new student and add to list
                new_student = Student(student_number, name, coursework_marks, exam_mark)
                self.students.append(new_student)
                
                # Save to file
                if self.save_data():
                    dialog.destroy()
                    self.view_all_students()
                    messagebox.showinfo("Success", f"Student {name} added successfully.")
                else:
                    # Remove student if save failed
                    self.students.remove(new_student)
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for marks.")
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Add Student", command=validate_and_add).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    # Deleting a student record
    def delete_student(self):
        if not self.students:
            messagebox.showwarning("No Data", "No student records available to delete.")
            return
        
        # Selecting the Student
        dialog = tk.Toplevel(self.root)
        dialog.title("Delete Student")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select Student to Delete", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Listbox with student data
        listbox = tk.Listbox(dialog, width=80, height=10)
        listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        for student in self.students:
            listbox.insert(tk.END, f"{student.student_number} - {student.name} - {student.calculate_overall_percentage():.1f}%")
        
        def delete_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a student to delete.")
                return
            
            index = selection[0]
            student = self.students[index]
            
            # Confirming deletion
            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {student.name} ({student.student_number})?"):
                deleted_student = self.students.pop(index)
                
                # Save to file
                if self.save_data():
                    dialog.destroy()
                    self.view_all_students()
                    messagebox.showinfo("Success", f"Student {deleted_student.name} deleted successfully.")
                else:
                    # Restoring if the student data saving failed
                    self.students.insert(index, deleted_student)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Delete Selected", command=delete_selected).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    # Updating a student record
    def update_student(self):
        if not self.students:
            messagebox.showwarning("No Data", "No student records available to update.")
            return
        
        #Selecting the student
        dialog = tk.Toplevel(self.root)
        dialog.title("Update Student")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Select Student to Update", font=('Arial', 14, 'bold')).pack(pady=10)
        
        listbox = tk.Listbox(dialog, width=80, height=10)
        listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        for student in self.students:
            listbox.insert(tk.END, f"{student.student_number} - {student.name} - {student.calculate_overall_percentage():.1f}%")
        
        def update_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a student to update.")
                return
            
            index = selection[0]
            student = self.students[index]
            
            dialog.destroy()
            self.show_update_dialog(student, index)
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Update Selected", command=update_selected).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
    def show_update_dialog(self, student, index):
        # Dialog window for updating student
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Update Student: {student.name}")
        dialog.geometry("400x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text=f"Update {student.name}", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        ttk.Label(dialog, text="Student Number:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        number_entry = ttk.Entry(dialog, width=30)
        number_entry.insert(0, student.student_number)
        number_entry.grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Name:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.insert(0, student.name)
        name_entry.grid(row=2, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Coursework 1 (0-20):").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        cw1_entry = ttk.Entry(dialog, width=30)
        cw1_entry.insert(0, str(student.coursework_marks[0]))
        cw1_entry.grid(row=3, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Coursework 2 (0-20):").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        cw2_entry = ttk.Entry(dialog, width=30)
        cw2_entry.insert(0, str(student.coursework_marks[1]))
        cw2_entry.grid(row=4, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Coursework 3 (0-20):").grid(row=5, column=0, sticky=tk.W, padx=10, pady=5)
        cw3_entry = ttk.Entry(dialog, width=30)
        cw3_entry.insert(0, str(student.coursework_marks[2]))
        cw3_entry.grid(row=5, column=1, padx=10, pady=5)
        
        ttk.Label(dialog, text="Exam Mark (0-100):").grid(row=6, column=0, sticky=tk.W, padx=10, pady=5)
        exam_entry = ttk.Entry(dialog, width=30)
        exam_entry.insert(0, str(student.exam_mark))
        exam_entry.grid(row=6, column=1, padx=10, pady=5)
        
        def validate_and_update():
            try:
                # Validate inputs
                student_number = number_entry.get().strip()
                name = name_entry.get().strip()
                
                if not student_number or not name:
                    messagebox.showerror("Error", "Student number and name are required.")
                    return
                
                # Checking if student number already exists (excluding current student)
                if any(s.student_number == student_number and s != student for s in self.students):
                    messagebox.showerror("Error", "Student number already exists.")
                    return
                
                coursework_marks = [
                    int(cw1_entry.get().strip()),
                    int(cw2_entry.get().strip()),
                    int(cw3_entry.get().strip())
                ]
                
                # Validate coursework marks
                for mark in coursework_marks:
                    if mark < 0 or mark > 20:
                        messagebox.showerror("Error", "Coursework marks must be between 0 and 20.")
                        return
                
                exam_mark = int(exam_entry.get().strip())
                if exam_mark < 0 or exam_mark > 100:
                    messagebox.showerror("Error", "Exam mark must be between 0 and 100.")
                    return
                
                # Update student
                student.student_number = student_number
                student.name = name
                student.coursework_marks = coursework_marks
                student.exam_mark = exam_mark
                
                # Save to file
                if self.save_data():
                    dialog.destroy()
                    self.view_all_students()
                    messagebox.showinfo("Success", f"Student {name} updated successfully.")
                else:
                    # Revert changes if save failed
                    self.load_data()
                    
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for marks.")
        
        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=7, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Update Student", command=validate_and_update).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=10)
    
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
        average_percentage = total_percentage / len(self.students) if self.students else 0
        
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