from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CPFUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(label="Nome", max_length=150)
    last_name = forms.CharField(label="Sobrenome", max_length=150)
    cpf = forms.CharField(
        label="CPF", max_length=11, help_text="Apenas dígitos (11 números)"
    )
    matricula = forms.CharField(label="Matrícula", max_length=50)

    class Meta:
        model = User
        fields = (
            "cpf",
            "email",
            "first_name",
            "last_name",
            "matricula",
            "password1",
            "password2",
        )

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        # Remove pontos e hífens
        if cpf:
            cpf = cpf.replace(".", "").replace("-", "")
        if not cpf or not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError(
                "CPF deve conter exatamente 11 dígitos numéricos."
            )
        return cpf

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este e-mail já está cadastrado.")
        return email

    def clean_matricula(self):
        matricula = self.cleaned_data.get("matricula")
        if User.objects.filter(matricula=matricula).exists():
            raise forms.ValidationError("Esta matrícula já está cadastrada.")
        return matricula

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.cpf
        if commit:
            user.save()
        return user


class CPFAuthenticationForm(forms.Form):
    cpf = forms.CharField(label="CPF", max_length=11)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        # Remove pontos e hífens
        if cpf:
            cpf = cpf.replace(".", "").replace("-", "")
        if not cpf or not cpf.isdigit() or len(cpf) != 11:
            raise forms.ValidationError(
                "CPF deve conter exatamente 11 dígitos numéricos."
            )
        return cpf
