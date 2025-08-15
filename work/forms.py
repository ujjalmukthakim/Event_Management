from django import forms
from django.contrib.auth.models import User, Group,Permission
from .models import Category,Event


class StyledFormMixin:
    """ Mixing to apply style to form field"""

    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

    default_classes = "border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder':  f"Enter {field.label.lower()}",
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                print("Inside Date")
                field.widget.attrs.update({
                    "class": "border-2 border-gray-300 p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500"
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                print("Inside checkbox")
                field.widget.attrs.update({
                    'class': "space-y-2"
                })
            else:
                print("Inside else")
                field.widget.attrs.update({
                    'class': self.default_classes
                })


class AssignRoleForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all())
    role = forms.ModelChoiceField(queryset=Group.objects.all())

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'start_date', 'time', 'location', 'category', 'participant','pic']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 text-gray-800 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200',
                'placeholder': 'Event Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-2 text-gray-800 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200 resize-none',
                'rows': 3,
                'placeholder': 'Event Description'
            }),
            'start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'block w-full px-4 py-2 text-gray-800 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'block w-full px-4 py-2 text-gray-800 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200'
            }),
            'location': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 text-gray-800 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200',
                'placeholder': 'Event Location'
            }),
            'category': forms.Select(attrs={
                'class': 'block w-full px-4 py-2 text-gray-800 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200'
            }),
            'participant': forms.CheckboxSelectMultiple(),
            'pic': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-gray-800 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200 bg-white cursor-pointer file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
            }),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'block w-full px-4 py-2 text-gray-800 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200',
                'placeholder': 'Category Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'block w-full px-4 py-2 text-gray-800 border border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-200 resize-none',
                'rows': 3,
                'placeholder': 'Category Description'
            }),
            
        }


class CreateGroupForm(forms.Form):
    name = forms.CharField(label="Group Name", max_length=150)
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Assign Permissions"
    )