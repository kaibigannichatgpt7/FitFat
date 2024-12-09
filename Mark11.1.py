from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

# Function for calculating BMI
def calculate_bmi(weight, height):
    height_meters = height / 100  # Convert height to meters
    bmi = weight / (height_meters ** 2)
    return round(bmi, 2)

# Define exercise levels and corresponding exercises and foods
exercise_levels = {
    "Sedentary": {
        "exercises": ["Walking", "Stretching", "Yoga"],
        "foods": ["Oatmeal", "Avocados", "Nuts", "Fruit", "Vegetables"]
    },
    "Lightly Active": {
        "exercises": ["Jogging", "Swimming", "Cycling"],
        "foods": ["Lean Proteins", "Whole Grains", "Low-Fat Dairy", "Leafy Greens"]
    },
    "Moderately Active": {
        "exercises": ["Weight Training", "Running", "Hiking"],
        "foods": ["Chicken Breast", "Eggs", "Brown Rice", "Sweet Potatoes", "Spinach"]
    },
    "Very Active": {
        "exercises": ["CrossFit", "HIIT", "Martial Arts"],
        "foods": ["Salmon", "Quinoa", "Broccoli", "Avocado", "Greek Yogurt"]
    },
    "Extra Active": {
        "exercises": ["Powerlifting", "Olympic Weightlifting", "Endurance Running"],
        "foods": ["Steak", "Berries", "Whole Wheat Pasta", "Almond Butter", "Eggs"]
    }
}

class UserInfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.41, 0.8, 0.99, 1)  # Carolina Blue
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.title_label = Label(text="FITFAT: Your Daily Workout & Nutrition Guide App", font_size=30, size_hint=(1, None), height=50)
        self.layout.add_widget(self.title_label)

        self.form_layout = GridLayout(cols=2, padding=10, spacing=15, size_hint=(1, None))
        self.form_layout.bind(minimum_height=self.form_layout.setter('height'))

        self.name_label = Label(text="Name:")
        self.age_label = Label(text="Age:")
        self.height_label = Label(text="Height (cm):")
        self.weight_label = Label(text="Weight (kg):")

        self.name_input = TextInput(multiline=False, size_hint_y=None, height=40)
        self.age_input = TextInput(multiline=False, size_hint_y=None, height=40)
        self.height_input = TextInput(multiline=False, size_hint_y=None, height=40)
        self.weight_input = TextInput(multiline=False, size_hint_y=None, height=40)

        self.form_layout.add_widget(self.name_label)
        self.form_layout.add_widget(self.name_input)
        self.form_layout.add_widget(self.age_label)
        self.form_layout.add_widget(self.age_input)
        self.form_layout.add_widget(self.height_label)
        self.form_layout.add_widget(self.height_input)
        self.form_layout.add_widget(self.weight_label)
        self.form_layout.add_widget(self.weight_input)

        self.layout.add_widget(self.form_layout)

        self.submit_button = Button(text="Submit", on_press=self.submit_data, size_hint=(None, None), size=(200, 50))
        self.layout.add_widget(self.submit_button)

        self.settings_button = Button(text="Settings", on_press=self.go_to_settings, size_hint=(None, None), size=(200, 50))
        self.layout.add_widget(self.settings_button)

        self.add_widget(self.layout)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def submit_data(self, instance):
        name = self.name_input.text.strip()
        age = self.age_input.text.strip()
        height = self.height_input.text.strip()
        weight = self.weight_input.text.strip()

        if not name or not age.isdigit() or not height.isdigit() or not weight.isdigit():
            print("Please fill in all fields correctly.")
            return

        age = int(age)
        height = int(height)
        weight = int(weight)

        # Save user data to App's storage (in this case, to a list in the App class)
        app = App.get_running_app()
        app.saved_accounts.append({'name': name, 'age': age, 'height': height, 'weight': weight})

        self.manager.current = "activity_level_page"
        activity_screen = self.manager.get_screen("activity_level_page")
        activity_screen.set_user_data(name, age, weight, height)

    def go_to_settings(self, instance):
        self.manager.current = "settings_screen"

class ActivityLevelScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.41, 0.8, 0.99, 1)  # Carolina Blue
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.layout.add_widget(Label(text="Select Your Activity Level", font_size=30))

        self.activity_levels = ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Extra Active"]
        for level in self.activity_levels:
            button = Button(text=level, size_hint_y=None, height=50, on_press=self.select_activity_level)
            self.layout.add_widget(button)

        self.add_widget(self.layout)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def set_user_data(self, name, age, weight, height):
        self.name = name
        self.age = age
        self.weight = weight
        self.height = height

    def select_activity_level(self, instance):
        activity_level = instance.text
        self.manager.current = "final_screen"
        final_screen = self.manager.get_screen("final_screen")
        final_screen.set_user_data(self.name, self.age, self.weight, self.height, activity_level)

class FinalScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.41, 0.8, 0.99, 1)  # Carolina Blue
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        self.output_label = Label(text="", font_size=20, size_hint=(1, None), height=50)
        self.layout.add_widget(self.output_label)

        self.exercise_label = Label(text="", font_size=16, size_hint=(1, None), height=100)
        self.layout.add_widget(self.exercise_label)

        self.food_label = Label(text="", font_size=16, size_hint=(1, None), height=100)
        self.layout.add_widget(self.food_label)

        self.back_button = Button(text="Back to User's Info", size_hint=(None, None), size=(200, 50))
        self.back_button.bind(on_press=self.back_to_user_info)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def set_user_data(self, name, age, weight, height, activity_level):
        bmi = calculate_bmi(weight, height)
        exercises = exercise_levels.get(activity_level, {}).get("exercises", [])
        foods = exercise_levels.get(activity_level, {}).get("foods", [])
        self.output_label.text = f"Hello {name}, your BMI is {bmi}. You selected '{activity_level}'."
        self.exercise_label.text = f"Recommended Exercises: {', '.join(exercises)}"
        self.food_label.text = f"Recommended Foods: {', '.join(foods)}"

    def back_to_user_info(self, instance):
        self.manager.current = "user_info"

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.41, 0.8, 0.99, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.layout.add_widget(Label(text="Settings", font_size=20))

        self.saved_accounts_label = Label(text="Saved Accounts:", font_size=16, size_hint_y=None, height=40)
        self.layout.add_widget(self.saved_accounts_label)

        self.saved_accounts_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=200)
        self.scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, 200))
        self.scroll_view.add_widget(self.saved_accounts_layout)
        self.layout.add_widget(self.scroll_view)

        self.back_button = Button(text="Back to User's Info", size_hint=(None, None), size=(200, 50))
        self.back_button.bind(on_press=self.back_to_user_info)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

    def on_enter(self):
        # Show saved accounts when the Settings screen is opened
        self.saved_accounts_layout.clear_widgets()
        app = App.get_running_app()
        for account in app.saved_accounts:
            account_label = Button(text=f"{account['name']}, {account['age']} years old", size_hint_y=None, height=40)
            self.saved_accounts_layout.add_widget(account_label)

    def back_to_user_info(self, instance):
        self.manager.current = "user_info"

class ScreenManagement(ScreenManager):
    pass

class WeightLossApp(App):
    saved_accounts = []  # Store user data globally for now

    def build(self):
        sm = ScreenManagement()
        sm.add_widget(UserInfoScreen(name="user_info"))
        sm.add_widget(ActivityLevelScreen(name="activity_level_page"))
        sm.add_widget(FinalScreen(name="final_screen"))
        sm.add_widget(SettingsScreen(name="settings_screen"))
        sm.current = "user_info"
        return sm

if __name__ == '__main__':
    WeightLossApp().run()
