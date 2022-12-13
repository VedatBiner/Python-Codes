from django import forms 

class RegisterForm(forms.Form): # Kayıt formu
    username = forms.CharField(max_length=50, label="Kullanıcı Adı")
    password = forms.CharField(max_length=20, label="Parola", widget=forms.PasswordInput)
    confirm = forms.CharField(max_length=20, label="Parolayı Doğrula", widget=forms.PasswordInput)
    
    def clean(self): # parola konfirmasyonu için Jango 'nun önerdiği yöntem
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("*** Parolalar Eşleşmiyor ***")

        # Eğer bilgilerde sorun yoksa aşağıdaki gibi bir dictionary oluşturup,
        # fonksiyondan dönüyoruz.
        values = {
            "username" : username,
            "password" : password
        } 
        return values

class LoginForm(forms.Form): # Giriş formu
    username = forms.CharField(label = "Kullanıcı Adı")
    password = forms.CharField(label = "Parola", widget = forms.PasswordInput)
