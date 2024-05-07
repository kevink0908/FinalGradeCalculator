# Name: Tony Gonzalez & Kevin Kim
# Instructor: Professor Yang
# Course: CS 2520.01
# Date: 5/11/2024
# Description: A Tkinter application that allows users to easily calculate their final course
#              grades. Users will be able to input labels for each field and adjust their 
#              grading scale based on their course.
import tkinter as tk
from tkinter import messagebox

class GradeCalculatorApp(tk.Tk):
    # This is the constructor for the grade calculator app.
    def __init__(self):
        super().__init__()
        self.title('Final Grade Calculator')
        self.geometry('500x300')

        # Keep track of user's data for grades.
        self.fields = []
        self.current_page = 0

        # Start GUI.
        self.start_frame = tk.Frame(self)
        self.start_frame.pack(fill='both', expand=True)

        # Prompt the user to enter the number of fields.
        tk.Label(self.start_frame, text="Please enter the number of fields:").pack(pady=20)
        self.num_fields_entry = tk.Entry(self.start_frame)
        self.num_fields_entry.pack()

        # Use the button to begin calculating final grade.
        tk.Button(self.start_frame, text="Submit", command=self.create_fields).pack(pady=10)

    # This method creates an appropriate data structure to store different grading criteria.
    def create_fields(self):
        # Sanitize user input.
        try:
            self.num_fields = int(self.num_fields_entry.get())
            if self.num_fields == 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for number of fields")
            return 

        self.start_frame.destroy()

        # Prepare data structure for all the fields.
        self.fields = [{'label': '', 'weight': 0, 'earned_points': 0, 'max_points': 0} for _ in range(self.num_fields)]
        self.setup_page(0)

    # This method allows the user to cutomize each field by prompting the user for label, grading scale weight,
    # Points earned, and max points for their course.
    def setup_page(self, page):
        # Check to see if this object has a frame. 
        if hasattr(self, 'current_frame'):
            # if so, destroy the existing frame.
            self.current_frame.destroy()
        
        # Then, start a new frame.
        self.current_frame = tk.Frame(self)
        self.current_frame.pack(fill='both', expand=True)

        field = self.fields[page]
        tk.Label(self.current_frame, text=f"Field {page+1}:").pack(pady=10)

        # Have the user input the label for this field.
        tk.Label(self.current_frame, text="Label:").pack()
        field['label_entry'] = tk.Entry(self.current_frame)
        field['label_entry'].pack()
        field['label_entry'].insert(0, field['label'])

        # Have the user input the weight for this field.
        tk.Label(self.current_frame, text="Weight (in %):").pack()
        field['weight_entry'] = tk.Entry(self.current_frame)
        field['weight_entry'].pack()
        field['weight_entry'].insert(0, str(field['weight']))

        # Have the user input earned points for this field.
        tk.Label(self.current_frame, text="Points earned:").pack()
        field['earned_entry'] = tk.Entry(self.current_frame)
        field['earned_entry'].pack()
        field['earned_entry'].insert(0, str(field['earned_points']))

        # Have the user input max points for this field.
        tk.Label(self.current_frame, text="Max points:").pack()
        field['max_entry'] = tk.Entry(self.current_frame)
        field['max_entry'].pack()
        field['max_entry'].insert(0, str(field['max_points']))

        # Allow the user to nagivate through different pages using the "back" and "next" buttons.
        if page > 0:
            tk.Button(self.current_frame, text="Back", command=lambda: self.change_page(-1)).pack(side='left', padx=10)

        if page < self.num_fields - 1:
            tk.Button(self.current_frame, text="Next", command=lambda: self.change_page(1)).pack(side='right', padx=10)
        else:
            tk.Button(self.current_frame, text="Calculate", command=self.calculate_final_grade).pack(side='right', padx=10)

    # This method changes pages.
    def change_page(self, direction):
        # Check if all fields have be properly populated
        try:
            self.save_current_page()
        except ValueError:
            return
        self.current_page += direction
        self.setup_page(self.current_page)

    # This method saves the most recent page that the user was on.
    def save_current_page(self):
        page = self.current_page
        field = self.fields[page]
        # Check if all fields have be properly populated
        try:
            field['label'] = field['label_entry'].get()
            field['weight'] = float(field['weight_entry'].get())
            field['earned_points'] = float(field['earned_entry'].get())
            field['max_points'] = float(field['max_entry'].get())
        except ValueError:
            messagebox.showerror("Error", "Please fill in fields before switching pages")
            raise ValueError

    # This method calculates the final grade.
    def calculate_final_grade(self):
        try:
            self.save_current_page()
            total_weight = sum(field['weight'] for field in self.fields) # calcualte total weight

            # Check if total weight == 100
            if total_weight != 100:
                messagebox.showerror("Error", "Total weight does not equal 100. Please recheck weights and try again")
                return
            
            # Calculate final grade
            final_grade = sum(
                (field['earned_points'] / field['max_points']) * field['weight']
                for field in self.fields
            ) / total_weight * 100
            messagebox.showinfo("Final Grade", f"Final Grade: {final_grade:.2f}%")
        except: # incorrect inputs
            messagebox.showerror("Error", "Please recheck values and try again")

if __name__ == "__main__":
    # run the calculator app.
    app = GradeCalculatorApp()
    # respond to user interactions with the mainloop() function.
    app.mainloop()