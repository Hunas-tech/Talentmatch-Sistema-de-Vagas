from django import forms
from django.contrib.auth.models import User
from .models import Candidato, Empresa, Vaga


class CandidatoPerfilForm(forms.ModelForm):
    """Formulário para edição de perfil do candidato."""
    
    first_name = forms.CharField(
        max_length=150,
        required=True,
        label='Nome',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Seu nome'
        })
    )
    
    last_name = forms.CharField(
        max_length=150,
        required=True,
        label='Sobrenome',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'Seu sobrenome'
        })
    )
    
    user_email = forms.EmailField(
        required=True,
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
            'placeholder': 'seu@email.com'
        })
    )
    
    class Meta:
        model = Candidato
        fields = ['telefone', 'cidade', 'estado', 'habilidades', 'experiencia_anos', 
                  'escolaridade', 'pretensao_salarial', 'area_interesse', 'curriculo']
        widgets = {
            'telefone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': '(00) 00000-0000'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ex: São Paulo'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ex: SP'
            }),
            'habilidades': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Separe suas habilidades por vírgula (Ex: Python, JavaScript, React)',
                'rows': 3
            }),
            'experiencia_anos': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Anos de experiência',
                'min': 0
            }),
            'escolaridade': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ex: Superior Completo em Ciência da Computação'
            }),
            'pretensao_salarial': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ex: 5000',
                'step': '0.01',
                'min': 0
            }),
            'area_interesse': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Ex: Desenvolvimento Web, Data Science'
            }),
            'curriculo': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent',
                'placeholder': 'Resuma sua experiência profissional, projetos e conquistas',
                'rows': 5
            }),
        }
        labels = {
            'telefone': 'Telefone',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'habilidades': 'Habilidades',
            'experiencia_anos': 'Anos de Experiência',
            'escolaridade': 'Escolaridade',
            'pretensao_salarial': 'Pretensão Salarial (R$)',
            'area_interesse': 'Área de Interesse',
            'curriculo': 'Currículo / Resumo Profissional',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name
            self.fields['user_email'].initial = self.user.email
    
    def save(self, commit=True):
        candidato = super().save(commit=False)
        
        if self.user:
            self.user.first_name = self.cleaned_data.get('first_name', '')
            self.user.last_name = self.cleaned_data.get('last_name', '')
            self.user.email = self.cleaned_data.get('user_email', '')
            if commit:
                self.user.save()
        
        if commit:
            candidato.save()
        
        return candidato


class EmpresaPerfilForm(forms.ModelForm):
    """Formulário para edição de perfil da empresa."""
    
    user_email = forms.EmailField(
        required=True,
        label='Email de Contato',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
            'placeholder': 'contato@empresa.com'
        })
    )
    
    class Meta:
        model = Empresa
        fields = ['nome', 'cnpj', 'setor', 'site', 'telefone', 'cidade', 'estado', 
                  'endereco', 'descricao']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Nome da empresa'
            }),
            'cnpj': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-gray-100',
                'placeholder': '00.000.000/0000-00',
                'readonly': True
            }),
            'setor': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Ex: Tecnologia, Saúde, Educação'
            }),
            'site': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'https://www.suaempresa.com.br'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': '(00) 0000-0000'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Ex: São Paulo'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Ex: SP'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Endereço completo'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Descreva sua empresa, cultura, valores e o que a torna única',
                'rows': 5
            }),
        }
        labels = {
            'nome': 'Nome da Empresa',
            'cnpj': 'CNPJ',
            'setor': 'Setor de Atuação',
            'site': 'Website',
            'telefone': 'Telefone',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'endereco': 'Endereço',
            'descricao': 'Sobre a Empresa',
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['user_email'].initial = self.user.email
    
    def save(self, commit=True):
        empresa = super().save(commit=False)
        
        if self.user:
            self.user.email = self.cleaned_data.get('user_email', '')
            if commit:
                self.user.save()
        
        if commit:
            empresa.save()
        
        return empresa


class VagaForm(forms.ModelForm):
    """Formulário para criação e edição de vagas."""
    
    class Meta:
        model = Vaga
        fields = ['titulo', 'descricao', 'requisitos', 'habilidades_necessarias', 'nivel', 
                  'tipo', 'cidade', 'estado', 'salario_min', 'salario_max', 
                  'experiencia_minima', 'status']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Ex: Desenvolvedor Full Stack Python/React'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Descreva as responsabilidades, o que o candidato fará no dia a dia...',
                'rows': 6
            }),
            'requisitos': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Liste os requisitos obrigatórios e diferenciais',
                'rows': 4
            }),
            'habilidades_necessarias': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Separe por vírgula (Ex: Python, Django, React, PostgreSQL)',
                'rows': 2
            }),
            'nivel': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent'
            }),
            'tipo': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Ex: São Paulo'
            }),
            'estado': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Ex: SP'
            }),
            'salario_min': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Ex: 5000',
                'step': '0.01',
                'min': 0
            }),
            'salario_max': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Ex: 8000',
                'step': '0.01',
                'min': 0
            }),
            'experiencia_minima': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent',
                'placeholder': 'Anos de experiência',
                'min': 0
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent'
            }),
        }
        labels = {
            'titulo': 'Título da Vaga *',
            'descricao': 'Descrição da Vaga *',
            'requisitos': 'Requisitos *',
            'habilidades_necessarias': 'Habilidades Necessárias *',
            'nivel': 'Nível da Vaga *',
            'tipo': 'Tipo de Trabalho *',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'salario_min': 'Salário Mínimo (R$)',
            'salario_max': 'Salário Máximo (R$)',
            'experiencia_minima': 'Experiência Mínima (anos)',
            'status': 'Status da Vaga',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        salario_min = cleaned_data.get('salario_min')
        salario_max = cleaned_data.get('salario_max')
        
        if salario_min and salario_max and salario_min > salario_max:
            raise forms.ValidationError('O salário mínimo não pode ser maior que o salário máximo.')
        
        return cleaned_data
