from django import forms
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate # Para verificar a senha antiga
from django.core.exceptions import ValidationError

class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label="Senha Atual",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua senha atual'}),
        strip=False # Importante para senhas que podem ter espaços (embora raro)
    )
    new_password1 = forms.CharField(
        label="Nova Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Digite sua nova senha'}),
        help_text="<ul class='text-muted small'><li>Sua senha não pode ser muito parecida com suas outras informações pessoais.</li><li>Sua senha deve conter pelo menos 8 caracteres.</li><li>Sua senha não pode ser uma senha comumente usada.</li><li>Sua senha não pode ser inteiramente numérica.</li></ul>"
    )
    new_password2 = forms.CharField(
        label="Confirme a Nova Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme sua nova senha'})
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user # O usuário logado é passado para o formulário

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Sua senha atual está incorreta.")
        return old_password

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        # Validação de correspondência das novas senhas
        if new_password1 and new_password2 and new_password1 != new_password2:
            self.add_error('new_password2', "As novas senhas não coincidem.")

        # Validação de complexidade da nova senha (usando o validador do Django)
        if new_password1:
            try:
                validate_password(new_password1, user=self.user)
            except ValidationError as error:
                self.add_error('new_password1', error) # Adiciona o erro ao campo new_password1
                
        return cleaned_data

    def save(self):
        new_password = self.cleaned_data['new_password1']
        self.user.set_password(new_password)
        self.user.save()
        return self.user